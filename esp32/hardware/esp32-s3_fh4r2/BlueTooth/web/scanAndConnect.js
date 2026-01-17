const connectButton = document.getElementById('connect');
const statusEl = document.getElementById('status');
const output = document.getElementById('output');

// const SERVICE_UUID = '6e400001-b5a3-f393-e0a9-e50e24dcca9e'
// const CHARACTERISTIC_UUID = '4798e0f2-300a-4d68-af64-8a8f5258404e'
const SERVICE_UUID = '6e400001-b5a3-f393-e0a9-e50e24dcca9e';
const CHARACTERISTIC_UUID = '6e400002-b5a3-f393-e0a9-e50e24dcca9e';
if (!("bluetooth" in navigator)) {
    alert("Error: This browser doesn't support Web Bluetooth. Try using Chrome.");
  }
  
connectButton.addEventListener('click', async () => {
  try {
    statusEl.textContent = 'Requesting device...';

    const device = await navigator.bluetooth.requestDevice({
      
      filters: [
        { 
          services: [SERVICE_UUID] // NUS service UUID 
        }
      ],
      
      // acceptAllDevices: true,
      optionalService: [SERVICE_UUID],
    });

    statusEl.textContent = `Connecting to ${device.name || device.id}...`;
    const server = await device.gatt.connect();

    statusEl.textContent = 'Getting Magic Wand Service...';
    const service = await server.getPrimaryService(SERVICE_UUID);

    const char = await service.getCharacteristic(CHARACTERISTIC_UUID);
    
    
    // Remember to handle disconnects
    device.addEventListener('gattserverdisconnected', onDisconnected);
  } catch (error) {
    statusEl.textContent = 'Error';
    output.textContent = error;
    console.error(error);
  }
});

function onDisconnected(event) {
  const device = event.target;
  output.textContent = `${device.name || device.id} disconnected`;
}
