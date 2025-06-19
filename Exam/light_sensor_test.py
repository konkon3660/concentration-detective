import spidev
import time

# SPI 초기화 (MCP3008)
spi = spidev.SpiDev()
spi.open(0, 0)  # Bus 0, Device 0
spi.max_speed_hz = 1350000

def read_adc(channel):
    """MCP3008에서 ADC 값 읽기"""
    if channel < 0 or channel > 7:
        return -1
    r = spi.xfer2([1, (8 + channel) << 4, 0])
    adc_val = ((r[1] & 3) << 8) + r[2]
    return adc_val

def get_light_level(adc_value):
    """조도 레벨 판정"""
    if adc_value > 800:
        return "매우 밝음 ☀️"
    elif adc_value > 500:
        return "밝음 🌤️"
    elif adc_value > 200:
        return "보통 ⛅"
    elif adc_value > 50:
        return "어두움 🌙"
    else:
        return "매우 어두움 🌑"

print("\n💡 조도 센서 테스트 시작 (Ctrl+C로 종료)")
print("센서를 손으로 가리거나 조명을 켜고 꺼보세요!\n")
print("ADC 값 범위: 0-1023 (0=어두움, 1023=밝음)")
print("-" * 50)

try:
    max_val = 0
    min_val = 1023
    readings = []
    
    while True:
        light_val = read_adc(0)  # 조도센서: CH0에 연결
        light_level = get_light_level(light_val)
        
        # 최대/최소값 업데이트
        max_val = max(max_val, light_val)
        min_val = min(min_val, light_val)
        
        # 최근 10개 값의 평균 계산
        readings.append(light_val)
        if len(readings) > 10:
            readings.pop(0)
        avg_val = sum(readings) / len(readings)
        
        # 상태 출력
        print(f"[{time.strftime('%H:%M:%S')}] ADC: {light_val:4d} | 평균: {avg_val:6.1f} | {light_level}")
        print(f"                    최소: {min_val:4d} | 최대: {max_val:4d} | 범위: {max_val-min_val:4d}")
        print("\033[2A", end="")  # 커서를 2줄 위로 올려서 덮어쓰기
        
        time.sleep(0.2)

except KeyboardInterrupt:
    print("\n\n✅ 조도 센서 테스트 종료")
    print(f"📊 측정 결과:")
    print(f"   - 최소값: {min_val} (가장 어두웠을 때)")
    print(f"   - 최대값: {max_val} (가장 밝았을 때)")
    print(f"   - 측정 범위: {max_val-min_val}")
    if max_val - min_val > 100:
        print("   ✅ 센서가 정상적으로 작동합니다!")
    else:
        print("   ⚠️ 센서 연결을 확인해주세요.")
finally:
    spi.close()