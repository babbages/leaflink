import adafruit_dht, time, board


def get_temp_humid(dht_device):

    # read from sensor
    try:
        temp_c = dht_device.temperature
        temp_f = temp_c * (9/5) + 32
        humidity = dht_device.humidity
        return (temp_c, temp_f, humidity)
    except Exception as e:
        return (-9999, -9999, -9999)

if __name__ == "__main__":
    # setup sensor
    dht_device = adafruit_dht.DHT11(board.D26)
    
    while True:
        print(get_temp_humid(dht_device))
        time.sleep(2)