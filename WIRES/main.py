from machine import Pin, ADC
import time

chipOut = ADC(Pin(26, Pin.IN))

APin = Pin(20, Pin.OUT)
BPin = Pin(21, Pin.OUT)
CPin = Pin(22, Pin.OUT)

Vin = 5
Rref = 330


while True:
    APin.value(1)
    BPin.value(0)
    CPin.value(1)
    sensorValue = chipOut.read_u16()
    Vout = (Vin * sensorValue) / 65535
    R = (Rref * (1/((Vin / Vout) - 1 )))
    print(R)
    time.sleep(1)