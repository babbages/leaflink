from gpiozero import LED
from time import sleep
import board, neopixel

relay = LED(16)
lights = neopixel.NeoPixel(board.D18, 50) # 50 lights in strip

def lights_on():
    relay.on()
    sleep(0.1)
    lights.fill((255,255,255))
    # print("lights on")

def lights_off():
    relay.off()
    # print("lights off")
    
if __name__ == "__main__":
    while True:
        lights_on()
        sleep(5)
        lights_off()
        sleep(5)
    GPIO.cleanup()
