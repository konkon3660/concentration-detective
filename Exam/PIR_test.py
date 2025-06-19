import RPi.GPIO as GPIO
import time

# PIR 센서 핀 설정
PIR_SENSOR_PIN = 17

# GPIO 초기화 (Pull-down 저항 추가)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print("\n🔍 PIR 모션 센서 테스트 시작 (Ctrl+C로 종료)")
print("⏳ PIR 센서 안정화 대기 중... (30초)")
print("   (센서가 안정될 때까지 잠시 기다려주세요)")

# PIR 센서 안정화 대기
for i in range(30, 0, -1):
    print(f"\r   안정화 대기: {i:2d}초 남음", end="", flush=True)
    time.sleep(1)

print("\n✅ 안정화 완료! 센서 앞에서 움직여보세요!\n")

try:
    motion_count = 0
    last_state = 0
    continuous_high_count = 0
    
    print("📊 실시간 센서 값 모니터링:")
    print("   (연속으로 HIGH가 나오면 회로 문제일 수 있습니다)")
    print("-" * 50)
    
    while True:
        current_state = GPIO.input(PIR_SENSOR_PIN)
        
        # 연속 HIGH 상태 카운트
        if current_state == 1:
            continuous_high_count += 1
        else:
            continuous_high_count = 0
        
        # 상태 변화가 있을 때만 출력
        if current_state != last_state:
            if current_state == 1:
                motion_count += 1
                print(f"🚶 [{time.strftime('%H:%M:%S')}] 움직임 감지됨! (총 {motion_count}회)")
            else:
                print(f"⏸️  [{time.strftime('%H:%M:%S')}] 움직임 멈춤")
            
            last_state = current_state
        
        # 연속 HIGH 경고
        if continuous_high_count > 50:  # 5초간 연속 HIGH
            print(f"⚠️  [{time.strftime('%H:%M:%S')}] 경고: {continuous_high_count/10:.1f}초간 연속 HIGH 상태")
            print("    → 회로 연결을 확인해주세요 (Pull-down 저항 필요할 수 있음)")
            continuous_high_count = 0  # 경고 리셋
        
        # 현재 상태를 주기적으로 표시 (10초마다)
        if int(time.time()) % 10 == 0 and time.time() - int(time.time()) < 0.1:
            print(f"📍 [{time.strftime('%H:%M:%S')}] 현재 상태: {'HIGH' if current_state else 'LOW'}")
        
        time.sleep(0.1)  # 100ms 간격으로 체크

except KeyboardInterrupt:
    print(f"\n✅ PIR 센서 테스트 종료")
    print(f"📊 총 감지 횟수: {motion_count}회")
finally:
    GPIO.cleanup()