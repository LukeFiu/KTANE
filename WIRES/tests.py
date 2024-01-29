from machine import Pin, ADC
import time

wirePin = ADC(Pin(26, Pin.IN))
APin = Pin(20, Pin.OUT)
BPin = Pin(21, Pin.OUT)
CPin = Pin(22, Pin.OUT)

Vin = 3.3
Vout = 0
Rref = 330

values = [];

def calcResistance(sensorValue):
    print(sensorValue)
    Vout = (Vin * sensorValue)/65535
    r = Rref *(1/((Vin/Vout) -1))
    return r

def readAllValues():
    for i in range(0,6):
        selectNum = bin(i)
        print(bin(i))
        APin.value(selectNum >> 1)
        BPin.value(selectNum >> 2)
        CPin.value(selectNum >> 3)
        values[i] = wirePin.read_u16()
        
    
while True:
    readAllValues
    time.sleep(1)