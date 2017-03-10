import RPi.GPIO as GPIO
import time, get_weather
import urllib

GPIO.setmode(GPIO.BOARD)
GPIO.setup(36, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)
GPIO.setup(40, GPIO.OUT)

status_led = GPIO.PWM(36, 200)

s = GPIO.PWM(37, 200) #Wind speed
t = GPIO.PWM(38, 200) # Air Temp
d = GPIO.PWM(40, 200) # Wind Direction

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
        status_led.start(100)
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
        for i in range(10):
            # Blink LED if Ethernet connection is down
            if i % 2 == 0:
                status_led.ChangeDutyCycle(0)
            else:
                status_led.ChangeDutyCycle(100)
            time.sleep(.5)
        continue

t.stop()
s.stop()
d.stop()
status_led.stop()
GPIO.cleanup()
