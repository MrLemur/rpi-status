# Simple Raspberry Pi Web Status Page
# - /u/TheLadDothCallMe
# 
# DISCLAIMER: I won't be held accountable for what you do with
# this script. Use it however you choose, and let me know
# if you create something cool with it!
#
# This script collects various infos about the Pi
# and then inserts them into an HTML template before
# printing it to the screen.
# It is meant to be used by calling the script from the
# command line and outputting the result to an file
# on a webserver.
#
# Example usage: "python status.py > /var/wwww/html/status.html"
#
# As it is HTML, the whole look and feel can be modified in the
# template below if you know a little CSS. Additional information
# can be added by adding the output of a shell command to a variable
# and enclosing it within a DIV of class "detailItem" in the template.

import psutil # Only used pretty much for getting the RAM values
import time
from subprocess import check_output

# This has the main HTML template that is used every time the script is run.
# If you have issue after modifying it, make sure you have your quotes in
# the right places. Notepad++ is great for synatx highlighting it.
def printHtml():
	print '''<html>
	<head>
		<title>Raspberry Pi Status</title>
		<link href='https://fonts.googleapis.com/css?family=Oswald' rel='stylesheet' type='text/css'>
		<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1" />
		<style>
			body {
			background-color: #1C1C1C;
			font-family: 'Oswald', sans-serif;
			}
			
			#container {
			width: 100%;
			max-width: 600px;
			margin: 20px auto;
			padding-top: 10px;
			background-color: #585858;
			}
			
			#details {
			display:block;
			padding:10px;
			}
			
			#logo {
			background-image: url("rpi.png");
			background-size: auto 150px;
			background-repeat: no-repeat;
			height: 150px;
			width: 125px;
			margin: 0px auto;
			}
			
			.detailItem {
			padding: 5px;
			margin: 10px;
			background-color: #A4A4A4;
			vertical-align:middle;
			}
			
			#ramBar {
			width:100%;
			height: 20px;
			background-color:#75a928;
			}
			
			#ramFill {
			float:left;
			width: ''' + ram_percent + '''%;
			height:100%;
			background-color:#bc1142;
			}
		</style>
	</head>
	<body>
		<div id="container">
			<div id="logo"></div>
			<div id="details">
				
				<div class="detailItem">Hostname: ''' + hostname + '''</div>
				<div class="detailItem">Uptime: ''' + uptime + '''</div>
				<div class="detailItem">CPU Temp: ''' + temp + ''' &deg;C</div>
				
				<div class="detailItem">RAM: ''' + ram_used + ''' MB used of ''' + ram_total + ''' MB, ''' + ram_free + ''' MB free
					<div id="ramBar">
						<div id="ramFill"></div>
					</div>
				</div>
				
			<div class="detailItem">Google Ping: ''' + ping + ''' ms</div>
			<div class="detailItem">Last Updated: ''' + updated + '''</div>
		</div>
		
	</body>
</html>'''
	
	return

hostname = check_output(["hostname"]).strip() # Just shows the hostname command. Note the .split() function to get rid of any new lines from the shell.
ram_total = str(psutil.virtual_memory().total / 1024 / 1024) # The calculations here are just lazy and round to the nearest integer.
ram_used = str((psutil.virtual_memory().total - psutil.virtual_memory().available) / 1024 / 1024)
ram_free = str(psutil.virtual_memory().available / 1024 / 1024)
ram_percent = str(psutil.virtual_memory().percent)
uptime = check_output(["uptime", "-p"]).strip() # Shows the uptime from the shell with the pretty option
updated = time.strftime("%H:%M:%S %d/%m/%Y") # The last time the script was run
temp = str(round(float(check_output(["cat","/sys/class/thermal/thermal_zone0/temp"])) / 1000,1)) # Reads the CPU temp in milligrade
ping = check_output(["ping -c 5 8.8.8.8 | tail -1| awk -F '/' '{print $5}'"],shell=True).strip() # Pings Google DNS 5 times and awks the average ping time

printHtml() # Calls the function and puts everything together
