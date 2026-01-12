from microdot import Microdot, send_file
from microdot.websocket import websocket_upgrade
from wifi_connect import *
from machine import Timer
import asyncio

print ("Connecting to the network")
connect()

app = Microdot()

global triggered
triggered = False

def timerCallback(src):
    global triggered
    triggered = True

timer = Timer(0)
timer.init(period=1000, mode=Timer.PERIODIC, callback=timerCallback)

ws = None
@app.route('/')
async def index(request):
    return send_file('html/echo.html')

@app.route('/echo')
async def echo(request):
    global ws
    ws = await websocket_upgrade(request)
    
    print("WebSocket connection established")
    asyncio.create_task(readMsg())
    asyncio.create_task(writeMsg())
    while True:
        # data = await ws.receive()
        # print("Message received: ",data)
        # data = "Hello"
        # await ws.send(data)
        await asyncio.sleep_ms(1000)
        
async def readMsg():
    print("readMsg task created")
    while True:
        if ws == None:
            await asyncio.sleep_ms(100)
            continue
        msg = await ws.receive()
        print("msg received: ",msg)
        # await ws.send(data)
        
async def writeMsg():
    global triggered
    print("writeMsg task created")
    while True:
        if triggered:
            await ws.send("Hello from ISR")
            triggered = False
        else:
            await asyncio.sleep_ms(10)
        
print("Please connect to http://" + getIPAddress())
app.run(debug=2, host = getIPAddress(), port=80)

