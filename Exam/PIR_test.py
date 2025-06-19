import RPi.GPIO as GPIO
import time

# PIR 센서 핀 설정
PIR_SENSOR_PIN = 17

# GPIO 초기화
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_SENSOR_PIN, GPIO.IN)

print("\n🔍 PIR 모션 센서 테스트 시작 (Ctrl+C로 종료)")
print("센서 앞에서 움직여보세요!\n")

try:
    motion_count = 0
    last_state = 0
    
    while True:
        current_state = GPIO.input(PIR_SENSOR_PIN)
        
        # 상태 변화가 있을 때만 출력
        if current_state != last_state:
            if current_state == 1:
                motion_count += 1
                print(f"🚶 [{time.strftime('%H:%M:%S')}] 움직임 감지됨! (총 {motion_count}회)")
            else:
                print(f"⏸️  [{time.strftime('%H:%M:%S')}] 움직임 멈춤")
            
            last_state = current_state
        
        time.sleep(0.1)  # 100ms 간격으로 체크

except KeyboardInterrupt:
    print(f"\n✅ PIR 센서 테스트 종료")
    print(f"📊 총 감지 횟수: {motion_count}회")
finally:
    GPIO.cleanup()