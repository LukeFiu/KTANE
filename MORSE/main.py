from machine import Pin, ADC, PWM
from PiicoDev_SSD1306 import *
from PiicoDev_Unified import sleep_ms
import utime

pot = ADC(28)
AA_led = Pin(0, Pin.OUT)
AB_led = Pin(1, Pin.OUT)
AC_led = Pin(2, Pin.OUT)
AD_led = Pin(3, Pin.OUT)
AE_led = Pin(4, Pin.OUT)
AF_led = Pin(5, Pin.OUT)
AG_led = Pin(6, Pin.OUT)

BA_led = Pin(16, Pin.OUT)
BB_led = Pin(17, Pin.OUT)
BC_led = Pin(18, Pin.OUT)
BD_led = Pin(19, Pin.OUT)
BE_led = Pin(20, Pin.OUT)
BF_led = Pin(21, Pin.OUT)
BG_led = Pin(22, Pin.OUT)
delay = 0.1

leds = [AA_led, AB_led, AC_led, AD_led, AE_led, AF_led, AG_led, BA_led, BB_led, BC_led, BD_led, BE_led, BF_led, BG_led]
Aletters = {"1":[AB_led, AC_led] , "2":[AA_led, AB_led, AD_led, AE_led, AF_led], "3":{AA_led, AB_led, AC_led, AD_led, AF_led}, "4":[AB_led, AC_led, AF_led, AG_led], "5":[AA_led, AC_led, AD_led, AF_led, AG_led], "6":[AA_led, AC_led, AD_led, AE_led, AF_led, AG_led], "7":[AA_led, AB_led, AC_led], "8":[AA_led, AB_led, AC_led, AD_led, AE_led, AF_led, AG_led], "9":[AA_led, AB_led, AC_led, AD_led, AF_led, AG_led], "0":[AA_led, AB_led, AC_led, AD_led, AE_led, AG_led]}

Bletters = {"1":[BB_led, BC_led] , "2":[BA_led, BB_led, BD_led, BE_led, BF_led], "3":{BA_led, BB_led, BC_led, BD_led, BF_led}, "4":[BB_led, BC_led, BF_led, BG_led], "5":[BA_led, BC_led, BD_led, BF_led, BG_led], "6":[BA_led, BC_led, BD_led, BE_led, BF_led, BG_led], "7":[BA_led, BB_led, BC_led], "8":[BA_led, BB_led, BC_led, BD_led, BE_led, BF_led, BG_led], "9":[BA_led, BB_led, BC_led, BD_led, BF_led, BG_led], "0":[BA_led, BB_led, BC_led, BD_led, BE_led, BG_led]}

display = create_PiicoDev_SSD1306()

def map(x, in_min, in_max, out_min, out_max):
    return int((x-in_min) * (out_max-out_min) / (in_max - in_min) + out_min)
    
while True:
    display.fill(0)
    num = str(map(pot.read_u16(), 288, 65535, 0, 16))
    display.text(num,10,round(HEIGHT/2), 1)
    display.show()
    if len(num) == 1:
        num = "0" + num
    sleep_ms(10)



