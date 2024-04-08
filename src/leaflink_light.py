import RPi.GPIO as GPIO
import time

DO_PIN = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(DO_PIN, GPIO.IN)

while True:
    try:
        light_state = GPIO.input(DO_PIN)
        print(light_state)
        if light_state == GPIO.LOW:
            print("More light")
        else:
            print("Less light")
    except:
        print("error")
    finally:
        time.sleep(2)

