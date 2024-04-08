import RPi.GPIO as GPIO
import time, requests

LAT = 35.996653
LON = -78.9018053
DO_PIN = 19
API_KEY = '5023fb07d222fcca1dfe21b2673d64c8'

def get_weather():
    weather_url = f'https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}'

    weather_resp = requests.get(weather_url)

    desc = weather_resp.json()['weather'][0]['description']

    return desc


GPIO.setmode(GPIO.BCM)
GPIO.setup(DO_PIN, GPIO.IN)

desc = get_weather()


while True:
    try:
        if desc == 'clear sky' or desc == 'few clouds':
            GPIO.output(DO_PIN, GPIO.HIGH)
            print("LED On")
        else:
            GPIO.output(DO_PIN, GPIO.LOW)
            print("LED Off")
    except:
        print("error")
    finally:
        time.sleep(2)