/* javascript file for ble_temp.html */
const connectBtn = document.getElementById('connectBtn');
const disconnectBtn = document.getElementById('disconnectBtn');
const ble_status = document.getElementById('status');
const deviceName = document.getElementById('deviceName');
const deviceId = document.getElementById('deviceId');
const tempLabel = document.getElementById("tempLabel");
const minTempInput =  document.getElementById("minTemp");
const maxTempInput =  document.getElementById("maxTemp");

let connectBtnColor = connectBtn.style.backgroundColor;
let connectBtnText = connectBtn.textContent;
let newTempValue=0;
let newTempDisplay=0;
let fahrenheit = false;

const units = {
	Celcius: "°C",
	Fahrenheit: "°F"
};

const config = {
	minTemp: -20,
	maxTemp: 50,
	unit: "Celcius"
};

console.log("Connect button text: " + connectBtnText);

const ENV_SENSE_UUID = 0x181a;
const ENV_SENSE_TEMP_UUID = 0x2a6e;
if (!("bluetooth" in navigator)) {
    alert("Error: This browser doesn't support Web Bluetooth. Try using Chrome.");
  }
 var ble_device = null;

connectBtn.addEventListener('click', async () => {
  try {
    ble_status.textContent = 'Requesting device...';

    device = await navigator.bluetooth.requestDevice({
      filters: [
        { 
          services: [ENV_SENSE_UUID] // temperature service UUID 
        }
      ],
      
      // acceptAllDevices: true,
      optionalService: [ENV_SENSE_UUID],
    });

    ble_device = device;
    deviceId.textContent = "Device Id: " + device.id;
    deviceName.textContent = "Device name: " + device.name;  
    ble_status.textContent = `Connecting to ${device.name || device.id}...`;
    const server = await device.gatt.connect();
    const service = await server.getPrimaryService(ENV_SENSE_UUID);
    const char = await service.getCharacteristic(ENV_SENSE_TEMP_UUID);
    /*
    console.log("notify is permitted: ",char.properties.notify);
    console.log("read is permitted: ",char.properties.read);
    console.log("write is permitted: ",char.properties.write);
    */
    if (char.properties.read) {
      char.addEventListener(
        "characteristicvaluechanged",
        async (event) => {
          newTempValue = event.target.value.getInt16(0,true)/100;
          tempLabel.textContent = newTempValue.toString();
          // console.log("temp label: ",tempLabel);
          console.log(`Temperature measurement: ${newTempValue}`);
          setTemperature();
        },
      );
      await char.startNotifications();
    }
    /*
    var value = await char.readValue();
    var temp = value.getInt16(0,true);
    console.log("Type of received value: ",typeof value);
    var tempString = temp.toString(16)
    console.log("promise returned: ",value);
    console.log("Value read:" ,temp);
    console.log("Hex value: 0x",tempString);
    */

    // Remember to handle disconnects
    device.addEventListener('gattserverdisconnected', onDisconnected);
    connectBtn.disabled=true;
    connectBtn.textContent="Connected to " + device.name;
    connectBtn.style.backgroundColor = "rgb(0,255,0)";
    disconnectBtn.style.display = "inline";
    ble_status.textContent = "Connected";
  } catch (error) {
    ble_status.textContent = 'Error';
    console.error(error);
  }
});

// Change min and max temperature values

const tempValueInputs = document.querySelectorAll("input[type='text']");

tempValueInputs.forEach((input) => {
	input.addEventListener("change", (event) => {
		const newValue = event.target.value;
		
		if(isNaN(newValue)) {
			return input.value = config[input.id];
		} else {
			config[input.id] = input.value;
			return setTemperature();                        // Update temperature
		}
	});
});

// Switch unit of temperature

const unitP = document.getElementById("unit");

unitP.addEventListener("click", () => {
	config.unit = config.unit === "Celcius" ? "Fahrenheit" : "Celcius";
  console.log("Units: ",config.unit)
	unitP.innerHTML = config.unit + ' ' + units[config.unit];
  /* change lower and upper limits to reflect the new units */
  if (config.unit == "Fahrenheit") {
    config.minTemp=toFahrenheit(config.minTemp);
    config.maxTemp=toFahrenheit(config.maxTemp);
  }
  else {
    config.minTemp=toCelsius(config.minTemp);
    config.maxTemp=toCelsius(config.maxTemp);
  }
  console.log("new min: ",config.minTemp);
  minTempInput.value = config.minTemp;
  maxTempInput.value = config.maxTemp;

	return setTemperature();
})

// Change temperature

const temperature = document.getElementById("temperature");

function setTemperature() {
  if (config.unit == "Fahrenheit") {
    newTempDisplay = toFahrenheit(newTempValue);
  }
  else {
    newTempDisplay = newTempValue;
  }
	temperature.style.height = (newTempDisplay - config.minTemp) / (config.maxTemp - config.minTemp) * 100 + "%";
	temperature.dataset.value = newTempDisplay + units[config.unit];
}

disconnectBtn.onclick = async function() {
  console.log("ble device: ",ble_device);
  if (ble_device.gatt.connected) {
    console.log("disconnecting");
    await ble_device.gatt.disconnect();
    if (ble_device.gatt.connected)
      console.log("Still connected");
    else
      console.log("Disconnected");
  }
  else {
    console.log("Device is already disconnected");
  }
  
  connectBtn.disabled=false;
  connectBtn.textContent="Connect to Device";
  connectBtn.style.backgroundColor = null;
  disconnectBtn.style.display="none";
  ble_status.textContent = "Disconnected"
  deviceName.textContent = "";
  deviceId.textContent = "";
  tempLabel.textContent = "";
}
// disconnectBtn.onclick 
function onDisconnected(event) {
  const device = event.target;
  ble_status.textContent = `${device.name || device.id} disconnected`;
}
function toFahrenheit(degreesC) {
  return degreesC*9/5 + 32;
}
function toCelsius(degreesF){
  return (degreesF-32)*5/9;
}
console.log("Setting temperature");
console.log("Temp in Fahrenheit: ",toFahrenheit(newTempValue));
setTemperature();
