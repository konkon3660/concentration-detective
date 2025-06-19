import RPi.GPIO as GPIO
import spidev
import time

# GPIO 핀 설정
PIR_SENSOR_PIN = 27
BUZZER_PIN = 18
LED_PIN = 23

# GPIO 초기화
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_SENSOR_PIN, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(LED_PIN, GPIO.OUT)

# SPI 초기화 (MCP3008)
spi = spidev.SpiDev()
spi.open(0, 0)  # Bus 0, Device 0
spi.max_speed_hz = 1350000

def read_adc(channel):
    if channel < 0 or channel > 7:
        return -1
    r = spi.xfer2([1, (8 + channel) << 4, 0])
    adc_val = ((r[1] & 3) << 8) + r[2]
    return adc_val

print("\n✅ 센서/출력 테스트 시작 (Ctrl+C로 종료)\n")

try:
    while True:
        # 센서 읽기
        light_val = read_adc(0)  # 조도센서: CH0
        pir_val = GPIO.input(PIR_SENSOR_PIN)

        # 값 출력
        print(f"[조도센서] {light_val:>4} | [PIR센서] {pir_val} (1:감지, 0:없음)")

        # LED 깜빡이기
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(LED_PIN, GPIO.LOW)

        # 부저 울리기
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(BUZZER_PIN, GPIO.LOW)

        # 센서 간 딜레이
        time.sleep(0.35)

except KeyboardInterrupt:
    print("\n테스트 종료")
finally:
    spi.close()
    GPIO.cleanup()
