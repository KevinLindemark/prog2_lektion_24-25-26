from threading import Thread
from flask import Flask, render_template, Response
import pigpio
from time import sleep
import subprocess
from flask_socketio import SocketIO
from datetime import datetime
from camera_pi import Camera
import adc_moist

pi = pigpio.pi()
GPIO_RED_LED = 13
GPIO_BLUE_LED = 12
GPIO_PUMP = 17

pi.set_PWM_range(GPIO_RED_LED, 100)
pi.set_PWM_range(GPIO_BLUE_LED, 100)
pi.set_PWM_frequency(GPIO_RED_LED, 100000)
pi.set_PWM_frequency(GPIO_BLUE_LED, 100000)
pi.set_PWM_dutycycle(GPIO_BLUE_LED, 0)
pi.set_PWM_dutycycle(GPIO_BLUE_LED, 0)
pi.set_mode(GPIO_RED_LED, pigpio.OUTPUT)
pi.set_mode(GPIO_BLUE_LED, pigpio.OUTPUT)
pi.set_PWM_dutycycle(GPIO_RED_LED, 0)
pi.set_PWM_dutycycle(GPIO_BLUE_LED, 0)


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('red_led_change')
def red_led(data):
    lysstyrke = int(data['red_led_brightness'])
    print(lysstyrke)
    if lysstyrke < 0:
        lysstyrke = 0

    if lysstyrke > 50:
        lysstyrke = 50

    pi.set_PWM_dutycycle(GPIO_RED_LED, lysstyrke)

@socketio.on('blue_led_change')
def red_led(data):
    lysstyrke = int(data['blue_led_brightness'])
    print(lysstyrke)
    if lysstyrke < 0:
        lysstyrke = 0

    if lysstyrke > 50:
        lysstyrke = 50

    pi.set_PWM_dutycycle(GPIO_BLUE_LED, lysstyrke)


@app.route('/')
def home():
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
def send_soil():
    while True:            
        moisture = adc_moist.get_soilmoisture_percentage()
        socketio.emit('soil_measure', moisture)
        sleep(2)

soil_thread = Thread(target=send_soil)
soil_thread.start()

@app.route('/soil')
def soil():
    moisture = adc_moist.get_soilmoisture_percentage()
    return render_template('soil.html', moisture = moisture)
    
if __name__ == '__main__':
    socketio.run(app, port="9999", host="0.0.0.0", debug=True)
