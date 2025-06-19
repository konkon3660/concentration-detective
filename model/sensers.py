#조도, PIR 입력 처리
import RPi.GPIO as GPIO
import time

# 핀 설정 (변수로 구성하여 쉽게 변경 가능)
PIR_PIN = 17
LDR_PIN = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(LDR_PIN, GPIO.IN)

def is_motion_detected():
    return GPIO.input(PIR_PIN)

def is_dark():
    return GPIO.input(LDR_PIN) == 0  # 0이면 어두운 것으로 간주
