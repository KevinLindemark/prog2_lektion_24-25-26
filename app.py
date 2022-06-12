import base64
from io import BytesIO
from matplotlib.figure import Figure
import sqlite3
from threading import Thread
from flask import Flask, render_template, Response
import pigpio
from time import sleep
import subprocess
from flask_socketio import SocketIO
from datetime import datetime
from camera_pi import Camera
import adc_moist

conn=sqlite3.connect('database.sqlite', check_same_thread=False)
curs=conn.cursor()

pi = pigpio.pi()
GPIO_RED_LED = 13
GPIO_BLUE_LED = 12
GPIO_PUMP = 17

pi.set_PWM_range(GPIO_RED_LED, 100)
pi.set_PWM_range(GPIO_BLUE_LED, 100)
pi.set_PWM_frequency(GPIO_RED_LED, 100000)
pi.set_PWM_frequency(GPIO_BLUE_LED, 100000)
pi.set_mode(GPIO_RED_LED, pigpio.OUTPUT)
pi.set_mode(GPIO_BLUE_LED, pigpio.OUTPUT)
if pi.get_PWM_dutycycle(GPIO_BLUE_LED) > 40 or pi.get_PWM_dutycycle(GPIO_RED_LED) > 30:
    pi.set_PWM_dutycycle(GPIO_RED_LED, 30)
    pi.set_PWM_dutycycle(GPIO_BLUE_LED, 40)
redStartVal = pi.get_PWM_dutycycle(GPIO_RED_LED)
blueStartVal = pi.get_PWM_dutycycle(GPIO_BLUE_LED)

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('red_led_change')
def red_led(data):
    lysstyrke = int(data['red_led_brightness'])
    print(lysstyrke)
    if lysstyrke < 0:   
        lysstyrke = 0

    if lysstyrke > 30:
        lysstyrke = 30
    print("setting red LED PWM to: ", lysstyrke)
    pi.set_PWM_dutycycle(GPIO_RED_LED, lysstyrke)

@socketio.on('blue_led_change')
def red_led(data):
    lysstyrke = int(data['blue_led_brightness'])
    print(lysstyrke)
    if lysstyrke < 0:
        lysstyrke = 0

    if lysstyrke > 40:
        lysstyrke = 40

    pi.set_PWM_dutycycle(GPIO_BLUE_LED, lysstyrke)


@app.route('/')
def home():
    # global redStartVal
    # global blueStartVal
    if LEDValues.state == True:
        pi.set_PWM_dutycycle(GPIO_BLUE_LED, LEDValues.blue_val)
        pi.set_PWM_dutycycle(GPIO_RED_LED, LEDValues.red_val)
        LEDValues.state = False
        redStartVal = pi.get_PWM_dutycycle(GPIO_RED_LED)
        blueStartVal = pi.get_PWM_dutycycle(GPIO_BLUE_LED)
    else:
        redStartVal = pi.get_PWM_dutycycle(GPIO_RED_LED)
        blueStartVal = pi.get_PWM_dutycycle(GPIO_BLUE_LED)
    return render_template('index.html', redStartVal = redStartVal, blueStartVal= blueStartVal)

@app.route('/photo/')
def photo():
    sleep(2)
    timestamp = datetime.now()
    #date and time format: dd/mm/YYYY H:M:S
    format = "%d-%m-%Y-%H-%M-%S"
    #format datetime using strftime() 
    timestamp = timestamp.strftime(format)
    cmd = f'raspistill --width 1080 --height 640 -vf -o /home/pi/greenhouse/static/{timestamp}.jpeg'
    print(cmd)
    subprocess.call(cmd, shell=True)
    return render_template("photo.html", timestamp = timestamp)

@app.route("/video/")
def video():
    """Video streaming home page."""
    return render_template('video.html')

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
class LEDValues:
    red_val = 0
    blue_val = 0
    state = False
def soil_monitor():
    while True:
        try:
            moisture = adc_moist.get_soilmoisture_percentage()
            socketio.emit('soil', moisture)
            sleep(4)
        except AssertionError as error:
            print(f"Soilmoisture measure error{error}")
def pump_monitor():
    while True:
        try:
            pump_state = pi.read(GPIO_PUMP)
            socketio.emit('pump', pump_state)
            sleep(2)
        except AssertionError as e:
            print(f"pump error {e}")

soil_moisture_thread = Thread(target=soil_monitor)
soil_moisture_thread.start()
moisture = adc_moist.get_soilmoisture_percentage()

pump_monitor_thread = Thread(target=pump_monitor)
pump_monitor_thread.start()
@app.route('/soil')
def soil():
    soil_plot = plot_soilmoisture()
    LEDValues.state = True
    LEDValues.blue_val = pi.get_PWM_dutycycle(GPIO_BLUE_LED)
    LEDValues.red_val = pi.get_PWM_dutycycle(GPIO_RED_LED)
    pi.set_PWM_dutycycle(GPIO_BLUE_LED, 0)
    pi.set_PWM_dutycycle(GPIO_RED_LED, 0)
    pump_startval = pi.read(GPIO_PUMP)
    return render_template('soil.html', moisture = moisture, pump_startval = pump_startval, soil_plot = soil_plot)
@socketio.on('start_pump')
def start_pump():
    try:
        print("Starting pump for 1 second")
        pi.write(GPIO_PUMP, 1)
        # the pump gives aproximately 200 mililiters of water per 10 seconds
        sleep(3)
        pi.write(GPIO_PUMP, 0)
        print("Stopped pump again!")
    except:
        print("Something went wrong, stopping pump")
        pi.write(GPIO_PUMP, 0)


def getHistData (numSamples):
	curs.execute("SELECT * FROM soilmoisture ORDER BY timestamp DESC LIMIT "+str(numSamples))
	data = curs.fetchall()
	dates = []
	soilmoisture_data = []

	for row in reversed(data):
		dates.append(row[0])
		soilmoisture_data.append(row[1])
		
	return dates, soilmoisture_data

def plot_soilmoisture():
    times, soilmoisture_data = getHistData(4)
    # Generate the figure **without using pyplot**.
    print("times :",times)
    ys = soilmoisture_data
    xs = times
    fig = Figure()
    ax = fig.subplots()
    fig.subplots_adjust(bottom=0.3) 
    ax.tick_params(axis="x", which="both", rotation=30)
    ax = fig.subplots()
    ax.set_facecolor("#000") # inner plot background color HTML black
    fig.patch.set_facecolor('#000') # outer plot background color HTML black
    ax.plot(xs, ys, linestyle = 'dashed', c = 'green', linewidth = '1.5',
     marker = 'o', mec = 'red', ms = 10, mfc = 'red' )
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('Soilmoisture percentage %')
    ax.xaxis.label.set_color('green') #setting up X-axis label color to hotpink
    ax.yaxis.label.set_color('green') #setting up Y-axis label color to hotpink
    ax.tick_params(axis='x', colors='white') #setting up X-axis tick color to white
    ax.tick_params(axis='y', colors='white') #setting up Y-axis tick color to white
    ax.spines['left'].set_color('green') # setting up Y-axis tick color to blue
    ax.spines['top'].set_color('green') #setting up above X-axis tick color to blue
    ax.spines['bottom'].set_color('green') #setting up above X-axis tick color to blue
    ax.spines['right'].set_color('green') #setting up above X-axis tick color to blue
    fig.subplots_adjust(bottom=0.3) 
    ax.tick_params(axis="x", which="both", rotation=30) 
   
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    #print(data)
    return data

if __name__ == '__main__':
    socketio.run(app, port="9999", host="0.0.0.0", debug=True)
