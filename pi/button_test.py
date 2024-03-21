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

class btn: 
    def __init__(self, pin, name):
        self.name = name
        self.pin = pin
        logging.debug(f"Created button with pin={self.pin} name={self.name}")
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
    btn(FN1_PIN, "Func1")
    btn(FN2_PIN, "Func2")
    btn(FN3_PIN, "Func3")
    btn(FN4_PIN, "Func4")
    btn(FN5_PIN, "Func5")
    btn(SEL_PIN, "Selector")

    GPIO.setmode(GPIO.BCM)
    signal.signal(signal.SIGINT, signal_handler)
    logging.info("Press CTRL-C to exit.")
    signal.pause()