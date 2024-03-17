import RPi.GPIO as GPIO

BUTTON = 14
RED_LED = 15

def button_changed(button):
    if GPIO.input(button) == GPIO.LOW:
        print("Button pressed.")
        GPIO.output(RED_LED, GPIO.HIGH)
    else:
        print("Button released.")
        GPIO.output(RED_LED, GPIO.LOW)

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.output(RED_LED, GPIO.LOW)
GPIO.add_event_detect(BUTTON, GPIO.BOTH, callback=button_changed, bouncetime=10)
print("Press CTRL-C to exit.")
try:
    while True:
        pass
finally:
    GPIO.cleanup()