# 사용 제품 및 사용 라이브러리 세팅
from machine import Pin, ADC, I2C
from ds3231 import *
import time, sdcard, uos, dht

sensor = dht.DHT11(Pin(26))

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

# 텍스트파일명 지정 및 텍스트파일 내 소제목 출력하기
now = ds.get_time()
title = "%04d.%02d.%02d.%s Measure temperature & humidity" % (now[0],now[1],now[2],Day_of_the_week_eng[now[6]])
with open("/sd/%s.txt" % title, "a") as file:
            file.write("%04d년 %02d월 %02d일 %s요일 온습도 측정\r\n\n" % (now[0], now[1], now[2], Day_of_the_week_kor[now[6]]))

flag = now[5]
one_print = 0

while True:
    # 추후에 사용할 온도 값과 습도 값, 시간 등 변수 세팅
    sensor.measure()
    temp = sensor.temperature()
    humi = sensor.humidity()
    
    now = ds.get_time()
    
    title = "%04d.%02d.%02d.%s Measure temperature & humidity" % (now[0],now[1],now[2],Day_of_the_week_eng[now[6]])
    
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
    
    # 1분마다 온도 및 습도 값을 SD CARD에 출력합니다.
    if second == flag and one_print == 0 :
        with open("/sd/%s.txt" % title, "a") as file:
            file.write("온도 : %02d℃, 습도 : %02d％ %s %02d시 %02d분 %02d초\r\n\n" % (temp, humi, half, pm_hour, now[4], now[5]))
        one_print = 1
    elif second != flag and one_print == 1 :
        one_print = 0
    
    time.sleep_ms(100)
    





