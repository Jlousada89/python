import ewsclient #Changes to Suds to make it EWS compliant
import ewsclient.monkey # More Suds changes
import datetime
import os
import sys
import suds.client
import logging
import time
import Config
from suds.transport.https import WindowsHttpAuthenticated

#Uncomment below to turn on logging
#logging.basicConfig(level=logging.DEBUG)

#Logging on/accessing EWS SOAP API
domain = '<your-domain>'
username = r'<your-domain>\<your-user>'
password = '<your-pwd>'

transport = WindowsHttpAuthenticated(username=username, password=password)
client = suds.client.Client("https://%s/EWS/Services.wsdl" % domain, transport=transport,plugins=[ewsclient.AddService()])

#Now that the SOAP client is connected to EWS, send this XML soap message
client.service.CreateItem(__inject={'msg': 'test'})

#Uncomment below to turn on logging
logging.basicConfig(level=logging.DEBUG)
