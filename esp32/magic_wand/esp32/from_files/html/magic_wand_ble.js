const connectBtn = document.getElementById('connectBtn');
const statusEl = document.getElementById('status');
const output = document.getElementById('output');

const MAGIC_WAND_UUID = "4798e0f2-0000-4d68-af64-8a8f5258404e";
const MAGIC_WAND_CHARACTERISTIC_UUID = "4798e0f2-300a-4d68-af64-8a8f5258404e";

/* prints a message on the status label in a defined color */
const msg = (text, color) => {
    statusEl.innerHTML = `<span style="color: ${color}">${text}</span><br>`;
}

async function temporary_msg(text,color) {
    let current_background = statusEl.style.backgroundColor;
    let current_text = statusEl.innerHTML;
    console.log("current text: ",current_text);
    msg(text,color);
    await sleep_ms(1000); // display the message during 1 s
    statusEl.innerHTML = `<span style="color: ${current_background}">${current_text}</span><br>`;
}

const STATUS = Object.freeze({
    WAITING: 0,
    DRAWING: 1,
    DONE: 2,
})

let currentStroke = [];
  
// sleep a number of ms
async function sleep_ms(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}

// return last item of array
Array.prototype.latest = function(){
    return this[this.length - 1];
};

/* ---------------------------------------------------*/
/* This is the main program
/* ---------------------------------------------------*/

if (!("bluetooth" in navigator)) {
    alert("Error: This browser doesn't support Web Bluetooth. Try using Chrome.");
}

connectBtn.addEventListener('click', async () => {
    try {
	statusEl.textContent = 'Requesting device...';

	const device = await navigator.bluetooth.requestDevice({
	    
	    filters: [
		{ 
		    services: [MAGIC_WAND_UUID] // temperature service UUID 
		}
	    ],
	    
	    // acceptAllDevices: true,
	    optionalService: [MAGIC_WAND_UUID],
	});

	statusEl.textContent = `Connecting to ${device.name || device.id}...`;
	const server = await device.gatt.connect();

	const service = await server.getPrimaryService(MAGIC_WAND_UUID);
	const char = await service.getCharacteristic(MAGIC_WAND_CHARACTERISTIC_UUID);
    console.log("read is supported: ",char.properties.read);
    console.log("notify is supported: ",char.properties.notify);
    console.log("write is supported: ",char.properties.write);

    if (char.properties.read) {
      char.addEventListener(
        "characteristicvaluechanged",
        async (event) => {
            let dv = event.target.value;
            // console.log("characteristic change seen");
            handleIncoming(dv);
        },
      );
      await char.startNotifications();
    }
    msg(`Connected to ${device.name}`,"green");
    connectBtn.style.backgroundColor =  `rgb(129, 233, 69)`; // light green

	// Remember to handle disconnects
	device.addEventListener('gattserverdisconnected', onDisconnected);


    } catch (error) {
        console.log("In connection error");
        await temporary_msg("error: " + error,"red");
        console.error(error);    
        msg("Click button to connect to the board","white");
        connectBtn.style.backgroundColor = null; // reset to default color  
    }
});

async function onDisconnected(event) {
    const device = event.target;
    await temporary_msg(`${device.name || device.id} disconnected`,"red");
    msg("Click button to connect to the board","white");
    connectBtn.style.backgroundColor = null; // reset to default color  
}

initStrokeGraph();


/* handles incoming data
   The packet is converted into a dataview for further treatment 
   Gets the stroke status and updates the message on the basic canvas
   If we are in drawing state, draw on the main canvas
   If we are going from done state to waiting, copy the main canvas to
   the store
*/
async function handleIncoming(dataview) {
    console.log("Msg received: ", typeof dataview);        
    updateStrokeGraph(dataview);
}

