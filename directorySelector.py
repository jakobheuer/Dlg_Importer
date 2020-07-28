# Jakob Heigl-Auer, 20.7.2020, Importer für .dlg nach URL
import sys
import os
import requests
import logging
import os.path
from os import path
from datetime import datetime
from decimal import Decimal
# Import smtplib for the actual sending function
import smtplib

# Here are the email package modules we'll need
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

def current_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S:%f")
    return(current_time)
"""
if(path.exists(sys.argv[1])==True): #Checks if path is real directory
    files = [dI for dI in os.listdir(sys.argv[1]) if os.path.isdir(os.path.join(sys.argv[1],dI))]
    for f in files:
        print(f)
elif(path.exists(sys.argv[1])==False): #If path is not a directory
    print("Error: [" + sys.argv[1] + "] wasn't found. Please check if the given path is correct.")
"""
# Create the container (outer) email message.
msg = MIMEMultipart()
msg['Subject'] = 'Test'
# me == the sender's email address
# family = the list of all recipients' email addresses
msg['From'] = me
msg['To'] = ', '.join(family)
msg.preamble = 'Our family reunion'

# Assume we know that the image files are all in PNG format
for file in pngfiles:
    # Open the files in binary mode.  Let the MIMEImage class automatically
    # guess the specific image type.
    with open(file, 'rb') as fp:
        img = MIMEImage(fp.read())
    msg.attach(img)

# Send the email via our own SMTP server.
s = smtplib.SMTP('localhost')
s.sendmail(me, family, msg.as_string())
s.quit()



server = smtplib.SMTP('w0194fd3.kasserver.com', 25)

#Next, log in to the server
server.login("m054a19d", "")

#Send the mail
msg = "Hello!\nTest" # The /n separates the message from the headers
server.sendmail("jakob.heigl-auer@konrad-technologies.at", "andreas.zeiner@konrad-technologies.at", msg)
print(current_time())
