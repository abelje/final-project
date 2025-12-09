from led import Led, RGBLed
from microdot import Microdot
from wifi import Wifi
from machine import Pin, ADC
from time import sleep_ms
import json
from websocket import with_websocket

wifi = Wifi("WarriorNET", "VictorEWarrior2023")
wifi.connect('172.16.37.27')
port = 5000

# button to change area to affect physically
# button = Pin(14, Pin.IN, Pin.PULL_UP)
# pressed = False

# leds
red_Led = Led(25)
blue_Led = Led(32)
rgb_Led = RGBLed(18, 19, 22)

app = Microdot()

@app.get('/')
async def index(request):
    ipaddr = wifi.get_ip_addr()
    with open('index.html', 'r') as f:
        text = f.read().replace('ADDRESS', f'{ipaddr}:{port}')
        return text, {'Content-Type': 'text/html'}
     
@app.get('/area')
@with_websocket
async def change_area(request, ws):
    try:
        while True:
            data = await ws.receive()
            if data is None:
                break
            print(data)
            d = json.loads(data)

            if d['area'] == 'rgbRoom':
                if d['rgb']["red"] == -1:
                    rgb_Led.off()
                    d['rgb']["red"] = 0
                    
                red = max(0, min(1, d['rgb']['red'] / 100))
                green = max(0, min(1, d['rgb']['green'] / 100))
                blue = max(0, min(1, d['rgb']['blue'] / 100))
                rgb_Led.set_color(red, green, blue)

            elif d['area'] == 'redRoom':
                try:
                    value = red_Led.get_brightness()
                    if value > 0:
                        red_Led.off()
                    else:
                        red_Led.on()
                except Exception as e:
                    print("Error toggling red LED:", e)

            elif d['area'] == 'blueRoom':
                try:
                    value = blue_Led.get_brightness()
                    if value > 0:
                        blue_Led.off()
                    else:
                        blue_Led.on()
                except Exception as e:
                    print("Error toggling blue LED:", e)

    except Exception as e:
        print("WebSocket disconnected:", e)


app.run()
