# model/sensors.py
import RPi.GPIO as GPIO  # 라즈베리파이 GPIO 제어
import spidev            # SPI 통신(MCP3008용)
from config.pins import *  # 핀/상수 일괄 import

class SensorManager:
    def __init__(self):
        # GPIO 모드 설정 (BCM)
        GPIO.setmode(GPIO.BCM)
        # PIR 센서 핀 입력으로 설정
        GPIO.setup(PIR_SENSOR_PIN, GPIO.IN)
        
        # SPI 초기화 (MCP3008 ADC)
        self.spi = spidev.SpiDev()
        self.spi.open(SPI_BUS, SPI_DEVICE)
        self.spi.max_speed_hz = SPI_MAX_SPEED
        
    def read_adc(self, channel):
        """MCP3008에서 ADC 값 읽기 (0~7채널)"""
        if channel < 0 or channel > 7:
            return -1
        r = self.spi.xfer2([1, (8 + channel) << 4, 0])  # SPI 전송
        adc_val = ((r[1] & 3) << 8) + r[2]  # 10비트 값 추출
        return adc_val
    
    def get_pir_value(self):
        """PIR 센서 값 반환 (0: 없음, 1: 감지)"""
        return GPIO.input(PIR_SENSOR_PIN)
    
    def is_motion_detected(self):
        """움직임 감지 여부 (True/False)"""
        return self.get_pir_value() == 1
    
    def get_light_value(self):
        """조도 센서 ADC 값 반환 (0~1023)"""
        return self.read_adc(LIGHT_SENSOR_CH)
    
    def is_dark(self):
        """어두운지 판정 (임계값 이하면 True)"""
        return self.get_light_value() < LIGHT_DARK_THRESHOLD
    
    def cleanup(self):
        """SPI, GPIO 등 리소스 정리"""
        self.spi.close()
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

def get_light_value():
    return get_sensor_manager().get_light_value()

def is_dark():
    return get_sensor_manager().is_dark()