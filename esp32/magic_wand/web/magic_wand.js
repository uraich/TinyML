
var maxRecords = 64;
var STROKE_POINT_COUNT = 160;

// UI elements
const bigButton = document.getElementById('bigButton');
const BLEstatus = document.getElementById('bluetooth');

if ("bluetooth" in navigator) {
  bigButton.addEventListener('click', function(event) {
    connect();
  });
  // else the browser doesn't support bluetooth
} else {
  msg("Browser not supported"); bigButton.style.backgroundColor = "red";
  alert("Error: This browser doesn't support Web Bluetooth. Try using Chrome.");
}

function msg(m){
  BLEstatus.innerHTML = m;
}

async function connect() {
  bigButton.style.backgroundColor="grey";
  msg('Requesting device ...');

  const device = await navigator.bluetooth.requestDevice({
    filters: [
      {
        services: [SERVICE_UUID] // SERVICE_UUID
      }
    ]
  });

  msg('Connecting to device ...');
  device.addEventListener('gattserverdisconnected', onDisconnected);
  const server = await device.gatt.connect();

  msg('Getting primary service ...');
  const service = await server.getPrimaryService(SERVICE_UUID);

  // Set up the characteristics
  for (const sensor of sensors) {
    msg("Characteristic "+sensor+"...");
    BLEsense[sensor].characteristic = await service.getCharacteristic(BLEsense[sensor].uuid);
    // Set up notification
    console.log("Characteristic "+sensor+"...");
    console.log("Can notify: ",BLEsense[sensor].characteristic.properties.notify);
    console.log("Can read: ",BLEsense[sensor].characteristic.properties.read);
    console.log("Can write: ",BLEsense[sensor].characteristic.properties.write);   
    if (BLEsense[sensor].properties.includes("BLENotify")){
      BLEsense[sensor].characteristic.addEventListener('characteristicvaluechanged',function(event){
        handleIncoming(BLEsense[sensor],event.target.value);
      });
      await BLEsense[sensor].characteristic.startNotifications();
    }
    // Set up polling for read
    /*
    if (BLEsense[sensor].properties.includes("BLERead")){
      BLEsense[sensor].polling = setInterval(function() {
        BLEsense[sensor].characteristic.readValue().then(function(data){
          handleIncoming(BLEsense[sensor],data);
        })}, 200);
      }
    */
    if (BLEsense[sensor].properties.includes("BLERead")){
      console.log("adding read event listener");
      BLEsense[sensor].characteristic.addEventListener('characteristicvaluechanged',function(event){
        console.log("characteristic change callback seen, value = ",event.target.value);
        handleIncoming(BLEsense[sensor],event.target.value);
      });
    }
      BLEsense[sensor].rendered = false;
    }
    bigButton.style.backgroundColor = 'green';
    msg('Connected.');
  }
  
  function getStrokePoints(dataview, byteOffset, littleEndian) {
    var result = [];
    var currentOffset = byteOffset;
    for (var i = 0; i < STROKE_POINT_COUNT; ++i) {
      var entry = {};
      entry.x = dataview.getInt8(currentOffset, littleEndian) / 128.0;
      currentOffset += 1;
      entry.y = dataview.getInt8(currentOffset, littleEndian) / 128.0;
      currentOffset += 1;
      result.push(entry);
    }
    return result;
  }

  function handleIncoming(sensor, dataReceived) {
    const columns = Object.keys(sensor.data); // column headings for this sensor
    const typeMap = {
      "Uint8":    {fn:DataView.prototype.getUint8,    bytes:1},
      "Uint16":   {fn:DataView.prototype.getUint16,   bytes:2},
      "Int32":    {fn:DataView.prototype.getInt32,    bytes:4},
      "Float32":  {fn:DataView.prototype.getFloat32,  bytes:4},
      "StrokePoints": {fn:getStrokePoints, bytes:(STROKE_POINT_COUNT* 2 * 1)},
    };
    var packetPointer = 0,i = 0;

    /* Check if we got real data */
    // if (dataReceived.byteLength == 0)
    //   return;

    console.log("handle_incoming, sensor: ",sensor);
    console.log("structure: ",sensor.structure)
    console.log("handle_incoming, data: ",dataReceived);
    
    // Read each sensor value in the BLE packet and push into the data array
    sensor.structure.forEach(function(dataType){      
      var unpackedValue;
      if (dataType === "StrokePoints") {
        console.log("packetPointer,i: ",packetPointer,i);
        var dataViewFn = typeMap[dataType].fn;
        console.log("dataViewFn: ",dataViewFn);
        unpackedValue = dataViewFn(dataReceived, packetPointer,true);
        console.log("unpacked value: ",unpackedValue)
      } else {
        var dataViewFn = typeMap[dataType].fn.bind(dataReceived);
        unpackedValue = dataViewFn(packetPointer,true);
        console.log("unpacked value: ",unpackedValue);
      }
      // Push sensor reading onto data array
      sensor.data[columns[i]].push(unpackedValue);
      // Keep array at buffer size
      if (sensor.data[columns[i]].length> maxRecords) {sensor.data[columns[i]].shift();}
      // move pointer forward in data packet to next value
      packetPointer += typeMap[dataType].bytes;
      bytesReceived += typeMap[dataType].bytes;
      i++;
    });
    console.log("state: ",sensor.data[columns[0]]);
    console.log("length: ",sensor.data[columns[1]]);
    sensor.rendered = false; // flag - vizualization needs to be updated
    console.log("sensor.onUpdate: ", sensor.onUpdate);
    if (typeof sensor.onUpdate != 'undefined') {
      sensor.onUpdate();
    }
  }

  function onDisconnected(event) {
    let device = event.target;
    bigButton.style.backgroundColor="red";
    // clear read polling
    for (const sensor of sensors) {
      if(typeof BLEsense[sensor].polling !== 'undefined'){
        clearInterval(BLEsense[sensor].polling);
      }
    }
    msg('Device ' + device.name + ' is disconnected.');
  }

  function BLEwriteTo(sensor){
    if (BLEsense[sensor].writeBusy) return; // dropping writes when one is in progress instead of queuing as LED is non-critical / realtime
    BLEsense[sensor].writeBusy = true; // Ensure no write happens when GATT operation in progress
    BLEsense[sensor].characteristic.writeValue(BLEsense[sensor].writeValue)
    .then(_ => {
      BLEsense[sensor].writeBusy = false;
    })
    .catch(error => {
      console.log(error);
    });
  }

