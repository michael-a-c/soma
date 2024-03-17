import requests
import time

CONST_ESP32_IP = "192.168.0.105"
CONST_ESP32_RELAY_PIN = 15
ESP32_URL = f'http://{CONST_ESP32_IP}/digital/{CONST_ESP32_RELAY_PIN}'

print("Relay On Request")
response = requests.get(f'{ESP32_URL}/1')
print(f"On:{response.status_code}")

time.sleep(0.5)

print("Relay Off Request")
response = requests.get(f'{ESP32_URL}/0')
print(f"Off:{response.status_code}")