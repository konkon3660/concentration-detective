# led, 부저 출력 처리
import RPi.GPIO as GPIO

# 핀 설정
LED_PIN = 22
BUZZER_PIN = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setwarnings(False)

pwm = GPIO.PWM(BUZZER_PIN, 262)

def led_on():
    GPIO.output(LED_PIN, True)

def led_off():
    GPIO.output(LED_PIN, False)

def buzzer_on():
    pwm.start(50.0)

def buzzer_off():
    pwm.start(50.0)
