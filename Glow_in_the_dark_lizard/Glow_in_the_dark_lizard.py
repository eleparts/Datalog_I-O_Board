# 사용 제품 및 사용 라이브러리 세팅
from machine import Pin, ADC, I2C
from ds3231 import *
from time import sleep
import time, sdcard, uos

photoPIN = 26
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

before_light = 0

Day_of_the_week_eng = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
Day_of_the_week_kor = ["월","화","수","목","금","토","일"]

# 텍스트파일명 지정 및 텍스트파일 내 소제목 출력하기
now = ds.get_time()
title = "%04d.%02d.%02d.%s cds control" % (now[0],now[1],now[2],Day_of_the_week_eng[now[6]])
with open("/sd/%s.txt" % title, "a") as file:
            file.write("%04d년 %02d월 %02d일 %s요일 광센서 제어\r\n\n" % (now[0], now[1], now[2], Day_of_the_week_kor[now[6]]))

def readLight(photoGP):
    photoRes = ADC(Pin(26))
    light = photoRes.read_u16()
    light = round(light/65535*100,2)
    return light

while True:
    # 추후에 사용할 밝기 값, 시간 등 변수 세팅
    
    print("light: " + str(readLight(photoPIN)) +"%")
    sleep(1)
    
    now = ds.get_time()
    
    title = "%04d.%02d.%02d.%s cds control" % (now[0],now[1],now[2],Day_of_the_week_eng[now[6]])
    
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
    
    # 평소 밝기 값보다 낮아지는 경우, LED를 키며, 문구를 출력합니다.
    if readLight(photoPIN) < 3 and before_light == 0 :
        LED.value(1)
        before_light = 1
        with open("/sd/%s.txt" % title, "a") as file:
            file.write("LED가 켜진 시간 / %s %02d시 %02d분 %02d초\r\n" % (half, pm_hour, now[4], now[5]))
    # 평소 밝기 값보다 낮으며, LED가 켜져있는 상태에서 LED가 켜진 것을 유지한다.
    elif readLight(photoPIN) < 3 and before_light == 1 :
        LED.value(1)
    # 평소 밝기 값이거나 보다 높아졌을 때, LED를 끄고, 문구를 출력합니다.    
    elif readLight(photoPIN) >= 3 and before_light == 1 :
        LED.value(0)
        before_light = 0
        with open("/sd/%s.txt" % title, "a") as file:
            file.write("LED가 꺼진 시간 / %s %02d시 %02d분 %02d초\r\n\n" % (half, pm_hour, now[4], now[5]))
            
    time.sleep_ms(100)
    



