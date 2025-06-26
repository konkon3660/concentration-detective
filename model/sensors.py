# model/sensors.py
import RPi.GPIO as GPIO  # 라즈베리파이 GPIO 제어
from config.pins import PIR_SENSOR_PIN  # 핀/상수 일괄 import

class SensorManager:
    def __init__(self):
        # GPIO 모드 설정 (BCM)
        GPIO.setmode(GPIO.BCM)
        # PIR 센서 핀 입력으로 설정
        GPIO.setup(PIR_SENSOR_PIN, GPIO.IN)
        
    def get_pir_value(self):
        """PIR 센서 값 반환 (0: 없음, 1: 감지)"""
        return GPIO.input(PIR_SENSOR_PIN)
    
    def is_motion_detected(self):
        """움직임 감지 여부 (True/False)"""
        return self.get_pir_value() == 1
    
    def cleanup(self):
        """GPIO 등 리소스 정리"""
        GPIO.cleanup()

# 전역 센서 매니저 인스턴스 (싱글톤)
_sensor_manager = None

def get_sensor_manager():
    """센서 매니저 싱글톤 인스턴스 반환"""
    global _sensor_manager
    if _sensor_manager is None:
        _sensor_manager = SensorManager()
    return _sensor_manager

# 하위 호환성 및 간편 사용을 위한 래퍼 함수들
def get_pir_value():
    return get_sensor_manager().get_pir_value()

def is_motion_detected():
    return get_sensor_manager().is_motion_detected()