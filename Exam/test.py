import RPi.GPIO as GPIO
import time

# GPIO 핀 번호 설정 (원하는 핀으로 수정 가능)
LIGHT_SENSOR_PIN = 17     # 조도 센서
PIR_SENSOR_PIN = 27       # 인체 감지 센서
BUTTON_PIN = 22           # 버튼
BUZZER_PIN = 18           # 부저

# 초기화
GPIO.setmode(GPIO.BCM)
GPIO.setup(LIGHT_SENSOR_PIN, GPIO.IN)
GPIO.setup(PIR_SENSOR_PIN, GPIO.IN)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

def main():
    print("▶ 부품 연결 테스트 시작 (Ctrl+C로 종료)")
    try:
        while True:
            light = GPIO.input(LIGHT_SENSOR_PIN)
            pir = GPIO.input(PIR_SENSOR_PIN)
            button = GPIO.input(BUTTON_PIN)

            print(f"[조도 센서] 상태: {'밝음' if light else '어두움'}")
            print(f"[PIR 센서] 상태: {'감지됨' if pir else '없음'}")
            print(f"[버튼] 상태: {'눌림' if button == 0 else '안 눌림'}")

            # 부저로 테스트 비프음
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            time.sleep(0.1)
            GPIO.output(BUZZER_PIN, GPIO.LOW)

            time.sleep(1)
            print("-" * 30)

    except KeyboardInterrupt:
        print("▶ 테스트 종료")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
