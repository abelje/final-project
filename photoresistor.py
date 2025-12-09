from machine import Pin,PWM,ADC, reset
from led import Led
import time
import uasyncio as asyncio
from machine import ADC, Pin

class Photoresistor:
    def __init__(self, adc_pin, led=None):
        self.led = led
        self.adc = ADC(Pin(adc_pin))
        self.adc.atten(ADC.ATTN_11DB)
        self.adc.width(ADC.WIDTH_10BIT)

    def read(self):
        return self.adc.read()

    def duty(self, value):
        self.led.brightness(value)

    def deinit(self):
        self.led.deinit()
        
    def dim(self):
        try:
            while True:
                adcValue = resistor.read()/1000
                resistor.duty(adcValue)
        finally:
            resistor.deinit()
        
if __name__ == '__main__':
    try:
        led = Led(25)
        resistor = Photoresistor(13, led)
        while True:
            adcValue = resistor.read()/1000
            resistor.duty(adcValue)
            print(resistor.read()/1000)
            time.sleep_ms(100)

    except:
        resistor.deinit()