function getStrokePoints(dataview, littleEndian) {
    var result = [];
    var currentOffset = 8;
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
        console.log("offset: ",currentOffset, "stroke length: ",strokeLength, " entry: ",entry);
        result.push(entry);
    }
    return result;
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
        } 
        /*else if (i == (strokeDataLength - 1)) {
          ctx.lineTo(xCanvas+5, yCanvas+5);
          ctx.lineTo(xCanvas-5, yCanvas-5);
          ctx.moveTo(xCanvas+5, yCanvas-5);
          ctx.moveTo(xCanvas-5, yCanvas+5);      
          }*/ 
        else {
            ctx.lineTo(xCanvas, yCanvas);
        }
    }
    ctx.stroke();  
}
function clearCanvas(canvas) {
    const ctx = canvas.getContext('2d');

    ctx.fillStyle = "#111111";
    ctx.fillRect(0, 0, canvas.width, canvas.height);  
    
}
var previousStrokeState = STATUS.WAITING;

function updateStrokeGraph(dataview) {
    
    var label = document.getElementById('stroke_label');
    var canvas = document.getElementById('stroke');
    
    var strokeState = dataview.getInt32(0,true);
    var strokeDataLength = dataview.getInt32(4,true);
    
    var strokePoints = getStrokePoints(dataview,true)
    currentStroke = currentStroke.concat(strokePoints);
    console.log("Current length of stroke: ",currentStroke.length/2);

    // strokePoints = strokePoints.slice(0, strokeDataLength);
    
    if ((strokeState == STATUS.DONE) && (previousStrokeState != STATUS.DONE)) {
        storeStroke(strokePoints);
        clearCanvas(canvas);
        currentStroke = [];
    }
    
    previousStrokeState = strokeState;

    if (strokeState == STATUS.WAITING) {
        label.innerText = "Waiting for gesture";
    } else if (strokeState == STATUS.DRAWING) {
        label.innerText = "Drawing";    
    } else {
        label.innerText = "Done";
        clearCanvas(canvas);    
    }

    if (strokeState == STATUS.DRAWING) {
        console.log("No of stroke points: ",currentStroke.length);
        drawStrokeGraph(canvas, currentStroke, currentStroke.length);
    }
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

async function onLabelBlur(event) {
    var parent = event.target.parentElement;
    var id = parent.id;
    var index = Number(id.replace('store_', ''));
    console.log("event.target.innerText: ",event.target.innerText);

    if ((event.target.innerText.trim().length == 0)) {
        console.log("event comes from ",typeof event.target);
        event.target.innerText = "?";
    }
    else {
        var entry = storedStrokes.find(entry => entry.index === index);
        entry.label = event.target.innerText;
        onStoreChange();
    }
}                

function onLabelKeydown(event) {
    if (event.keyCode == 13) {  // key 13 is key 0xd which is the return key
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
    /*
      var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(data));
      console.log("on store change");
      console.log("length of store: ",storedStrokes.length);
      var downloadBtn = document.querySelector('#downloadBtn');
      downloadBtn.setAttribute('href', dataStr);
      downloadBtn.setAttribute('download', 'wanddata.json');
    */
    var count = document.querySelector('#count');
    count.innerText = storedStrokes.length;
}

function download() {
    var data = {
        strokes: storedStrokes,
    };
    var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(data));

    //creating an invisible element

    let element = document.createElement('a');
    element.setAttribute('href',dataStr);
    element.setAttribute('download', "magic_wand_data.json");
    document.body.appendChild(element);
    element.click();

    document.body.removeChild(element);
}

// Start file download.

document.getElementById("downloadBtn").addEventListener("click", async function () {
    /* check if there are any strokes in the store */
    if (storedStrokes.length == 0) {
        temporary_msg("There are no registered strokes yet, download refused","red");
        return;             
    }
    /* check if all labels have been defined */
    console.log("No of strokes in store: ",storedStrokes.length);
    for (let i=0; i<storedStrokes.length; i++) {
        console.log (`Stroke ${i} label: ${storedStrokes[i].label}`);
        if (storedStrokes[i].label === "") {
            temporary_msg("Not all labels are defined yet, download refused","red");
            return;
        }
    }
    download();
}, false);

