# This example drives two OLED modules independently.
# Each OLED module requires a unique address, set by the ADDR Jumper or ASW Switch
from PiicoDev_SSD1306 import *
from machine import Pin
import time
import random

btnA = Pin(21)
btnB = Pin(20)
btnC = Pin(19)
btnD = Pin(18)

loseLed = Pin(12)
winLed = Pin(13)

sdaPin = Pin(14)
sclPin = Pin(15)

buttonsPressed = []
debounceTime = 0
win = False



oledA = create_PiicoDev_SSD1306(bus = 1, sda=sdaPin, scl=sclPin, asw=0) 
oledB = create_PiicoDev_SSD1306(bus = 1, sda=sdaPin, scl=sclPin, asw=1) # set up each device using the address-switch argument. 0:Open, 1:Closed

symbolSets = (('balloon', 'at', 'lambda','squigglyn', 'squidknife', 'hookn', 'leftc'),
              ('euro','balloon','leftc','cursive','hollowstar','hookn', 'questionmark'),
              ('copyright', 'pumpkin', 'cursive', 'doublek','meltedthree', 'lambda','hollowstar'),
              ('six','paragraph','bt','squidknife','doublek','questionmark','smileyface'),
              ('pitchfork','smileyface','bt','rightc','paragraph','dragon','filledstar'),
              ('six', 'euro', 'tracks', 'ae', 'pitchfork', 'nwithhat', 'omega'))


# advanced users may prefer using explicit I2C addresses, which can be set using the 'address' argument as follows:
# oledB = oledB = create_PiicoDev_SSD1306(address=0x3D)
def callbackZero(btnA):
    global debounceTime, buttonsPressed
    if (time.ticks_ms()-debounceTime) > 200:
        debounceTime=time.ticks_ms()
        buttonsPressed.append(0)
        print("button A pressed")
        
btnA.irq(trigger=Pin.IRQ_RISING, handler=callbackZero)

def callbackOne(btnB):
    global debounceTime, buttonsPressed
    if (time.ticks_ms()-debounceTime) > 200:
        debounceTime=time.ticks_ms()
        buttonsPressed.append(1)
        print("button B pressed")
        
btnB.irq(trigger=Pin.IRQ_RISING, handler=callbackOne)

def callbackTwo(btnC):
    global debounceTime, buttonsPressed
    if (time.ticks_ms()-debounceTime) > 200:
        debounceTime=time.ticks_ms()
        buttonsPressed.append(2)
        print("button C pressed")
        
btnC.irq(trigger=Pin.IRQ_RISING, handler=callbackTwo)

def callbackThree(btnD):
    global debounceTime, buttonsPressed
    if (time.ticks_ms()-debounceTime) > 200:
        debounceTime=time.ticks_ms()
        buttonsPressed.append(3)
        print("button D pressed")
        
btnD.irq(trigger=Pin.IRQ_RISING, handler=callbackThree)

def initKeypad():
    symbols = []
    btnOrder = []
    indexes = []
    symbolSet = symbolSets[random.randint(0,5)]
    while (len(symbols) < 4):
        candidate = symbolSet[random.randint(0,6)]
        if candidate not in symbols:
            symbols.append(candidate)
    for s in symbols:
        indexes.append(symbolSet.index(s))
    while len(indexes) > 0:
        smallestInd = min(indexes)
        btnOrder.append(symbols.index(symbolSet[smallestInd]))
        indexes.remove(smallestInd)
    
    return symbols, btnOrder
            
            
# Load a different string onto each display
def main():
    global buttonsPressed, win
    loseLed = Pin(12, Pin.OUT)
    winLed = Pin(13, Pin.OUT)
    loseLed.value(0)
    winLed.value(0)
    btnOrder = []
    symbols, btnOrder = initKeypad()
    unpressed = btnOrder.copy()
    print(symbols)
    print(btnOrder)

    oledA.load_pbm(f"{symbols[0]}A.pbm",1)
    oledA.load_pbm(f"{symbols[1]}B.pbm",1)
    oledB.load_pbm(f"{symbols[2]}A.pbm",1)
    oledB.load_pbm(f"{symbols[3]}B.pbm",1)

    oledA.show()
    oledB.show()
    
    buttonsPressed = []
    while not win:
        if len(unpressed) > 0:
            if len(buttonsPressed) > 0:
                b = buttonsPressed.pop(0)
                if (b == unpressed.pop(0)):
                    print('CORRECT')
                else:
                    print("WRONG")
                    unpressed = btnOrder.copy()
                    loseLed.value(1)
                    time.sleep(1)
                    loseLed.value(0)
        else:
            print("WIN")
            win = True
            winLed.value(1)
    
    
    
        
        


if __name__ == '__main__':
    main()