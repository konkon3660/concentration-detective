# model/actuators.py
import RPi.GPIO as GPIO  # 라즈베리파이 GPIO 제어
from config.pins import LED_PIN, BUZZER_PIN  # 핀 번호 상수

class ActuatorManager:
    def __init__(self):
        # GPIO 모드 설정 (BCM)
        GPIO.setmode(GPIO.BCM)
        # LED, 부저 핀 출력으로 설정
        GPIO.setup(LED_PIN, GPIO.OUT)
        GPIO.setup(BUZZER_PIN, GPIO.OUT)
        
        # 부저 PWM 객체 생성 (262Hz: 도 음)
        self.buzzer_pwm = GPIO.PWM(BUZZER_PIN, 262)
        self.led_state = False      # LED 상태 저장
        self.buzzer_state = False   # 부저 상태 저장
    
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
        """부저 켜기 (PWM)"""
        self.buzzer_pwm.start(duty_cycle)
        self.buzzer_state = True
    
    def buzzer_off(self):
        """부저 끄기"""
        self.buzzer_pwm.stop()
        self.buzzer_state = False
    
    def buzzer_beep(self, duration=1.0, duty_cycle=50.0):
        """부저를 일정 시간(초) 울리기"""
        import time
        self.buzzer_on(duty_cycle)
        time.sleep(duration)
        self.buzzer_off()
    
    def buzzer_continuous_on(self):
        """부저를 계속 울리게 하기"""
        self.buzzer_on(50.0)
    
    def cleanup(self):
        """GPIO 및 리소스 정리"""
        self.buzzer_off()
        self.led_off()
        GPIO.cleanup()

# 전역 액츄에이터 매니저 인스턴스 (싱글톤)
_actuator_manager = None

def get_actuator_manager():
    """액츄에이터 매니저 싱글톤 인스턴스 반환"""
    global _actuator_manager
    if _actuator_manager is None:
        _actuator_manager = ActuatorManager()
    return _actuator_manager

# 하위 호환성 및 간편 사용을 위한 래퍼 함수들
def led_on():
    get_actuator_manager().led_on()

def led_off():
    get_actuator_manager().led_off()

def buzzer_on():
    get_actuator_manager().buzzer_on()

def buzzer_off():
    get_actuator_manager().buzzer_off()

def buzzer_continuous_on():
    get_actuator_manager().buzzer_continuous_on()