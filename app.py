from flask import Flask, render_template, request
app = Flask(__name__)
import sys
sys.path.insert(0, './raspi_gpio_control')
from raspi_gpio_control.read_state_log import raspi_gio_read_state_log
from raspi_gpio_control.set_pin import raspi_gpio_control


@app.route("/")
def main():

   raspiPinStateDict = raspi_gio_read_state_log()

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

   return render_template('main.html', **templateData)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=60, debug=True)

