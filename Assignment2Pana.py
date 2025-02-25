#Menambahkan library
import network
import time
import dht
from machine import Pin
from time import sleep
import urequests

#Menghubungkan ke WiFi
SSID = "Galaxy M15"
PASSWORD = "machobay"
#URL MongoDB dan Ubidots
API_URL = "http://192.168.20.148:5000/api/dht"

#Definisi untuk terhubungan ke Wifi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    while not wlan.isconnected():
        pass

    print("terhubung wipi:", wlan.ifconfig())

connect_wifi()

#input pin sensor
sensor = dht.DHT11(Pin(26))
pir = Pin(25, Pin.IN)

#Definisi untuk data sensor
def send_data():
    try:
        sleep(2)
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        pir_value = pir.value()

        year, month, mday, hour, minute, second, _, _ = time.localtime()
        timestamp = f"{mday:02d}-{month:02d}-{year} {hour:02d}:{minute:02d}:{second:02d}"

        
        print(f"Temperature: {temp}, Humidity: {hum}, Timestamp: {timestamp}")
        if pir.value():
            print ("Gerakan kedetek bos")
        else:
            print ("Ga ada gerakan")
        time.sleep(2)

        data = {"temperature": temp, "humidity": hum, "pir_value": pir_value, "timestamp": timestamp}
        response = urequests.post(API_URL, json=data)
        print("Response:", response.content)
        response = None

    except Exception as e:
        print("Error:", e)


while True:
    send_data()
    sleep(1)
    