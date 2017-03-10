# rpi-status
A simple Python script that gathers various infos about a Raspberry Pi and outputs an HTML page

## Prerequisites
1. Linux based OS on your Pi (I'm using Raspbian on Pi 2 B)
2. A web server of some sort (Apache/Nginx/LightHTPD). I'm using Nginx cause it is lightweight but highly configurable.
3. The user you will be running the Python script as needs write access to the HTML directory (/var/www/html in this case)
4. PSUtil Python library installed (I used this guide: http://www.isendev.com/app/entry/39)

## Installation Instructions
1. Copy the status.py script into your home directory (e.g. /home/pi/status.py) and the rpi.png to your public HTML folder (e.g. /var/www/html/rpi.png).
2. In your terminal, set the script as executable - chmod +x ~/status.py
3. To test if the script is working run python ~/status.py > /var/www/html/status.html in your terminal.
4. In a browser go to http://[your Raspberry PI IP address]/status.html (e.g. http://192.168.1.5/status.html)
5. Now to get it to automatically update, I set up a cron job to run the above command every 5 minutes. I find this provides a pretty good refresh rate of information.
6. In your terminal run crontab -e. This should bring up your text editor with your crontab (list of cron jobs). if it asks to choose a default editor, choose Nano cause it's easy to navigate.
7. At the bottom, add the following line */5 * * * * python ~/status.py > /var/www/html/status.html (This will cause the script to run every 5 minutes. You can change that to whatever you want (e.g. */30 for every half hour).
8. Save the file (Ctrl + X and then type Y in Nano)
9. If you don't want to change anything, then you are now done!

If you get a permission denied message, make sure you have added the executable flag on the status.py script, and you have write access to the HTML directory.

## Optional configuration

If you want to modify some of the information that is displayed, it should be pretty simple if you look at the script. Apart from the RAM info, everything else is just an output from a shell command added to a string variable. The script used the check_output() function of the subprocess library. Then the variable is inserted into the HTML template. I use Notepad++ as I find it helpful for syntax highlighting and showing me where the quotes start and end.

For example, take this command that shows the uptime: uptime = check_output(["uptime", "-p"]).strip()

uptime is the variable name, check_output(["uptime", "-p"]) is the commad I want to run (the first argument is the actual command e.g. cat, ls etc., and the second argument is the parameters or switches passed to it, -p in this instance). The .strip() is there to get rid of any returns and new lines that the shell command gives. Use it if you find the command is inserting lines where there shouldn't be.
The next step is to insert that variable into the HTML template, which is easy enough to do. The div that is used to display the information is of class detailItem. That means you can have as many as you want (as long as they are one after another), and the HTML page will still look nice. Just make sure you put it under the RAM part, or it will probably break. Here is the HTML for the div for uptime:
<div class="detailItem">Uptime: ''' + uptime + '''</div>
Basically you can copy and paste this, and then just change the information to what you want before the quotes. Note the ''' before and after the variable name. This needs to be there, otherwise Python doesn't know which is the HTML template and which is the variable that holds your information. Hopefully this is pretty self explanatory.
Now for simplicity's sake, let's say I want to add the output of the shell command date to the status page. I'd add a new line at the bottom of the script where the variables are defined (should be obvious) that reads:
date = check_output(["date"]).strip()
Then in the HTML template at the top in the printHtml() function, I'd create and new line under the div I want it to appear and add the following:
<div class="detailItem">Date: ''' + date+ '''</div>
Now you just save the script to it's location in your home directory and give it a test (step 5 from above).

## Note about output from more than one shell command

If you are using a shell command that is using pipes or more than one command (like it is used for opening and grepping the DNSmasq log), you will need to modify how thecheck_output() function is used. Instead of using two arguments, you just pass the whole argument like so:
something = check_output(["cat /some/file | grep \"info you want\""],shell=True).strip()
The whole command is pasted in (you may need to escape double quotes in your shell command with a backslash), and the second argument is shell=True. This means just run the whole command without sanatising the input. This is quite a big security risk in Python, and I normally wouldn't use it but it works for what I need it to. The script doesn't accept user input, so it should be quite safe if your Pi is secured from the outside world.

## DNS queries

I've only tested the DNS query bit with the DNSmasq log. if you are using DNSmasq, you may need to change the part of the script which points to the location of log file. Mine is in /var/log/dnsmasq.log. The user running the script needs to have read access to the log file.

## Issue with ping command

The Google DNS ping command would not work unless I was running as root. I ran sudo chmod u+s /bin/ping in the terminal and this fixed it.
