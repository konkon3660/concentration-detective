# 공부 시간 측정
import RPi.GPIO as GPIO

# 핀 설정
LED_PIN = 22
BUZZER_PIN = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

def led_on():
    GPIO.output(LED_PIN, True)

def led_off():
    GPIO.output(LED_PIN, False)

def buzzer_on():
    GPIO.output(BUZZER_PIN, True)

def buzzer_off():
    GPIO.output(BUZZER_PIN, False)
