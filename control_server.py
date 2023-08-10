import threading
import mysql.connector
from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from art import *


# Enter Raspberry Device's IP
device_ip = "192.168.3.150"

# Pins
led_pin = 27
buzzer_pin = 17

# Database
db_host = '103.136.41.122'
db_name = 'iotdevice'
db_user = 'misl'
db_password = 'Misladmin@soft123'

print(text2art("NR IOT"))
print(decor("barcode1")+decor("barcode1")+decor("barcode1")+decor("barcode1")+decor("barcode1"))

print(' ')
print(' ')

# Current date and time
print('Current Date & Time:', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
print(' ')

# Copyright
print('Copyright ©', datetime.now().strftime('%Y'), 'Nipuna Rangika. All rights reserved.')
print(' ')
print('----------------------------------------------------------------------------')
print(' ')


# Connect to Device
print('Connecting to Device')
factory = PiGPIOFactory(host=device_ip)
print('Connection Successful!')

# Set Device GPIO Pins
led = LED(led_pin, pin_factory=factory)      # GPIO17 Pin
buzzer = LED(buzzer_pin, pin_factory=factory)   # GPIO27 Pin
print('LED Pin Set to GPIO' + str(led_pin) +
      ' & Buzzer Pin Set to GPIO' + str(buzzer_pin))

# Set Database
mydb = mysql.connector.connect(
    host=db_host,
    database=db_name,
    user=db_user,
    password=db_password
)
print('Database Set to Host : ' + str(db_host) +
      ' & Database Name : ' + str(db_name))
cursor = mydb.cursor()
print(' ')
print('----------------------------------------------------------------------------')
print(' ')










##### Add Startup function to check if there are already unclosed ALarms





class RequestHandler(BaseHTTPRequestHandler):

    alert_running = False

    # Start Alert
    def alertOn(self):
        RequestHandler.alert_running = True

        # Run Alert
        while RequestHandler.alert_running:
            led.on()        # red on
            buzzer.on()     # buzzer on
            sleep(0.5)      # Wait 1 second in the above state
            led.off()       # red off
            buzzer.off()     # buzzer on
            sleep(0.2)      # Wait 0.5 seconds in the above state

    # End Alert
    def alertOff(self):
        RequestHandler.alert_running = False
        led.off()       # red on
        buzzer.off()    # buzzer on


    # Insert the new entry into the 'device_runs' table
    def createDbEntry(self, device_location):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = "INSERT INTO device_runs (start_time, device_location) VALUES (%s, %s)"
        values = (current_time, device_location)
        cursor.execute(query, values)
        mydb.commit()

    # Update end time of Last record of specified device location 'device_runs' table
    def updateDbEntry(self, device_location):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = 'UPDATE device_runs SET end_time = %s WHERE device_location = %s AND id = (SELECT MAX(id) FROM device_runs WHERE device_location = %s)'
        values = (current_time, device_location, device_location)
        cursor.execute(query, values)
        mydb.commit()

    def checkActiveDevices(self):
        query = "SELECT COUNT(*) FROM device_runs WHERE end_time IS NULL"
        cursor.execute(query)
        status = cursor.fetchone()[0]
        if status > 0:
            return 1
        else:
            return 0
        
    def checkDeviceStatus(self, device_location):
        query = "SELECT COUNT(*) FROM device_runs WHERE end_time IS NULL AND device_location = '" + device_location + "'"
        cursor.execute(query)
        device_status = cursor.fetchone()[0]
        if device_status > 0:
            return 1
        else:
            return 0

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Hello! Sorry! There is nothing here!')
            self.checkAlertEndStatus()

        elif self.path == '/trigger':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            # Read the JSON body from the request
            content_length = int(self.headers['Content-Length'])
            request_body = self.rfile.read(content_length).decode('utf-8')

            # Parse the JSON body
            json_data = json.loads(request_body)

            device_location = json_data['location']                  
        
            # Check the value of the 'notification' field
            if 'notification' in json_data:
                if json_data['notification'] == 'on':
                    
                    if self.checkDeviceStatus(device_location)==0:
                        self.createDbEntry(device_location)
                        if not RequestHandler.alert_running:
                            alert_thread = threading.Thread(target=self.alertOn)
                            print("Alert On | Alert On successfully for " + device_location + " device")
                            print(' ')
                            alert_thread.start()
                        else:
                            print("Alert Already On | Alert already triggered from other devices. ON Entry created for " + device_location + " device")
                    else:
                        print("Alert Already ON | Alert for " + device_location + " device already ON")

                elif json_data['notification'] == 'off':
                    self.updateDbEntry(device_location)
                    if self.checkActiveDevices() == 0:
                        if RequestHandler.alert_running:
                            print("Alert Off | Alert Off successfully for " + device_location + " device")
                            print(' ')
                            self.alertOff()
                        else:
                            print("Alert Not Running | Alert is not running on any device")
                            print(' ')
                    else:
                        print("Alert Still Active | Alerts are still active on some devices. OFF Entry created for " + device_location + " device")
                        print(' ')
                else:
                    # Prepare the response JSON
                    response_data = {
                        'message': 'Invalid Command'
                    }
                    # Convert the response JSON to string
                    response_body = json.dumps(response_data)
                    # Send the response message
                    self.wfile.write(response_body.encode('utf-8'))
        else:
            self.send_error(404, 'Not Found')



# Set the host and port for the server
host = 'localhost'
port = 8000

# Create an HTTP server with the specified host and port, and the custom request handler
server = HTTPServer((host, port), RequestHandler)

# Start the server and keep it running until interrupted
print(f'Starting server on http://{host}:{port}')
print(' ')
server.serve_forever()
