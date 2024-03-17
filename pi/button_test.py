import RPi.GPIO as GPIO
import Relay
import signal
import sys

BUTTON = 14
RED_LED = 15

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    GPIO.cleanup()
    sys.exit(0)

def button_changed(button):
    if GPIO.input(button) == GPIO.LOW:
        print("Button pressed.")
        Relay.relay_on()
        GPIO.output(RED_LED, GPIO.HIGH)
    else:
        Relay.relay_off()
        print("Button released.")
        GPIO.output(RED_LED, GPIO.LOW)

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.output(RED_LED, GPIO.LOW)
GPIO.add_event_detect(BUTTON, GPIO.BOTH, callback=button_changed, bouncetime=10)

signal.signal(signal.SIGINT, signal_handler)
print("Press CTRL-C to exit.")
signal.pause()