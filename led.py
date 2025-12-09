from machine import PWM, Pin
from math import sqrt
from time import sleep_ms

class Led:
    def __init__(self, pin_num, output=True, freq=1000):
        """Variable brightness LED. Parameter output controls whether pin is
in output mode or input mode"""
        pin = Pin(pin_num, Pin.OUT) if output else Pin(pin_num, Pin.IN)
        self.output = output
        self.pwm = PWM(pin, freq)
        self.off()
        self.value = 0
        sleep_ms(10) # allow PWM hardware to stabilize

    def deinit(self):
        """Deinitialize to avoid unintended behavior"""
        self.pwm.deinit()

    def brightness(self, value):
        """Brightness value between [0, 1]"""
        if 0 <= value <= 1:
            levels =  1024
            if self.output:
                value = int((levels-1) * value**2)
            else:
                value = int((levels-1) * sqrt(1 - value))
            
            self.value = value
            self.pwm.duty(value)
        else:
            raise ValueError(f"brightness value must be within [0, 1], not {value}")
        
    def on(self):
        """Turn Led fully on"""
        self.brightness(1)

    def off(self):
        """Turn Led completely off"""
        self.brightness(0)
        
    def get_brightness(self):
        return self.value

class RGBLed:
    def __init__(self, r, g, b, freq=1000):
        """Use Led class to initialize red, green, and blue portions of the RGB Led"""
        self.leds = [Led(r, False), Led(g, False), Led(b, False)]
        self.red = 0
        self.green = 0
        self.blue = 0

    def deinit(self):
        """Safely deinitialize pins at the end of use"""
        for led in self.leds:
            led.deinit()

    def off(self):
        """Turn all three leds off"""
        for led in self.leds:
            led.off()

    def set_color(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue
        
        self.leds[0].brightness(red)
        self.leds[1].brightness(green)
        self.leds[2].brightness(blue)
        
    def get_color(self):
        return (self.red, self.green, self.blue)

class LedBar:
    def __init__(self, pins):
        """Initialize all 10 leds on the led bar"""
        self.leds = [Pin(pin, Pin.OUT) for pin in pins]

    def leds_on(self):
        """Turn the entire led bar on"""
        for led in self.leds:
            led.value(1)

    def leds_off(self):
        """Turn the entire led bar off"""
        for led in self.leds:
            led.value(0)
            
    def led_on(self, index):
        """Turn individual led from [0, 9] on"""
        self.leds[index].value(1)
        
    def led_off(self, index):
        """Turn individual led from [0, 9] off"""
        self.leds[index].value(0)
            
# pins that work [23, 22, 32, 33, 25, 26, 27, 14, 12, 13]