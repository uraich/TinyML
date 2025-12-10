import sys
import asyncio
from microdot import Microdot
from wifi_connect import connect, getIPAddress

# connect to WiFi
connect()
app = Microdot()

frames = []
for file in ['images/1.jpg', 'images/2.jpg', 'images/3.jpg']:
    with open(file, 'rb') as f:
        frames.append(f.read())


@app.route('/')
async def index(request):
    return '''<!doctype html>
<html>
  <head>
    <title>Microdot Video Streaming</title>
    <meta charset="UTF-8">
  </head>
  <body>
    <h1>Microdot Video Streaming</h1>
    <img src="/video_feed">
  </body>
</html>''', 200, {'Content-Type': 'text/html'}


@app.route('/video_feed')
async def video_feed(request):
    print('Starting video stream.')

    # MicroPython can only use class-based async generators
    class stream():
        def __init__(self):
            self.i = 0
            
        def __aiter__(self):
            return self
            
        async def __anext__(self):
            await asyncio.sleep(1)
            self.i = (self.i + 1) % len(frames)
            return b'Content-Type: image/jpeg\r\n\r\n' + \
                frames[self.i] + b'\r\n--frame\r\n'
            
        async def aclose(self):
            print('Stopping video stream.')
    
    print("Type of stream(): ",type(stream()))
    return stream(), 200, {'Content-Type':
                           'multipart/x-mixed-replace; boundary=frame'}


if __name__ == '__main__':
    app.run(debug=True,host=getIPAddress(), port=80)
