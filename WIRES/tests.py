from machine import Pin, ADC
import time

wirePin = ADC(Pin(26, Pin.IN))
APin = Pin(16, Pin.OUT)
BPin = Pin(17, Pin.OUT)
CPin = Pin(18, Pin.OUT)

Vin = 5
Vout = 0
Rref = 330

values = [0,0,0,0,0,0];

def calcResistance(sensorValue):

    Vout = (Vin * sensorValue)/65535
    r = Rref *(1/((Vin/Vout) -1))
    return r

def padBin(binaryStr):
    length = len(binaryStr)
    if length == 3:
        s = binaryStr[-1]
        return f'00{s}'
    elif length == 4:
        s = binaryStr[-2:]
        return f'0{s}'
    elif length == 5:
        s = binaryStr[-3:]
        return s

def readAllValues():
    for i in range(0,6):
        selectNum = bin(i)
        selectNum = padBin(selectNum)
        print(selectNum)
        APin.value(selectNum[-1])
        BPin.value(selectNum[-2])
        CPin.value(selectNum[-3])
        values[i] = wirePin.read_u16()
        print(i, calcResistance(values[i]))
    print()
        
    
while True:
    readAllValues()
    time.sleep(1)