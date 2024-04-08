import time, board, busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

def moist_nums(chan):
    return (chan_0.value, chan_0.voltage)

if __name__ == "__main__":
    i2c = busio.I2C(board.SCL, board.SDA)
    adc = ADS.ADS1115(i2c)
    chan_0 = AnalogIn(adc, ADS.P0) # sensor 0
    
    while True:
        try:
            value, voltage = moist_nums(chan_0)
            print("\n" + str(value))
            if value > 21024:
                print("Dry")
            else:
                print("Wet")
        except:
            print("error")
        finally:
            time.sleep(2)