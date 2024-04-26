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
from src.numeric_input import *
import requests

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

url = "https://suneeln-duke-leaflink-ask.hf.space/ask"

path = "/home/aipi/Desktop/leaflink/sounds/"
mp3_file = "output"
counter = str(1)

orient_motor()


# Master Loop
while True:
    # speech
    button_state = GPIO.input(button_pin)
    try:
        if button_state == GPIO.LOW:
            print("Button pressed\n\n")
            
            # options for when room is too loud
            print("Press one of the following on keyboard:")
            print("1. Speak to the plant")
            print("2. Water the plant")
            print("3. Give the plant light (only at the end of the demonstration)")
            print("4. Turn off the lights")
            print("5. Feed the plant some fertilizer")
            print("6. Ask the plant about the high and low temperature in the data this year, as well as their difference")
            print("7. Ask the plant to tell about the optimal sunlight it should receive")
            print("8. Ask the plant about it's latin name and natural habitat")
            print("9. Ask the plant to help with your calculus homework and give the derivative of x cubed")
            num = get_numeric_input("Enter a number: ")
            
            if num == 2:
                pump_water()
                text = "That drink hit the spot. Thank you!"
                clone_voice_jared(text, path, mp3_file, counter)
            elif num == 3:
                lights_on()
                text = "I can finally see! Thank you for the wonderful light!"
                clone_voice_jared(text, path, mp3_file, counter)
            elif num == 4:
                lights_off()
                text = "Who turned the lights off? I don't like the dark!"
                clone_voice_jared(text, path, mp3_file, counter)
            elif num == 5:
                operate_motor()
                text = "I was very hungry. Thank you for feeding me!"
                clone_voice_jared(text, path, mp3_file, counter)
            elif num >= 6 and num <= 9:
                if num == 6:
                    entry = "What is the high and low temperature in the data this year, as well as their difference?"
                elif num == 7:
                    entry = "What is the optimal sunlight you should receive?"
                elif num == 8:
                    entry = "What is your latin name and natural habitat?"
                elif num == 9:
                    entry = "Help me with my calculus homework and give me the derivative of x cubed"
                
                # api call
                resp = requests.post(
                    url, params = {
                        "question": entry
                    }
                )
                
                # print api call response
                print(resp.json())
            
                if resp.status_code == 200:
                    resp = resp.json()
                else:
                    resp = "Error"
                
                # respond
                if resp['category_number'] > 1:
                    text = resp['response']
                    
                    clone_voice_jared(text, path, mp3_file, counter)
                
            elif num == 1:    
                # speech in
                speech = voice_to_text()
                
                # api call
                resp = requests.post(
                    url, params = {
                        "question": speech
                    }
                )
                
                # print api call response
                print(resp.json())
                
                if resp.status_code == 200:
                    resp = resp.json()
                else:
                    resp = "Error"
                
                # respond
                if resp['category_number'] > 1:
                    text = resp['response']
                    
                    clone_voice_jared(text, path, mp3_file, counter)
                else:
                    plant_category = resp['plant_category']
                    
                    if plant_category == 0: # fertilizer
                        operate_motor()
                        text = "I was very hungry. Thank you for feeding me!"
                        clone_voice_jared(text, path, mp3_file, counter)
                        
                    elif plant_category == 1: # turn lights on
                        lights_on()
                        text = "I can finally see! Thank you for the wonderful light!"
                        clone_voice_jared(text, path, mp3_file, counter)
                    
                    elif plant_category == 2: # turn lights off
                        lights_off()
                        text = "Who turned the lights off? I don't like the dark!"
                        clone_voice_jared(text, path, mp3_file, counter)
                    
                    elif plant_category == 3:
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

