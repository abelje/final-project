from machine import Pin,ADC, Timer
from led import Led
from machine import ADC, Pin

class Photoresistor:
    def __init__(self, adc_pin, delay=50, timer_id=1):
        self.adc = ADC(Pin(adc_pin))
        self.adc.atten(ADC.ATTN_11DB)
        self.adc.width(ADC.WIDTH_10BIT)
        
        self.led = None
        self.delay = delay
        self.timer = Timer(timer_id)
        self.running= False
    
    def start_dim(self, led):
        print("started!")
        self.led = led
        self.running = True
        self.timer.init(period=self.delay, callback=self._update)
        
    def stop_dim(self):
        self.running = False
        self.timer.deinit()    
    
    def _update(self, timer):
        if self.running:
            value = self.adc.read()
            self.led.brightness(value / 1023)
        
    def deinit(self):
        self.stop_dim()
        self.led = None
        self.adc = None

    def read(self):
        return self.adc.read()

        
if __name__ == '__main__':
    led = Led(25)
    resistor = Photoresistor(13)
    resistor.start_dim(led)

