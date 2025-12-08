from machine import Pin, SoftI2C
import ssd1306 # display driver
from array import array

class Display:
    """Handle the OLED Display"""
    def __init__(self, a, c, x=128, y=64):
        """Initialize I2C pins and the display"""
        i2c = SoftI2C(sda=Pin(a), scl=Pin(c))
        self.display = ssd1306.SSD1306_I2C(x, y, i2c)
    
    def text(self, msg, x, y, color=1):
        """Create message at x,y coordinate"""
        self.display.text(msg, x, y, color)
    
    def draw_polygon(self, coordinates):
        """Draw Polygon at x,y coordinate using coordinates [x1,y1,x2,y3,x4,y4...]"""
        coords = array('h', coordinates)
        self.display.poly(30, 30, coords, 1)

    def draw_ellipse(self, x, y, xr, yr, color=1):
        """Draw ellipse at x,y coordinate with the radii of xr, and yr"""
        self.display.ellipse(x, y, xr, yr, color)

    def draw_rectangle(self, x, y, width, height, color=1):
        """Draw a rectangle at x,y of a certain width and height"""
        self.display.rect(x, y, width, height, color)
        
    def fill_rect(self, x, y, width, height, color=1):
        self.display.fill_rect(x, y, width, height, color)

    def line(self, x, y, x2, y2, color=1):
        """Draw a line with starting points x,y and ending points x2, y2"""
        self.display.line(x, y, x2, y2, color)


    def show(self):
        """Show all created items on the display"""
        self.display.show()
    
    def clear(self):
        """Clear the display"""
        self.display.fill(0)


class ScrollingText:
    """Continuously scrolls text across a screen."""
    def __init__(self, text, y=0, screen_width=128, speed=1):
        self.text = text
        self.x = screen_width # start off-screen
        self.y = y
        self.screen_width = screen_width
        self.speed = speed

    def draw_on(self, display):
        """Put text on display and shift it to the left."""
        display.text(self.text, self.x, self.y)
        self.x -= self.speed
        if self.x <= -len(self.text) * 8: # 8 is the default font size
            self.x = self.screen_width

def scroll_text(display, text):
    """Scroll text across the screen in a while loop"""
    s = ScrollingText(text)
    while True:
        display.clear()
        s.draw_on(display)
        display.show()

def display_scroll(s, display):
    """Perform one update of the sliding display"""
    display.clear()
    s.draw_on(display)
     
dis = Display(22, 23)
dis.text('Hello, World!', 0, 0)

