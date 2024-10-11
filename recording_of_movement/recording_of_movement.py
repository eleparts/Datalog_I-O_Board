# 사용 제품 및 사용 라이브러리 세팅
from machine import Pin, ADC, I2C
from ds3231 import *
import time, sdcard, uos

PIR = Pin(22, Pin.IN)

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

Day_of_the_week_eng = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
Day_of_the_week_kor = ["월","화","수","목","금","토","일"]

before_human = 0

# 텍스트파일명 지정 및 텍스트파일 내 소제목 출력하기
now = ds.get_time()
title = "%04d.%02d.%02d.%s Human motion detection" % (now[0],now[1],now[2],Day_of_the_week_eng[now[6]])
with open("/sd/%s.txt" % title, "a") as file:
            file.write("%04d년 %02d월 %02d일 %s요일 인체 감지\r\n\n" % (now[0], now[1], now[2], Day_of_the_week_kor[now[6]]))

while True:
    # 추후에 사용할 인체 감지 센서 값, 시간 등 변수 세팅
    human = PIR.value()
    
    now = ds.get_time()
    
    title = "%04d.%02d.%02d.%s Human motion detection" % (now[0],now[1],now[2],Day_of_the_week_eng[now[6]])
    
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
    
    #인체 감지 센서에서 움직임을 감지할 시 출입 감지 문구를 SD CARD에 출력합니다.
    if human == 1 and before_human == 0:
        with open("/sd/%s.txt" % title, "a") as file:
            file.write("출입 감지 / %s %02d시 %02d분 %02d초\r\n\n" % (half, pm_hour, now[4], now[5]))
    
    before_human = human
    time.sleep_ms(100)
    




