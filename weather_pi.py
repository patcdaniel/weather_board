import RPi.GPIO as GPIO
import time, get_weather
import urllib
  
GPIO.setmode(GPIO.BOARD)
GPIO.setup(37, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)
s = GPIO.PWM(37, 200)
t = GPIO.PWM(38, 200)
d = GPIO.PWM(40, 200)

# For temperature (in degrees F) with 3.3v and currnent resitor (shoudl change)


def get_duty_temp(temp):
    max_temp = 105 
    min_temp = 30
    step_range = (max_temp - min_temp)
    return round((temp-min_temp) / step_range,3)*100

def get_duty_wnd_spd(wind_spd):
    wind_spd = wind_spd * 2.237 # M/S to MPH
    max_spd = 50 
    min_spd = 0
    step_range = (max_spd - min_spd)
    return round((wind_spd - min_spd) / step_range,3)*100

def get_duty_wnd_dir(wind_dir):
    max_dir = 105 
    min_dir = 30
    step_range = (max_dir - min_dir)
    return round((wind_dir-min_dir) / step_range,3)*100
s.start(0)
t.start(0)
d.start(0)

while True:
    try:
        windSpeed,windDir,airTemp = get_weather.get_mlml_weather()
        t.ChangeDutyCycle(get_duty_temp(airTemp))
        s.ChangeDutyCycle(get_duty_wnd_spd(windSpeed))
        d.ChangeDutyCycle(get_duty_wnd_dir(windDir))
        print(windSpeed,windDir,airTemp)
        time.sleep(1)
    except KeyboardInterrupt:
        print('Stopped')
        break
    except urllib.error.URLError:
        print('Failed to retrieve data')
        time.sleep(5)
        continue

p.stop()
GPIO.cleanup()
