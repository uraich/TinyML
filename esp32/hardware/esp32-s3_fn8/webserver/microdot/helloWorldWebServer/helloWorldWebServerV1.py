# The simplest possible WEB server printing "Hello World!"
# Program written for the IoT course at the University of Cape Coast
# This first version does not use picoweb but accesses the socket interface
# directly
# copyright (c) U. Raich April 2020
# This program is released under GPL

from wifi_connect import connect, getIPAddress
from microdot.microdot import Microdot

print ("Connecting to the network")
connect()

html = """ <!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
</head>
<body>
<title>Hello World </title>
<h1>The Hello World! HTML page</h1>
<p>This is the Hello World html page Version 1, served by a Microdot WEB server.<br>
  The html code is embedded in the server itself. There is no separate HTML file. <br>
  The program was written for<br>
  the <b>Course on the Internet of Things (IoT) </b>at the
  University of Cape Coast (Ghana) <br>
  Copyright (c) U. Raich, April 2020, <br>released under GPL
  
</p>

</body>
</html> 
"""
app = Microdot()

@app.route('/')
async def hello(request):
    return html, 200, {'Content-Type': 'text/html'}


@app.route('/shutdown')
async def shutdown(request):
    request.app.shutdown()
    return 'The server is shutting down...'


app.run(debug=True, host=getIPAddress(), port=80)
