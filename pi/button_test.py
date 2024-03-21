import RPi.GPIO as GPIO
import spidev as SPI
from lib import LCD_1inch69
from PIL import Image, ImageDraw, ImageFont
import signal
import sys
import logging

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
    def __init__(self, pin, name, selector):
        self.name = name  
        self.pin = pin
        self.selector=selector
        logging.info(f"Created button with pin={self.pin} name={self.name}")
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.pin, GPIO.BOTH, callback=self.onchange, bouncetime=7)

    def onchange(self, pin):
        if GPIO.input(pin) == GPIO.LOW:
            logging.info(f"Button {self.name}, pin={pin} OFF. SELECT={self.selector.get_state()}")
        else:
            logging.info(f"Button {self.name}, pin={pin} ON. SELECT={self.selector.get_state()}")

def signal_handler(sig, frame):
    disp.module_exit()
    logging.critical('Exiting, cleaning up pins')
    GPIO.cleanup()
    sys.exit(0)

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    sel = SelectorBtn(SEL_PIN)
    fn1 = Btn(FN1_PIN, "Func1", sel)
    fn2 = Btn(FN2_PIN, "Func2", sel)
    fn3 = Btn(FN3_PIN, "Func3", sel)
    fn4 = Btn(FN4_PIN, "Func4", sel)
    fn5 = Btn(FN5_PIN, "Func5", sel)

    # Initialize library.
    disp.Init()
    # Clear display.
    disp.clear()
    #Set the backlight to 100
    disp.bl_DutyCycle(50)
    Font1 = ImageFont.truetype("Font01.ttf", 35)

    logging.info("draw text")
    image1 = Image.new("RGB", (disp.width,disp.height ), "WHITE")
    draw = ImageDraw.Draw(image1)

    draw.rectangle([(20, 120), (160, 153)], fill = "BLUE")
    draw.text((25, 120), 'Hello world', fill = "RED", font=Font1)
    draw.text((0, 0), 'Hello world', fill = "RED", font=Font1)
    draw.text((3, 3), 'Hello world', fill = "RED", font=Font1)
    draw.text((15, 15), 'Hello world', fill = "RED", font=Font1)
    draw.text((25, 25), 'Hello world', fill = "RED", font=Font1)

    disp.ShowImage(image1)

    logging.info("Press CTRL-C to exit.")
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()