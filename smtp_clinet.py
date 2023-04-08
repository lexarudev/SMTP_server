# Include modules

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
# Create the message

sender = 'sender@example.com'
recipient = 'recipient@example.com'
msg = MIMEMultipart()
msg['Subject'] = 'Test email'
msg['From'] = sender
msg['To'] = recipient

# setup the parameters of the message
file_location = 'Sonya.png'
msg['person'] = 'Sonya'
msg['image'] = 'Sonya.png'
filename = os.path.basename(file_location)
attachment = open(file_location, "rb")

p = MIMEBase('application', 'octet-stream')

# To change the payload into encoded form
p.set_payload((attachment).read())

# encode into base64
encoders.encode_base64(p)

p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

# attach the instance 'p' to instance 'msg'
msg.attach(p)

server = smtplib.SMTP('192.168.104.11', 1025)
server.set_debuglevel(True) # show communication with the server

try:

    sending_data = msg.as_string()
    print(sending_data)
    server.sendmail(sender, recipient, sending_data)
    
finally:
    server.quit()
    