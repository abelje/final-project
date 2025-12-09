from machine import Pin,PWM,ADC, reset
import time

class Photoresistor:
    def __init__(self, pwm_pin, adc_pin):
        self.pwm = PWM(Pin(pwm_pin, Pin.OUT), 1000)
        self.adc = ADC(Pin(adc_pin))
        self.adc.atten(ADC.ATTN_11DB)
        self.adc.width(ADC.WIDTH_10BIT)

    def read(self):
        return self.adc.read()

    def duty(self, value):
        self.pwm.duty(value)

    def deinit(self):
        self.pwm.deinit()
        reset()

if __name__ == '__main__':
    try:
        resistor = Photoresistor(25, 13)
        while True:
            adcValue = resistor.read()
            resistor.duty(adcValue)
            print(resistor.read())
            time.sleep_ms(100)

    except:
        resistor.deinit()