var storedStrokes = [];
  
function storeStroke(strokePoints) {
  var storeIndex = storedStrokes.length;
  
  var template =
'      <div class="widget" id="store_' + storeIndex +'">' +
'        <div contenteditable="true" class="label"></div>' +
'        <div class="trash">&#128465;</div>' +
'        <canvas width="640px" height="640px" class="square"></canvas>' +
'      </div>';
  var storeDiv = document.querySelector('.gesture_store');
  var parser = new DOMParser();
  var html = parser.parseFromString(template, 'text/html');    
  storeDiv.prepend(html.body.firstChild);
  
  var strokeLabel = document.querySelector('#store_' + storeIndex +' > .label');
  strokeLabel.innerText = "?";
  strokeLabel.onfocus = onLabelFocus;
  strokeLabel.onblur = onLabelBlur;
  strokeLabel.onkeydown = onLabelKeydown;
  
  var strokeCanvas = document.querySelector('#store_' + storeIndex +' > canvas');
    
  const ctx = strokeCanvas.getContext('2d');
  ctx.fillStyle = "#111111";
  ctx.fillRect(0, 0, strokeCanvas.width, strokeCanvas.height);  

  drawStrokeGraph(strokeCanvas, strokePoints, strokePoints.length);
  
  storedStrokes.push({
    index: storeIndex,
    strokePoints: strokePoints,
    label: '',
  });
  onStoreChange();
  
  var strokeTrash = document.querySelector('#store_' + storeIndex +' > .trash');
  strokeTrash.onclick = onTrashClick;
}

function onLabelFocus(event) {
  if (event.target.innerText === '?') {
    event.target.innerText = '';
  }
}
  
function onLabelBlur(event) {
  var parent = event.target.parentElement;
  var id = parent.id;
  var index = Number(id.replace('store_', ''));
  var entry = storedStrokes.find(entry => entry.index === index);
  entry.label = event.target.innerText;
  onStoreChange();
}

function onLabelKeydown(event) {
  if (event.keyCode == 13) {
    event.preventDefault();
    event.target.blur();
  }  
}

function onTrashClick(event) {
  var parent = event.target.parentElement;
  var id = parent.id;
  parent.remove();

  var index = Number(id.replace('store_', ''));
  storedStrokes = storedStrokes.filter(entry => entry.index !== index);
  onStoreChange();
}
  
