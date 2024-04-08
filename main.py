from src.leaflink_temp import get_temp_humid
from src.leaflink_moist import moist_nums
import RPi.GPIO as GPIO
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_dht, board, time, busio
import csv, os
from datetime import datetime

# temp/humid setup sensor
dht_device = adafruit_dht.DHT11(board.D26)

# moisture setup sensor
i2c = busio.I2C(board.SCL, board.SDA)
adc = ADS.ADS1115(i2c)
chan_0 = AnalogIn(adc, ADS.P0) # sensor 0

# light sensor
light_pin = 12
GPIO.setmode(GPIO.BCM)
GPIO.setup(light_pin, GPIO.IN)
    
# record data
# csv file
filename = "plant_data.csv"
file_exists = os.path.isfile(filename)
with open(filename, "a", newline="") as csvfile:
    csvwriter = csv.writer(csvfile)
    if not file_exists:
        csvwriter.writerow(["date_time", "temperature_c", "temperature_f",
                            "humidity", "soil_moisture", "light"])
        
    while True:
        try:
            # time
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            
            # temp/humid
            temp_c, temp_f, humid = get_temp_humid(dht_device)
            if temp_c == -9999:
                continue
            print(f"{temp_c} C, {temp_f} F, {humid} %")
            
            # moisture
            # lower value mean moisture is high
            moisture_level = chan_0.value
            if moisture_level > 21024:
                print("Dry:", str(moisture_level))
            else:
                print("Wet:", str(moisture_level))
                
            # light
            light_state = GPIO.input(light_pin)
            if light_state == GPIO.LOW:
                print("More light")
            else:
                print("Less light")
                
            # change value to reflect yes/no in output
            # 1 is light is on
            light_state -= 1
            if light_state == -1:
                light_state = 1
                
            # csv
            csvwriter.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                temp_c,
                temp_f,
                humid,
                moisture_level,
                light_state
                ])
            
        except:
            print("error")
        finally:
            print("")
            time.sleep(2)
