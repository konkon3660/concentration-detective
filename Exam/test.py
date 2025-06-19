# test.py
import RPi.GPIO as GPIO
import time
from smbus import SMBus
import os

# GPIO 핀 번호 설정
LIGHT_SENSOR_PIN = 17       # 조도 센서
PIR_SENSOR_PIN = 27         # 인체 감지 센서
BUTTON_PIN = 22             # 버튼
BUZZER_PIN = 18             # 부저
I2C_LCD_ADDR = 0x27         # LCD 주소 (일반적으로 0x27 또는 0x3f)

GPIO.setmode(GPIO.BCM)
GPIO.setup(LIGHT_SENSOR_PIN, GPIO.IN)
GPIO.setup(PIR_SENSOR_PIN, GPIO.IN)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# LCD 테스트 함수
def test_lcd(bus):
    try:
        # I2C 통신이 열리는지만 확인
        bus.write_byte(I2C_LCD_ADDR, 0x00)
        print("[LCD] 연결 성공")
    except Exception as e:
        print(f"[LCD] 연결 실패: {e}")

# 메인 테스트 루프
def main():
    print("부품 연결 테스트를 시작합니다. (Ctrl+C로 종료)")
    bus = SMBus(1)

    try:
        test_lcd(bus)
        while True:
            light_state = GPIO.input(LIGHT_SENSOR_PIN)
            pir_state = GPIO.input(PIR_SENSOR_PIN)
            button_state = GPIO.input(BUTTON_PIN)

            print(f"[조도센서] {'어두움' if light_state == 0 else '밝음'}")
            print(f"[PIR센서] {'사람 감지됨' if pir_state == 1 else '감지 안됨'}")
            print(f"[버튼] {'눌림' if button_state == 0 else '안 눌림'}")

            # 부저로 소리 테스트
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            time.sleep(0.1)
            GPIO.output(BUZZER_PIN, GPIO.LOW)

            time.sleep(1)

    except KeyboardInterrupt:
        print("테스트를 종료합니다.")
    finally:
        GPIO.cleanup()
        bus.close()

if __name__ == "__main__":
    main()
