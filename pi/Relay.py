import requests

CONST_ESP32_IP = "192.168.0.105"
CONST_ESP32_RELAY_PIN = 15
ESP32_URL = f'http://{CONST_ESP32_IP}/digital/{CONST_ESP32_RELAY_PIN}'

def relay_on():
    print("Relay: On Request")
    response = requests.get(f'{ESP32_URL}/1')
    print(f"Relay: On={response.status_code}")

def relay_off():
    print("Relay: Off Request")
    response = requests.get(f'{ESP32_URL}/0')
    print(f"Relay: off={response.status_code}")
