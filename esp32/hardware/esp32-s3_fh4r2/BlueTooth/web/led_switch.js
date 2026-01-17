const SERVICE_UUID = '6e400001-b5a3-f393-e0a9-e50e24dcca9e';
const TX_UUID = '6e400002-b5a3-f393-e0a9-e50e24dcca9e';
const RX_UUID = '6e400003-b5a3-f393-e0a9-e50e24dcca9e';

let redSlider = document.getElementById("red_color");
let greenSlider = document.getElementById("green_color");
let blueSlider = document.getElementById("blue_color");
let colorCanvas = document.getElementById("ledCanvas");
let submitBtn = document.getElementById("submitBtn");
let connectBtn = document.getElementById("connectBtn");
let switchToggle = document.getElementById("toggle");
let outgoing = document.getElementById("outgoing");
let incoming = document.getElementById("incoming");
let logMsg = document.getElementById("log");

let red = 0;
let green = 0;
let blue = 0;
let rgbColor = `rgb(${red}, ${green}, ${blue})`;
let currentSwitchState = false;
let ctx = colorCanvas.getContext("2d");

let TxCharacteristic;  // Rx and Tx are switched with respect to the ESP32 program 
let RxCharacteristic;
let device;
let origConnectText = connectBtn.textContent;
console.log("Text in connect button:",origConnectText);
ctx.fillStyle = rgbColor;
ctx.fillRect(0,0,colorCanvas.width,colorCanvas.height);
ctx.stroke();

redSlider.oninput = function() {
  red = redSlider.value;
  console.log("red color: ",red)
  rgbColor = `rgb(${red}, ${green}, ${blue})`;
  ctx.fillStyle = rgbColor;
  ctx.fillRect(0,0,colorCanvas.width,colorCanvas.height);
  ctx.stroke();
}
greenSlider.oninput = function() {
  green = greenSlider.value;
  console.log("green color: ",green);
  rgbColor = `rgb(${red}, ${green}, ${blue})`;
  ctx.fillStyle = rgbColor;
  ctx.fillRect(0,0,colorCanvas.width,colorCanvas.height);
  ctx.stroke();
}
blueSlider.oninput = function() {
  blue = blueSlider.value;
   console.log("blue color: ",blue)
  rgbColor = `rgb(${red}, ${green}, ${blue})`;
  ctx.fillStyle = rgbColor;
  ctx.fillRect(0,0,colorCanvas.width,colorCanvas.height);
  ctx.stroke();
}
/* Do not allow the user to change the switch toggle state */
switchToggle.onclick = function() {
  console.log("Not allowing user to change the state of the switch");
  switchToggle.checked = currentSwitchState;
}

const log = (text, color) => {
  logMsg.innerHTML = `<span style="color: ${color}">${text}</span><br>`;
};

/* Check for the BlueTooth browser extension */
if ("bluetooth" in navigator) {
  connectBtn.addEventListener('click', function(event) {
  connect();
});
}
// else the browser doesn't support bluetooth
else {
  log("browser not supported","red"); 
  alert("Error: This browser doesn't support Web Bluetooth. Try using Chrome.");
}

async function connect() {
  if (device && device.gatt.connected) {
    log("Already connected","red");
    return;
  }

  connectBtn.style.backgroundColor="none";
  log('Requesting device ...','blue');

  device = await navigator.bluetooth.requestDevice({
    filters: [
      {
        services: [SERVICE_UUID] // SERVICE_UUID
      }
    ]
  });

  log("Connecting to device ...","blue");
  console.log("Device name: ",device.name);
  device.addEventListener('gattserverdisconnected', onDisconnected);
  const server = await device.gatt.connect();

  log('Getting primary service ...','blue');
  const service = await server.getPrimaryService(SERVICE_UUID);
  
  // set up the characteristics
  log('Setting up characteristics ...','blue')
  console.log("Setting up characteristics");

  RxCharacteristic = await service.getCharacteristic(RX_UUID);
  // add notify callback
  
  RxCharacteristic.addEventListener('characteristicvaluechanged',
    function(event){
      handleIncoming(event.target.value);
    });
  await RxCharacteristic.startNotifications();
  
  TxCharacteristic = await service.getCharacteristic(TX_UUID);
  console.log("RxCharacteristic: ",RxCharacteristic);
  console.log("TxCharacteristic: ",TxCharacteristic);
  console.log("Tx characteristic, notify is permitted:" ,TxCharacteristic.properties.notify);
  console.log("Tx characteristic, read is permitted:" ,TxCharacteristic.properties.read);
  console.log("Tx characteristic, write is permitted:" ,TxCharacteristic.properties.write);
  console.log("Tx characteristic, write without response is permitted:" ,TxCharacteristic.properties.writeWithoutResponse);
  connectBtn.style.backgroundColor="rgb(0, 255, 0)";
  disconnectBtn.style.display = "inline";
  disconnectBtn.textContent="Disconnect from " + device.name;
  connectBtn.innerHTML="Connected to " + device.name;
  log("Connected","green");
}


function handleIncoming(switchState) {
  const textDecoder = new TextDecoder('utf8');
  let switchStateString = textDecoder.decode(switchState);
  incoming.innerHTML = switchStateString;
  if (switchStateString.includes("open")) {
    currentSwitchState = false;
    switchToggle.checked = currentSwitchState;
  }
  else if  (switchStateString.includes("closed")) { 
    currentSwitchState = true;
    switchToggle.checked = currentSwitchState; 
  }
  else
    log("I do not understand the switch state: " + switchStateString,"red");
}
/* treat submit */
/* the color components are read from the sliders and some text of the form
   r,g,b is create an sent to the BLE server */

submitBtn.onclick = ev => {
  if (!device) {
    log("Not connected yet","red");
    return;
  }
  ev.preventDefault();
  let rgbText = red.toString(10) + ", " 
    + green.toString(10) + ", " 
    + blue.toString(10);
  console.log("Submitting rgb:" + rgbText);
  console.log("TxCharacteristic: ",TxCharacteristic);
  /* convert the string to an array */
  let encoder = new TextEncoder();
  let msg = "LED rgb: " + rgbText;
  TxCharacteristic.writeValue(encoder.encode(msg));
  outgoing.innerHTML = msg;
};

disconnectBtn.onclick = async function() {
  console.log("ble device: ",device);
  if (device.gatt.connected) {
    console.log("disconnecting");
    await device.gatt.disconnect();
    if (device.gatt.connected)
      console.log("Still connected");
    else
      console.log("Disconnected");
  }
  else {
    console.log("Device is already disconnected");
  }
  
  connectBtn.textContent=origConnectText;
  connectBtn.style.backgroundColor = null;
  disconnectBtn.style.display="none";
}

function onDisconnected(event) {
    let device = event.target;
    connectBtn.style.backgroundColor = null;
    connectBtn.textContent=origConnectText;
    disconnectBtn.style.display="none";
    log('Device ' + device.name + ' is disconnected.',"red");
  }