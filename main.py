# idea: Have 3 lights that can be controlled by the website to
# 3 rooms in this house. Make the leds controllable with the rotary
# encoder and on the webpage. Have the current brightness in the room
# display on the oled and on the webpage.
# Have brightness be controllable with the rotary encoder

from led import Led, RGBLed
from microdot import Microdot
from wifi import Wifi
from machine import Pin, ADC
from time import sleep_ms
import json

# button to change area to affect physically
button = Pin(11, Pin.IN, Pin.PULL_UP)
pressed = False

# leds
red_Led = Led(25)
blue_Led = Led(32)
rgb_Led = RGBLed(7, 8, 15)

wifi = Wifi("WarriorNET", "VictorEWarrior2023")
wifi.connect('172.16.37.27')
port = 5000

try:
    app = Microdot()

    @app.get('/')
    async def index(request):
        ipaddr = wifi.get_ip_addr()
        with open('index.html', 'r') as f:
            text = f.read().replace('ADDRESS', f'{ipaddr}:{port}')
            return text, {'Content-Type': 'text/html'}
        
    @app.get('/area')
    async def change_area(request, ws):
        while True:
            data = await ws.receive()
            print(data)
            d = json.loads(data)
            if (d['area'] == 'rgb'):
                red = max(0, min(1, d['red'] / 100))
                green = max(0, min(1, d['green'] / 100))
                blue = max(0, min(1, d['blue'] / 100))
                rgb_Led.set_color(red, green, blue)
            if (d['area'] == 'red'):
                red_Led.brightness(d['redLed'])

finally:
    rgb_Led.deinit()
    red_Led.deinit()
    blue_Led.deinit()