function onStoreChange() {
  var data = {
    strokes: storedStrokes,
  };
  var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(data));

  var downloadButton = document.querySelector('#downloadButton');
  downloadButton.setAttribute('href', dataStr);
  downloadButton.setAttribute('download', 'wanddata.json');
  
  var count = document.querySelector('#count');
  count.innerText = storedStrokes.length;
}
  
function initStrokeGraph() {
  var canvas = document.getElementById('stroke');
  const ctx = canvas.getContext('2d');
  ctx.fillStyle = "#111111";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
}

function drawStrokeGraph(canvas, strokePoints, strokeDataLength) {
  const ctx = canvas.getContext('2d');

  var canvasWidth = canvas.width;
  var canvasHeight = canvas.height;
  var halfHeight = canvasHeight / 2;
  var halfWidth = canvasWidth / 2;
  
  ctx.strokeStyle = "#ffffff";
  ctx.beginPath();
  for (var i = 0; i < strokeDataLength; ++i) {
    var x = strokePoints[i].x;
    var y = strokePoints[i].y;
    
    var xCanvas = halfWidth + (x * halfWidth);
    var yCanvas = halfHeight - (y * halfHeight);
    
    if (i === 0) {
      ctx.moveTo(xCanvas, yCanvas);
    } else if (i == (strokeDataLength - 1)) {
      ctx.lineTo(xCanvas+5, yCanvas+5);
      ctx.lineTo(xCanvas-5, yCanvas-5);
      ctx.moveTo(xCanvas+5, yCanvas-5);
      ctx.moveTo(xCanvas-5, yCanvas+5);      
    } else {
      ctx.lineTo(xCanvas, yCanvas);
    }
  }
  ctx.stroke();  
}
  
var previousStrokeState = 0;
  
function updateStrokeGraph() {
  var strokeData = BLEsense['stroke'].data;
  var strokeDataLength = strokeData.length.latest();
  var strokeState = strokeData.state.latest();
  var strokePoints = strokeData.strokePoints.latest();
  strokePoints = strokePoints.slice(0, strokeDataLength);
  
  if ((strokeState == 2) && (previousStrokeState != 2)) {
    storeStroke(strokePoints); 
  }
  previousStrokeState = strokeState;
  
  var label = document.getElementById('stroke_label');
  if (strokeState == 0) {
    label.innerText = "Waiting for gesture";
  } else if (strokeState == 1) {
    label.innerText = "Drawing";    
  } else {
    label.innerText = "Done";    
  }
  
  var canvas = document.getElementById('stroke');
  const ctx = canvas.getContext('2d');

  ctx.fillStyle = "#111111";
  ctx.fillRect(0, 0, canvas.width, canvas.height);  

  if (strokeState === 1) {
    drawStrokeGraph(canvas, strokePoints, strokeDataLength);
  }
}

var BLEsense =
{
  stroke:
  {
    uuid: '4798e0f2-300a-4d68-af64-8a8f5258404e',
    properties: ['BLERead'], // BLENotify only gives use the first 20 bytes.
    structure: [
      'Int32', 'Int32',
      'StrokePoints',
    ],
    data: {
      'state': [], 'length': [],
      'strokePoints': [],
    },
    onUpdate: updateStrokeGraph,
  },
};
const sensors = Object.keys(BLEsense);
const SERVICE_UUID = '4798e0f2-0000-4d68-af64-8a8f5258404e';
var bytesReceived = 0;
var bytesPrevious = 0;
    
// return last item of array
Array.prototype.latest = function(){
  return this[this.length - 1];
};

  function bytes(){
    if (bytesReceived > bytesPrevious){
      bytesPrevious= bytesReceived;
      msg(bytesReceived+" bytes received");
    }
  }

  var skip_frame = false;
  function draw(){
    function updateViz(sensor,fns){
      if (BLEsense[sensor].rendered == false) { // only render if new values are received
        fns.forEach(function(fn){
          fn(sensor);
        });
        BLEsense[sensor].rendered = true;
      }
    }
    if (skip_frame == false){ // TODO update with function to iterate object with viz function as a property      
      skip_frame = true;      // render alternate frames = 30fps
    } else {skip_frame=false;}
    requestAnimationFrame(draw);
  }
  
  initStrokeGraph();
    
  requestAnimationFrame(draw);
  
