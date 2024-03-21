import RPi.GPIO as GPIO
import spidev as SPI
from lib import LCD_1inch69
from PIL import Image, ImageDraw, ImageFont
import signal
import sys
import logging
import threading

logging.basicConfig(level = logging.DEBUG)
disp = LCD_1inch69.LCD_1inch69()

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0
device = 0

FN1_PIN = 12
FN2_PIN = 16
FN3_PIN = 20
FN4_PIN = 21
FN5_PIN = 26
SEL_PIN = 19

class SelectorBtn:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def get_state(self):
        logging.debug(f"Selector State: {GPIO.input(self.pin)}")
        return GPIO.input(self.pin)

class Btn: 
    def __init__(self, pin, name, alt_name, selector, dm, xy):
        self.name = name  
        self.alt_name = alt_name
        self.pin = pin
        self.displayManager = dm
        self.xy = xy
        self.selector=selector
        logging.debug(f"Created button with pin={self.pin} name={self.name}")
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.pin, GPIO.BOTH, callback=self.onchange, bouncetime=50)

    def onchange(self, pin):
        name = ""
        if(self.selector.get_state()):
            name = self.alt_name
        else:
            name = self.name

        if GPIO.input(pin) == GPIO.LOW:
            self.displayManager.add_text(self.xy, f"{name} \n OFF")
            logging.debug(f"Button {name}, pin={pin} OFF. SELECT={self.selector.get_state()}")
        else:
            self.displayManager.add_text(self.xy, f"{name} \n ON")
            logging.debug(f"Button {name}, pin={pin} ON. SELECT={self.selector.get_state()}")

def signal_handler(sig, frame):
    disp.module_exit()
    logging.critical('Exiting, cleaning up pins')
    GPIO.cleanup()
    sys.exit(0)


class DisplayManager():
    def __init__(self):
        # Initialize library.
        disp.Init()
        # Clear display.
        disp.clear()
        #Set the backlight to 100
        disp.bl_DutyCycle(50)
        self.font = ImageFont.truetype("Font02.ttf", 12)
        self.text_contents = {}
        logging.debug("Started Display Manager, redrawing 0.5s")

    def add_text(self, xy, text):
        logging.debug("Adding text")
        self.text_contents[xy] = text

    def draw(self):
        logging.debug(f"Drawing screen with ${len(self.text_contents.keys())}")
        image = Image.new("RGB", (disp.width,disp.height ), "WHITE")
        draw = ImageDraw.Draw(image)
            
        for xy in self.text_contents.keys():
            x,y = xy
            draw.text((x, y), self.text_contents[xy], fill = "BLACK", font=self.font)
        disp.ShowImage(image)
        
if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    dm = DisplayManager()
    threading.Timer(0.5, dm.draw).start()

    sel = SelectorBtn(SEL_PIN)
    fn1 = Btn(FN1_PIN, "FN1", "FN6",  sel, dm, (10, 10))
    fn2 = Btn(FN2_PIN, "FN2", "FN7",  sel, dm, (25, 10))
    fn3 = Btn(FN3_PIN, "FN3", "FN8",  sel, dm, (45, 10))
    fn4 = Btn(FN4_PIN, "FN4", "FN9",  sel, dm, (10, 35))
    fn5 = Btn(FN5_PIN, "FN5", "FN10", sel, dm, (30, 35))

    logging.info("Press CTRL-C to exit.")
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()