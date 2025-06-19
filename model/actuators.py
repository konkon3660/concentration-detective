# model/actuators.py
import RPi.GPIO as GPIO
from config.pins import LED_PIN, BUZZER_PIN

class ActuatorManager:
    def __init__(self):
        # GPIO 설정
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LED_PIN, GPIO.OUT)
        GPIO.setup(BUZZER_PIN, GPIO.OUT)
        
        # 부저 PWM 객체 (도 음 높이)
        self.buzzer_pwm = GPIO.PWM(BUZZER_PIN, 262)
        self.led_state = False
        self.buzzer_state = False
    
    def led_on(self):
        """LED 켜기"""
        GPIO.output(LED_PIN, True)
        self.led_state = True
    
    def led_off(self):
        """LED 끄기"""
        GPIO.output(LED_PIN, False)
        self.led_state = False
    
    def led_toggle(self):
        """LED 토글"""
        if self.led_state:
            self.led_off()
        else:
            self.led_on()
    
    def buzzer_on(self, duty_cycle=50.0):
        """부저 켜기"""
        self.buzzer_pwm.start(duty_cycle)
        self.buzzer_state = True
    
    def buzzer_off(self):
        """부저 끄기"""
        self.buzzer_pwm.stop()
        self.buzzer_state = False
    
    def buzzer_beep(self, duration=1.0, duty_cycle=50.0):
        """부저 일정 시간 울리기"""
        import time
        self.buzzer_on(duty_cycle)
        time.sleep(duration)
        self.buzzer_off()
    
    def cleanup(self):
        """리소스 정리"""
        self.buzzer_off()
        self.led_off()
        GPIO.cleanup()

# 전역 액츄에이터 매니저 인스턴스
_actuator_manager = None

def get_actuator_manager():
    """액츄에이터 매니저 싱글톤 인스턴스 반환"""
    global _actuator_manager
    if _actuator_manager is None:
        _actuator_manager = ActuatorManager()
    return _actuator_manager

# 하위 호환성을 위한 래퍼 함수들
def led_on():
    get_actuator_manager().led_on()

def led_off():
    get_actuator_manager().led_off()

def buzzer_on():
    get_actuator_manager().buzzer_on()

def buzzer_off():
    get_actuator_manager().buzzer_off()