from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
from turbo_flask import Turbo
turbo = Turbo(app)
import sys
sys.path.insert(0, './raspi_gpio_control')
from raspi_gpio_control.read_state_log import raspi_gio_read_state_log
from raspi_gpio_control.set_pin import raspi_gpio_control
import threading
import time


@app.route("/")
def main():
   inject_load()
   return render_template('main.html')

@app.route("/setpin/<pinNumber>/<pinState>")
def action(pinNumber, pinState):
   raspi_gpio_control(int(pinNumber), int(pinState))
   inject_load()

   return redirect(url_for('main'))

@app.context_processor
def inject_load():
   raspiPinStateDict = raspi_gio_read_state_log()
   templateData = {
      'raspiPinStateDict' : raspiPinStateDict
      }
   return templateData

@app.before_first_request
def before_first_request():
    threading.Thread(target=update_pin_states).start()

def update_pin_states():
    with app.app_context():
        while True:
            time.sleep(0.5)
            turbo.push(turbo.update(render_template('pin_control.html'), 'pin_states'))

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=60, debug=False)

