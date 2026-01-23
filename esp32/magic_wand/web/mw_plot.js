/* read the digits.json file containing 10 gestures, one for each digit */

const WAITING = 0; // code for "waiting"
const DRAWING = 1;
const DONE = 2;
var maxRecords = 64;
/* this is the main program 
   It reads the json file and then calls treatData to extract the state, length and stroke data */

fetch('digits.json')
    .then((response) => response.json())  // parse the json file
    .then(data => treatData(data))        // work with the data
    .catch(error => console.error('Error fetching digits.json: ',error));

// sleep a number of ms
async function sleep_ms(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/* converts the dictionary read from the json file into a dataview with the same
   format as the ones coming from the esp32 via BlueTooth BLE or web sockets */

async function treatData(data) {
  // treat all the digits, waiting 5s between each plot
  for (let i=0;i<10;i++) {
    dv = dict2dataview(data["strokes"][i]);
    dv.setInt32(0,DRAWING,true);     
    handleIncoming(sensor.stroke,dv); // this will draw into the left canvas
    await sleep_ms(2000);
    /* now set state to done */
    // let doneBuffer = new ArrayBuffer(8);
    // let doneView = new DataView(doneBuffer);
    dv.setInt32(0,DONE,true); // set stroke status to done
    handleIncoming(sensor.stroke,dv);
    await sleep_ms(5000);
  }
}

/* this functions takes a strokePoints dictionary and converts it into a DataView 
   identical to what we see, when stroke data are transmitted through BlueTooth of web sockets. 
   The data treatment is then the same, as if the data are transmitted from the esp32 */

function dict2dataview(dict) {
  let strokeLength = dict["strokePoints"].length;
  console.log("Length of stroke: ",strokeLength);
  let strokeLabel = dict["label"];
  console.log("Stroke Label: ",strokeLabel);
  let buffer = new ArrayBuffer(2*strokeLength +2*4);
  console.log("Length of buffer: ",(buffer.byteLength-8)/2);
  let dv = new DataView(buffer);
  dv.setInt32(0,DONE,true); // fill the status field to drawing
  dv.setInt32(4,strokeLength,true);  // and the stroke length field
 
  /* The rest of the ArrayBuffer within the DataView are one byte signed x,y values */
  let x;
  let y;
  for (let i=0;i<strokeLength;i++) {
    x = Math.round(parseFloat(dict["strokePoints"][i]["x"])*128.0);
    y = Math.round(parseFloat(dict["strokePoints"][i]["y"])*128.0);
    dv.setInt8(2*i + 8,x);
    dv.setInt8(2*i + 1+8,y);
  }
  /* The rest of the code is just used for visualization on the console */
  let bufview = new Uint8Array(buffer);  // this is needed to get at the values of buffer

  // console.log("status: ",bufview[0].toString(16),bufview[1].toString(16),bufview[2].toString(16),bufview[3].toString(16));
  // console.log("length: ",bufview[4].toString(16),bufview[5].toString(16),bufview[6].toString(16),bufview[7].toString(16));

  let line = [];
  for (let i=0; i<16;i++) {   // print the first 8 x and y values
    line.push("0x" + bufview.slice(2*i+8,2*i+9).toHex());
    line.push(", 0x" + bufview.slice(2*i+9,2*i+10).toHex());
  }
  console.log("First 8 x,y values: ",line);
  return dv;
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
  console.log(html.body.firstChild);
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
  console.log("stroke length: ",strokePoints.length);
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
  
async function onLabelBlur(event) {
  var parent = event.target.parentElement;
  var id = parent.id;
  var index = Number(id.replace('store_', ''));
  console.log("onLabelBlur, index: ",index);
  var entry = storedStrokes.find(entry => entry.index === index);
  console.log("event.target.innerText: ",event.target.innerText);

  
  /* if there was some text before, which was eliminated, a lf is returned */
  if (event.target.innerText.trim().length == 0){   
    event.target.innerText = "?";
    entry.label = "";
  }
  else 
    entry.label = event.target.innerText;
    console.log("entry.label: ",entry.label);
  onStoreChange();
}

function onLabelKeydown(event) {
  if (event.keyCode == 13) {   // key 13 is key 0xd which is the return key
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
  console.log("updateStrokeGraph");
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

var sensor =
{
  stroke:
  {
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

const sensors = Object.keys(sensor);
var bytesReceived = 0;
var bytesPrevious = 0;
console.log("sensor: ",sensor);
console.log("bytesReveived",bytesReceived);

// return last item of array
Array.prototype.latest = function(){
  return this[this.length - 1];
};

function getStrokePoints(dataview, byteOffset, littleEndian) {
    var result = [];
    var currentOffset = byteOffset;
    // read the length of the gesture
    let strokeLength = dataview.getInt32(4,true);
    console.log("stroke length read from dataview: ",strokeLength);
    console.log("offset: ",currentOffset);

    for (var i = 0; i < strokeLength; ++i) {
    var entry = {};
      entry.x = dataview.getInt8(currentOffset, littleEndian) / 128.0;
      currentOffset += 1;
      entry.y = dataview.getInt8(currentOffset, littleEndian) / 128.0;
      currentOffset += 1;
      // console.log("offset: ",currentOffset, " entry: ",entry);
      result.push(entry);
      //console.log("result_entry: offset x,y",currentOffset,result[(currentOffset-8)/2-1]);
    }
    return result;
  }

var entry = {};
entry.x = 5
entry.y = 6
console.log("entry: ",entry);

function handleIncoming(sensor, dataReceived) {
  // console.log("In handleIncoming: sensor:",sensor);
  // console.log("sensor.data: ",sensor.data);
  // console.log(dataReceived);
  strokeLength = dataReceived.getInt32(4,true);
  // console.log("in handleIncoming, strokeLength: ",strokeLength);
  const columns = Object.keys(sensor.data); // column headings for this sensor
  const typeMap = {
    "Uint8":    {fn:DataView.prototype.getUint8,    bytes:1},
    "Uint16":   {fn:DataView.prototype.getUint16,   bytes:2},
    "Int32":    {fn:DataView.prototype.getInt32,    bytes:4},
    "Float32":  {fn:DataView.prototype.getFloat32,  bytes:4},
    "StrokePoints": {fn:getStrokePoints, bytes:(strokeLength* 2 * 1)},
  };

  var packetPointer = 0,i = 0;

  // console.log("handle_incoming, sensor: ",sensor);
  // console.log("structure: ",sensor.structure)
  // console.log("handle_incoming, data: ",dataReceived);
    
  /* Extracts state, stroke length and the stroke from the dataview */
  sensor.structure.forEach(function(dataType){      
    var unpackedValue;
    if (dataType === "StrokePoints") {
      console.log("packetPointer,i: ",packetPointer,i);
      var dataViewFn = typeMap[dataType].fn;
      console.log("dataViewFn: ",dataViewFn);
      unpackedValue = dataViewFn(dataReceived, packetPointer,true);
      console.log("unpacked value: ",unpackedValue[0]);
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

function updateStrokeGraph() {
  console.log("In updateStrokeGraph");
  var strokeData = sensor['stroke'].data;
  var strokeDataLength = strokeData.length.latest();
  var strokeState = strokeData.state.latest();
  var strokePoints = strokeData.strokePoints.latest();
  strokePoints = strokePoints.slice(0, strokeDataLength);
  console.log("previousStrokeState: ",previousStrokeState, ", current stroke state: ",strokeState);
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
