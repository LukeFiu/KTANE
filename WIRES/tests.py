from machine import Pin, ADC
import time

wireZeroPin = ADC(Pin(26, Pin.IN))
wireOnePin = ADC(Pin(27, Pin.IN))
wireTwoPin = ADC(Pin(28, Pin.IN))

Vin = 3.3
Vout = 0
Rref = 330

def calcResistance(sensorValue):
    print(sensorValue)
    Vout = (Vin * sensorValue)/65535
    r = Rref *(1/((Vin/Vout) -1))
    return r
    
while True:
    valueZero = wireZeroPin.read_u16()
    valueOne = wireOnePin.read_u16()
    valueTwo = wireTwoPin.read_u16()
    
    print("Two: ", calcResistance(valueTwo))
    print("One: ", calcResistance(valueOne))
    print("Zero: ", calcResistance(valueZero))
    print()
    
    
    time.sleep(1)