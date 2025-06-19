# model/sensors.py
import RPi.GPIO as GPIO
import spidev
from config.pins import *

class SensorManager:
    def __init__(self):
        # GPIO 설정
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIR_SENSOR_PIN, GPIO.IN)
        
        # SPI 초기화 (MCP3008)
        self.spi = spidev.SpiDev()
        self.spi.open(SPI_BUS, SPI_DEVICE)
        self.spi.max_speed_hz = SPI_MAX_SPEED
        
    def read_adc(self, channel):
        """MCP3008에서 ADC 값 읽기"""
        if channel < 0 or channel > 7:
            return -1
        r = self.spi.xfer2([1, (8 + channel) << 4, 0])
        adc_val = ((r[1] & 3) << 8) + r[2]
        return adc_val
    
    def get_pir_value(self):
        """PIR 센서 값 반환 (0 또는 1)"""
        return GPIO.input(PIR_SENSOR_PIN)
    
    def is_motion_detected(self):
        """움직임 감지 여부"""
        return self.get_pir_value() == 1
    
    def get_light_value(self):
        """조도 센서 ADC 값 반환 (0-1023)"""
        return self.read_adc(LIGHT_SENSOR_CH)
    
    def is_dark(self):
        """어두운지 판정 (임계값 이하면 어두움)"""
        return self.get_light_value() < LIGHT_DARK_THRESHOLD
    
    def cleanup(self):
        """리소스 정리"""
        self.spi.close()
        GPIO.cleanup()

# 전역 센서 매니저 인스턴스
_sensor_manager = None

def get_sensor_manager():
    """센서 매니저 싱글톤 인스턴스 반환"""
    global _sensor_manager
    if _sensor_manager is None:
        _sensor_manager = SensorManager()
    return _sensor_manager

# 하위 호환성을 위한 래퍼 함수들
def get_pir_value():
    return get_sensor_manager().get_pir_value()

def is_motion_detected():
    return get_sensor_manager().is_motion_detected()

def get_light_value():
    return get_sensor_manager().get_light_value()

def is_dark():
    return get_sensor_manager().is_dark()