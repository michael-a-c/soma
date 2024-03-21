import RPi.GPIO as GPIO
import signal
import sys
import logging
logging.basicConfig(level = logging.DEBUG)

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

    signal.signal(signal.SIGINT, signal_handler)
    logging.info("Press CTRL-C to exit.")
    signal.pause()