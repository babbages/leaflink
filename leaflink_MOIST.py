import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)

water = 20

GPIO.setup(water, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def read_soil_MOIST():
    if GPIO.input(water):
        return f"MOIST | {GPIO.input(water)}"
    else:
        return f"Dry as the Sahara desert | {GPIO.input(water)}"

try:
    while True:
        MOISTURE_level = read_soil_MOIST()
        time.sleep(2)

        print(MOISTURE_level)
        # if GPIO.input(water):
        #     print("THE WATER NATION")
        # else:
        #     print("THE FIRE NATION ATTACKED")
except Exception as e:
    print(e)

GPIO.cleanup()