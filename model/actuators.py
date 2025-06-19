# actuators.py
import RPi.GPIO as GPIO

LED_PIN = 22
BUZZER_PIN = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# 부저 PWM 객체
pwm = GPIO.PWM(BUZZER_PIN, 262)  # 도 음 높이

def led_on():
    GPIO.output(LED_PIN, True)

def led_off():
    GPIO.output(LED_PIN, False)

def buzzer_on():
    pwm.start(50.0)  # duty cycle 50%

def buzzer_off():
    pwm.stop()
