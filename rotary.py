from machine import Pin, Timer
from micropython import schedule

class DebouncedSwitch:
    """Tolerates mechanical vibrations of a switch and calls the given
    callback after the switch has settled down.
    """
    def __init__(self, pin_num, callback, delay=50, timer_id=0):
        self.pin = Pin(pin_num, Pin.IN)
        self.callback = callback
        self.delay = delay
        self.timer = Timer(timer_id)
        self.timer.deinit()
        
        # 1. recognize first button press
        self.pin.irq(self.start_timer, trigger=Pin.IRQ_FALLING)
        
    def start_timer(self, pin):
        self.pin.irq(None) # disable irq to ignore any bounces
        # 2. Set up waiting period
        self.timer.init(period=self.delay, callback=self.timer_wakeup)
        
    def timer_wakeup(self, timer):
        # 3. Wake up and check if
        timer.deinit() # stop timer
        if not self.pin.value(): # true if stabilized
            # 4. Call handler once (we must use schedule to call our function if within an irq)
            schedule(self.callback, self.pin)
            
        # 5. Go back to step 1
        self.pin.irq(self.start_timer, trigger=Pin.IRQ_FALLING)

class RotaryEncoder:
    """Models a rotating dial and calls the given callback when a full 'click' has
    taken place. The value passed to callback will be +1 for clockwise and -1 for counter-clockwise."""

    # states
    START = const(0)
    CW1 = const(1)
    CW2 = const(2)
    CW3 = const(3)
    CCW1 = const(4)
    CCW2 = const(5)
    CCW3 = const(6)
    STATE_MASK = const(0x7)

    # direction data
    DIR_CW = const(0x10)
    DIR_CCW = const(0x20)
    DIR_MASK = const(0x30)

    # transition table for state machine
    # assumes CLK/DT = 11 for the starting state
    table = [
        # input CLK/DT
        # 00   01    10     11
        [START, CW1, CCW1, START], # START
        [CW2, CW1, START, START], # CW1
        [CW2, CW1, CW3, START], # CW2
        [CW2, START, CW3, START | DIR_CW], # CW3
        [CCW2, START, CCW1, START], # CCW1
        [CCW2, CCW3, CCW1, START], # CCW2
        [CCW2, CCW3, START, START | DIR_CCW] # CCW3
    ]

    def __init__(self, clk, dt, callback):
        self.clk = Pin(clk, Pin.IN)
        self.clk.irq(handler=self._update_state)
        self.dt = Pin(dt, Pin.IN)
        self.dt.irq(handler=self._update_state)

        self.callback = callback
        self.state = START

    def _update_state(self, pin):
        # encode pin state as binary number CLK/DT
        clk_dt = self.clk.value() << 1 | self.dt.value()

        # update state
        self.state = self.table[self.state & STATE_MASK][clk_dt]

        # see if a full click happened, if so call back
        direction = self.state & DIR_MASK
        if direction == DIR_CW:
            schedule(self.callback, +1)
        elif direction == DIR_CCW:
            schedule(self.callback, -1)

        # remove direction bits from state
        self.state &= STATE_MASK

def print_clk_dt(pin):
    print(f"{clk.value()}{dt.value()}")
        
if __name__ == '__main__':        
    # change pin numbers to yours
    clk = Pin(5, Pin.IN)
    dt = Pin(18, Pin.IN)

    clk.irq(handler=print_clk_dt)
    dt.irq(handler=print_clk_dt)