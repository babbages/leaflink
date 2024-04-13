import RPi.GPIO as GPIO
import time

def button_press():
    # Set GPIO mode
    GPIO.setmode(GPIO.BCM)

    # Set up GPIO pin 19 as input
    button_pin = 19
    GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Read the state of the button
    button_state = GPIO.input(button_pin)

    # Check if button is pressed (state is LOW because of pull-up resistor)
    if button_state == GPIO.LOW:
        print("Button pressed")
        # Add a small delay to debounce the button
        time.sleep(1)
        
if __name__ == "__main__":
    while True:
        try:
            button_press()
        except:
            pass
        