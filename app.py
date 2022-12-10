'''

Adapted excerpt from Getting Started with Raspberry Pi by Matt Richardson

Modified by Rui Santos
Complete project details: http://randomnerdtutorials.com

'''

import RPi.GPIO as GPIO
from flask import Flask, render_template, request
app = Flask(__name__)
import sys
sys.path.insert(0, './raspi_gpio_control')
from raspi_gpio_control.read_state_log import raspi_gio_read_state_log
from raspi_gpio_control.set_pin import raspi_gpio_control
import time

GPIO.setmode(GPIO.BCM)

# Create a dictionary called pins to store the pin number, name, and pin state:
#pins = {
#   23 : {'name' : 'GPIO 23', 'state' : GPIO.LOW},
#   24 : {'name' : 'GPIO 24', 'state' : GPIO.LOW}
#   }

@app.route("/")
def main():

   raspiPinStateDict = raspi_gio_read_state_log()
   #for pin in pins:
   #   pins[pin]['state'] = GPIO.input(pin)

   templateData = {
      'raspiPinStateDict' : raspiPinStateDict
      }
   
   return render_template('main.html', **templateData)

@app.route("/setpin/<pinNumber>/<pinState>")
def action(pinNumber, pinState):
   raspi_gpio_control(int(pinNumber), int(pinState))
   raspiPinStateDict = raspi_gio_read_state_log()
   templateData = {
      'raspiPinStateDict' : raspiPinStateDict
      }
#   changePin = int(changePin)
#   action_value = 0
#   if action == "on":
#      action_value = 1
#   if action == "off":
#      action_value = 0
#   time.sleep(3)
#   templateData = {
#      'pins' : pins
#      }
#   ass.set_raspi_pin(changePin, action_value)
   return render_template('main.html', **templateData)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=60, debug=True)

