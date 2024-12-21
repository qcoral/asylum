import network
import time
import urequests
import machine
import st7735
import rgb

spi = machine.SPI(1, baudrate=20000000, polarity=0, phase=0)

reset = machine.Pin(15, machine.Pin.OUT)
cs = machine.Pin(16, machine.Pin.OUT)
sda = machine.Pin(6, machine.Pin.OUT)
sck = machine.Pin(4, machine.Pin.OUT)
dc = machine.Pin(11, machine.Pin.OUT)

disp = st7735.ST7735(spi, cs=cs, dc=dc, rst=reset)
disp.init()

disp.fill(rgb.RED)
disp.text("TESTING TFT DISPLAY...", 10, 10, rgb.WHITE)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("SSID", "KEY")

while not wlan.isconnected():
    print("Connecting to Wi-Fi...")
    time.sleep(1)
print("Connected to Wi-Fi!")
print("IP Address:", wlan.ifconfig()[0])

url = "https://api.open-meteo.com/v1/forecast?latitude=52.4814&longitude=-1.8998&current=temperature_2m&forecast_days=1&models=ukmo_seamless"

while True:
    response = urequests.get(url)

    if response.status_code == 200:
        data = response.json()
    else:
        print("Failed")
    
    temp = data['current']['temperature_2m']
    disp.fill(rgb.BLACK)
    disp.text(f"Current Temperature: {temp}", 10, 10, rgb.WHITE)
    response.close()
    
    time.sleep(3600)