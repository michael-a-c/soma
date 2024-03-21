import RPi.GPIO as GPIO
import signal
import sys
import logging

FN1_PIN = 12
FN2_PIN = 16
FN3_PIN = 20
FN4_PIN = 21
FN5_PIN = 26
SEL_PIN = 19

class Btn: 
    def __init__(self, pin, name):
        self.name = name
        self.pin = pin
        logging.info(f"Created button with pin={self.pin} name={self.name}")
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.pin, GPIO.BOTH, callback=self.onchange, bouncetime=10)

    def onchange(self, pin):
        if GPIO.input(pin) == GPIO.LOW:
            logging.info(f"Button {self.name}, pin={pin} OFF.")
        else:
            logging.info(f"Button {self.name}, pin={pin} ON.")

def signal_handler(sig, frame):
    logging.critical('Exiting, cleaning up pins')
    GPIO.cleanup()
    sys.exit(0)

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    fn1 = Btn(FN1_PIN, "Func1")
    fn2 = Btn(FN2_PIN, "Func2")
    fn3 = Btn(FN3_PIN, "Func3")
    fn4 = Btn(FN4_PIN, "Func4")
    fn5 = Btn(FN5_PIN, "Func5")
    sel = Btn(SEL_PIN, "Selector")

    signal.signal(signal.SIGINT, signal_handler)
    logging.info("Press CTRL-C to exit.")
    signal.pause()