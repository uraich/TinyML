# The simplest possible WEB server printing "Hello World!"
# Program written for the IoT course at the University of Cape Coast
# copyright (c) U. Raich April 2020
# This program is released under GPL

import picoweb
import time
import network
import uasyncio as asyncio
import wifi_connect

print ("Connecting to the network")
wifi_connect.connect()
ipaddr=wifi_connect.getIPAddress()

html = """ <!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
</head>
<body>
<title>Hello World </title>
<h1>The Hello World! HTML page</h1>
<p>This is the Hello World html page Version 1, served by a picoweb WEB server.<br>
  The html code is embedded in the server itself. There is no separate HTML file. <br>
  The program was written for<br>
  the <b>Course on the Internet of Things (IoT) </b>at the
  University of Cape Coast (Ghana) <br>
  Copyright (c) U. Raich, April 2020, <br>released under GPL
  
</p>

</body>
</html> 
"""
print("Starting the Hello World WEB server")

app = picoweb.WebApp("__main__")

@app.route("/")
def index(req, resp):
     yield from resp.awrite(html)

app.run(debug=2, host = ipaddr,port=80)
