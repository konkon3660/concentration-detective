# sensors.py
import RPi.GPIO as GPIO

# 핀 번호 정의
PIR_PIN = 17
LDR_PIN = 27  # 추후 MCP3008으로 교체 시 여기에서 제거

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(LDR_PIN, GPIO.IN)

def get_pir_value():
    """PIR 센서 값 반환 (0 또는 1)"""
    return GPIO.input(PIR_PIN)

def is_motion_detected():
    return get_pir_value() == 1

def get_ldr_value():
    """조도 센서 디지털 값 반환"""
    return GPIO.input(LDR_PIN)

def is_dark():
    """0이면 어두운 것으로 간주"""
    return get_ldr_value() == 0
