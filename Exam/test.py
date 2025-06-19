import RPi.GPIO as GPIO
import spidev  # 아날로그 센서용 SPI
import time

# GPIO 핀 번호
PIR_SENSOR_PIN = 27
BUTTON_PIN = 22
BUZZER_PIN = 18

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_SENSOR_PIN, GPIO.IN)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# SPI 설정 (MCP3008)
spi = spidev.SpiDev()
spi.open(0, 0)  # Bus 0, Device 0
spi.max_speed_hz = 1350000

# MCP3008 채널에서 아날로그 값 읽기 (0~1023)
def read_adc(channel):
    if not 0 <= channel <= 7:
        return -1
    r = spi.xfer2([1, (8 + channel) << 4, 0])
    adc_out = ((r[1] & 3) << 8) + r[2]
    return adc_out

try:
    print("\n✅ 조도(PHOTO), PIR, 버튼, 부저 테스트 시작 (Ctrl+C로 종료)\n")
    while True:
        light_val = read_adc(0)  # MCP3008의 CH0에 연결되었다고 가정
        pir_val = GPIO.input(PIR_SENSOR_PIN)
        button_val = GPIO.input(BUTTON_PIN)

        print(f"[조도 ADC] {light_val:>4} | [PIR] {pir_val} | [버튼] {button_val}")

        if button_val == 0:
            print("→ 버튼 눌림! 부저 울림")
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            time.sleep(0.2)
            GPIO.output(BUZZER_PIN, GPIO.LOW)

        time.sleep(0.5)

except KeyboardInterrupt:
    print("\n테스트 종료")
finally:
    spi.close()
    GPIO.cleanup()
