import adafruit_dht, time, board
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

SENSOR_PIN = 26

SENSOR_TYPE = adafruit_dht.DHT11(board.D26, use_pulseio=False)

def read_temp_hum():
    # humidity, temperature = Adafruit_DHT.read_retry(SENSOR_TYPE, SENSOR_PIN)

    # humidity, temperature = adafruit_dht.read_retry(SENSOR_TYPE, SENSOR_PIN)

    # humidity, temperature = SENSOR_TYPE.humidity(), SENSOR_TYPE.temperature

    humidity, temperature = SENSOR_TYPE.humidity, SENSOR_TYPE.temperature

    if humidity is not None and temperature is not None:
        print(f"Humidity: {humidity} | temperature: {temperature}")

    else:
        print("The appocalypse is upon us")


try:
    while True:
        read_temp_hum()
        time.sleep(2)
except Exception as e:
    print(e)

GPIO.cleanup()