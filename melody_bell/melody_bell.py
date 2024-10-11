# 사용 제품 및 사용 라이브러리 세팅
from machine import Pin, ADC, I2C
from ds3231 import *
from picozero import Speaker
import time, sdcard, uos

speaker = Speaker(22)
SW = Pin(26, Pin.IN)

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

before_SW = 0

Day_of_the_week_eng = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
Day_of_the_week_kor = ["월","화","수","목","금","토","일"]

# 텍스트파일명 지정 및 텍스트파일 내 소제목 출력하기
now = ds.get_time()
title = "%04d.%02d.%02d.%s sw, buzzer control" % (now[0],now[1],now[2],Day_of_the_week_eng[now[6]])
with open("/sd/%s.txt" % title, "a") as file:
            file.write("%04d년 %02d월 %02d일 %s요일 스위치, 부저 제어\r\n\n" % (now[0], now[1], now[2], Day_of_the_week_kor[now[6]]))

# 멜로디 배열 제작 - Raspberry Pi Foundation 예제 사용
BEAT = 0.4
liten_mus = [ ['d5', BEAT / 2], ['d#5', BEAT / 2], ['f5', BEAT], ['d6', BEAT], ['a#5', BEAT], ['d5', BEAT],
              ['f5', BEAT], ['d#5', BEAT], ['d#5', BEAT], ['c5', BEAT / 2],['d5', BEAT / 2], ['d#5', BEAT],
              ['c6', BEAT], ['a5', BEAT], ['d5', BEAT], ['g5', BEAT], ['f5', BEAT], ['f5', BEAT], ['d5', BEAT / 2],
              ['d#5', BEAT / 2], ['f5', BEAT], ['g5', BEAT], ['a5', BEAT], ['a#5', BEAT], ['a5', BEAT], ['g5', BEAT],
              ['g5', BEAT], ['', BEAT / 2], ['a#5', BEAT / 2], ['c6', BEAT / 2], ['d6', BEAT / 2], ['c6', BEAT / 2],
              ['a#5', BEAT / 2], ['a5', BEAT / 2], ['g5', BEAT / 2], ['a5', BEAT / 2], ['a#5', BEAT / 2], ['c6', BEAT],
              ['f5', BEAT], ['f5', BEAT / 2], ['d#5', BEAT / 2], ['d5', BEAT], ['f5', BEAT], ['d6', BEAT], ['d6', BEAT / 2],
              ['c6', BEAT / 2], ['b5', BEAT], ['g5', BEAT], ['g5', BEAT], ['c6', BEAT / 2], ['a#5', BEAT / 2], ['a5', BEAT],
              ['f5', BEAT], ['d6', BEAT], ['a5', BEAT], ['a#5', BEAT * 1.5] ]

while True:
    # 추후에 사용할 버튼 ON_OFF, 시간 등 변수 세팅
    
    now = ds.get_time()
    
    title = "%04d.%02d.%02d.%s sw, buzzer control" % (now[0],now[1],now[2],Day_of_the_week_eng[now[6]])
    
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
    
    #버튼을 누를 시 설정한 멜로디가 재생되며, 노래 재생이라는 문구가 출력됩니다.
    #멜로디가 종료되면, 노래 중지라는 문구가 출력됩니다.
    if SW.value() == 1 and before_SW == 0 :
        speaker.play(liten_mus)
        with open("/sd/%s.txt" % title, "a") as file:
            file.write("노래 재생 / %s %02d시 %02d분 %02d초\r\n" % (half, pm_hour, now[4], now[5]))
    elif SW.value() == 0 and before_SW == 1 :
        with open("/sd/%s.txt" % title, "a") as file:
            file.write("노래 중지 / %s %02d시 %02d분 %02d초\r\n\n" % (half, pm_hour, now[4], now[5]))
    
    before_SW = SW.value()
    time.sleep_ms(100)
    

