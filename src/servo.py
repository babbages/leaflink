from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Servo
from time import sleep

factory = PiGPIOFactory()
servo = Servo(21, pin_factory=factory)


def orient_motor():
    servo.min()

def operate_motor():
    servo.min()
    sleep(1)
    servo.mid()
    sleep(1)
    servo.max()
    sleep(1)
    # servo.mid()
    sleep(1)
    servo.min()
    
if __name__ == "__main__":
    while True:
        operate_motor()
