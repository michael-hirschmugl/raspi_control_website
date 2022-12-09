'''

Adapted excerpt from Getting Started with Raspberry Pi by Matt Richardson

Modified by Rui Santos
Complete project details: http://randomnerdtutorials.com

'''

import RPi.GPIO as GPIO
from flask import Flask, render_template, request
app = Flask(__name__)
import raspi_gpio_control.set_pin as ass
import time

GPIO.setmode(GPIO.BCM)

# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
   23 : {'name' : 'GPIO 23', 'state' : GPIO.LOW},
   24 : {'name' : 'GPIO 24', 'state' : GPIO.LOW}
   }

@app.route("/")
def main():

   #for pin in pins:
   #   pins[pin]['state'] = GPIO.input(pin)

   templateData = {
      'pins' : pins
      }
   return render_template('main.html', **templateData)

@app.route("/<changePin>/<action>")
def action(changePin, action):
   changePin = int(changePin)
   action_value = 0
   if action == "on":
      action_value = 1
   if action == "off":
      action_value = 0
   time.sleep(3)
   templateData = {
      'pins' : pins
      }
   ass.set_raspi_pin(changePin, action_value)
   return render_template('main.html', **templateData)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=60, debug=True)

