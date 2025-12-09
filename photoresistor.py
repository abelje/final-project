from machine import Pin,ADC, Timer
from led import Led
from machine import ADC, Pin

class Photoresistor:
    def __init__(self, adc_pin, led, delay=50, timer_id=1):
        self.adc = ADC(Pin(adc_pin))
        self.adc.atten(ADC.ATTN_11DB)
        self.adc.width(ADC.WIDTH_10BIT)
        self.led = led
        self.delay = delay
        self.timer = Timer(timer_id)
        
        self.timer.init(period=delay, callback=self.update)

    def update(self, t):
        value = self.adc.read()
        self.led.brightness(value / 1023)

    def read(self):
        return self.adc.read()

        
if __name__ == '__main__':
    led = Led(25)
    resistor = Photoresistor(13, led)
