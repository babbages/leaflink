import RPi.GPIO as GPIO
from time import sleep



def pump_water():
    # Set GPIO mode
    GPIO.setmode(GPIO.BCM)

    # Define pins for left motor
    left_forward_pin = 23
    left_backward_pin = 22

    # Set GPIO pins as output
    GPIO.setup(left_forward_pin, GPIO.OUT)
    GPIO.setup(left_backward_pin, GPIO.OUT)
    
    GPIO.output(left_forward_pin, GPIO.HIGH)
    sleep(5)
    GPIO.output(left_forward_pin, GPIO.LOW)
    
if __name__ == "__main__":
    pump_water()




