import RPi.GPIO as GPIO
import time

# 핀 번호 설정
LIGHT_SENSOR_PIN = 17
PIR_SENSOR_PIN = 27
BUTTON_PIN = 22
BUZZER_PIN = 18
LED_PIN = 23

# GPIO 초기화
GPIO.setmode(GPIO.BCM)
GPIO.setup(LIGHT_SENSOR_PIN, GPIO.IN)
GPIO.setup(PIR_SENSOR_PIN, GPIO.IN)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(LED_PIN, GPIO.OUT)

print("\n✅ 센서 연결 테스트 시작 (Ctrl+C로 종료)\n")

try:
    while True:
        light = GPIO.input(LIGHT_SENSOR_PIN)
        pir = GPIO.input(PIR_SENSOR_PIN)
        button = GPIO.input(BUTTON_PIN)

        print(f"[조도] {'밝음' if light else '어두움'}", end=' | ')
        print(f"[PIR] {'감지됨' if pir else '없음'}", end=' | ')
        print(f"[버튼] {'눌림' if button == 0 else '안 눌림'}")

        # 조도 센서: 어두우면 LED 켜기
        GPIO.output(LED_PIN, GPIO.LOW if light else GPIO.HIGH)

        # 버튼 누르면 부저 울림
        if button == 0:
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            time.sleep(0.1)
            GPIO.output(BUZZER_PIN, GPIO.LOW)

        time.sleep(0.5)
except KeyboardInterrupt:
    print("\n종료합니다.")
finally:
    GPIO.cleanup()
