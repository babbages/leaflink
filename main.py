from src.leaflink_temp import get_temp_humid
from src.leaflink_moist import moist_nums
import RPi.GPIO as GPIO
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_dht, board, time, busio
import csv, os
from datetime import datetime
from src.servo import *
from src.lights import *
from src.pump import *
from src.sp_to_text import *
from src.espeak import *
from src.voice_clone import *

# temp/humid setup sensor
dht_device = adafruit_dht.DHT11(board.D26)

# moisture setup sensor
i2c = busio.I2C(board.SCL, board.SDA)
adc = ADS.ADS1115(i2c)
chan_0 = AnalogIn(adc, ADS.P0) # sensor 0

# light sensor
light_pin = 12
button_pin = 19
GPIO.setmode(GPIO.BCM)
GPIO.setup(light_pin, GPIO.IN)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

orient_motor()


# Master Loop
while True:
    # speech
    button_state = GPIO.input(button_pin)
    try:
        if button_state == GPIO.LOW:
            print("Button pressed")
            voice_to_text()
            
            text = "Suneel, your love life so terrible that even AI girlfriends will not date you."
            path = "/home/aipi/Desktop/leaflink/sounds/"
            mp3_file = "output"
            counter = str(1)
            # clone_voice_jared(text, path, mp3_file, counter)
            
            classification_1 = "plant action"
            if classification_1 == "plant action":
                classify_2 = 4
                if classify_2 == 1: # fertilizer
                    operate_motor()
                    text = "I was very hungry. Thank you for feeding me!"
                    clone_voice_jared(text, path, mp3_file, counter)
                elif classify_2 == 2: # turn lights on
                    lights_on()
                    text = "I can finally see! Thank you for the wonderful light!"
                    clone_voice_jared(text, path, mp3_file, counter)
                elif classify_2 == 3: # turn lights off
                    lights_off()
                    text = "Who turned the lights off? I don't like the dark!"
                    clone_voice_jared(text, path, mp3_file, counter)
                elif classify_2 == 4:
                    pump_water()
                    text = "That drink hit the spot. Thank you!"
                    clone_voice_jared(text, path, mp3_file, counter)
                    
    except:
        pass
    
    # keep track of time
    if datetime.now().strftime("%Y-%m-%d %H:%M:%S")[-1] == "8":
        print(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        sleep(1)
    
    # occurs at 10 seconds after minute
    # opereate fertilizer 
    if datetime.now().strftime("%Y-%m-%d %H:%M:%S")[-2:] == "10":
        try:
            operate_motor()
        finally:
            sleep(1)
        
    # occurs 20 seconds after minute
    # operate lights
    if datetime.now().strftime("%Y-%m-%d %H:%M:%S")[-2:] == "20":
        try:
            light_state = GPIO.input(light_pin)
            if light_state == GPIO.LOW:
                lights_off()
                print("Turn lights off")
            else:
                lights_on()
                print("Turn lights on")
        finally:
            sleep(1)
    
    # occurs 30 seconds after minute
    # operate lights
    if datetime.now().strftime("%Y-%m-%d %H:%M:%S")[-2:] == "30":
        try:
            moisture_level = chan_0.value
            if moisture_level > 21024:
                pump_water()
                print("Pumped water")
            else:
                print("Didn't pump water")
        finally:
            sleep(1)
    
    # occurs at bottom of minute
    # write sensor data to csv
    if datetime.now().strftime("%Y-%m-%d %H:%M:%S")[-2:] == "00":

        # record data
        # csv file
        filename = "plant_data.csv"
        file_exists = os.path.isfile(filename)
        with open(filename, "a", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            if not file_exists:
                csvwriter.writerow(["date_time", "temperature_c", "temperature_f",
                                    "humidity", "soil_moisture", "light"])
                
            try:
                # time
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    
                # temp/humid
                temp_c, temp_f, humid = get_temp_humid(dht_device)
                temp_f = int(temp_f)
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
                    print("High light")
                else:
                    print("Low light")
                        
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
                time.sleep(1)
