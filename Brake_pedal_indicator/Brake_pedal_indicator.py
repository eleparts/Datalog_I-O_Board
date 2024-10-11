# 사용 제품 및 사용 라이브러리 세팅
from machine import Pin, ADC, I2C
from ds3231 import *
import time, sdcard, uos

adc = ADC(Pin(26))
LED = Pin(22, Pin.OUT)

i2c = I2C(1,sda=Pin(14), scl=Pin(15))
ds = DS3231(i2c)

cs = machine.Pin(1, machine.Pin.OUT)
spi = machine.SPI(0,
                  baudrate=1000000,
                  polarity=0,
                  phase=0,
                  bits=8,
                  firstbit=machine.SPI.MSB,
                  sck=machine.Pin(2),
                  mosi=machine.Pin(3),
                  miso=machine.Pin(4))
sd = sdcard.SDCard(spi, cs)
vfs = uos.VfsFat(sd)
uos.mount(vfs, "/sd")

before_Pressure = 0
before_second = 0

P_value = 20000

Day_of_the_week_eng = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
Day_of_the_week_kor = ["월","화","수","목","금","토","일"]

# 텍스트파일명 지정 및 텍스트파일 내 소제목 출력하기
now = ds.get_time()
title = "%04d.%02d.%02d.%s" % (now[0],now[1],now[2],Day_of_the_week_eng[now[6]])
with open("/sd/%s.txt" % title, "a") as file:
            file.write("%04d년 %02d월 %02d일 %s요일\r\n\n" % (now[0], now[1], now[2], Day_of_the_week_kor[now[6]]))

while True:
    # 추후에 사용할 밟은 세기, 시간 등 변수 세팅
    Pressure = adc.read_u16()
    if Pressure > 0 :
        Pressure_percent = Pressure / 65535 * 100
    
    print(Pressure)
    
    now = ds.get_time()
    
    title = "%04d.%02d.%02d.%s" % (now[0],now[1],now[2],Day_of_the_week_eng[now[6]])

    second = now[5]
    
    # 오전 오후 구분 및 0시 12시 해결
    if now[3] // 12 == 0 :
        pm_hour = now[3] % 12
        half = "오전"
        if now[3] % 12 == 0 :
            pm_hour = 12
    elif now[3] // 12 == 1 :
        pm_hour = now[3] % 12
        half = "오후"
        if now[3] % 12 == 0 :
            pm_hour = 12
    
    #직전 측정때 설정 값이 안나왔으며, 이번 측정때 설정 값 이상이 나올 경우, 텍스트 파일([브레이크 밟은 시간]문구와 밟은 세기 출력, LED에서 브레이크 밟았을 때의 제어 시작 
    if before_Pressure < P_value and Pressure >= P_value :
        LED.value(1)
        with open("/sd/%s.txt" % title, "a") as file:
            file.write("브레이크 밟은 시간 / %s %02d시 %02d분 %02d초\r\n" % (half, pm_hour, now[4], now[5]))
            file.write("밟은 세기 / %d \r\n" %Pressure_percent)
        before_Pressure = P_value
    #브레이크를 밟는 것이 유지되고 있는 경우, 밟은 세기를 1초당 한번 출력
    elif before_Pressure == P_value and Pressure >= P_value :
        LED.value(1)
        if before_second != second :
            with open("/sd/%s.txt" % title, "a") as file:
                file.write("밟은 세기 / %d \r\n" %Pressure_percent)
    #브레이크를 밟다가 떼어냈을 경우, [브레이크 뗀 시간]문구 출력과 함께 LED를 끄며 마무리합니
    elif before_Pressure == P_value and Pressure < P_value :
        LED.value(0)
        with open("/sd/%s.txt" % title, "a") as file:
            file.write("브레이크 뗀 시간 / %s %02d시 %02d분 %02d초\r\n\n" % (half, pm_hour, now[4], now[5]))
        before_Pressure = 0
    else :
        LED.value(0)
        
    
    before_second = second        
    time.sleep_ms(100)
    

