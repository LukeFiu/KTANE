from machine import Pin, PWM
from machine import Timer
from time import sleep, time_ns, time, ticks_ms
import random
import math
from PiicoDev_SSD1306 import *
from PiicoDev_Unified import sleep_ms

buttonPin = Pin(16, Pin.IN)
sdaPin = Pin(26)
sclPin = Pin(27)
display = create_PiicoDev_SSD1306(bus = 1, sda=sdaPin, scl=sclPin)

winLed = Pin(10, Pin.OUT)
loseLed = Pin(11, Pin.OUT)
loseLedOn = None


R = PWM(Pin(20, Pin.OUT))
G = PWM(Pin(18, Pin.OUT))
B = PWM(Pin(19, Pin.OUT))

indR = PWM(Pin(6, Pin.OUT))
indG = PWM(Pin(8, Pin.OUT))
indB = PWM(Pin(7, Pin.OUT))

R.freq(1000)
G.freq(1000)
B.freq(1000)

indR.freq(1000)
indG.freq(1000)
indB.freq(1000)

blue = (0,0,255)
red = (255,0,0)
white = (255,255,255)
yellow = (255,255,0)
purple = (255,0,255)

buttonColours = (blue, red, white, yellow, purple)
indicatorColours = (blue, red, white, yellow)
words = ("Abort", "Detonate", "Hold", "Press")
word = None
colour = None
indColour = None

pressedTime = None
releasedTime = None
held = False
everHeld = False
interruptFlag = 0
debounceTime = 0

litIndicators = {"CAR", "FRK"}
numBatteries = 3
needsHold = None
releaseDigit = None
checkSolution = False

seconds = 300
win = False

def callbackTimer(t):
    global seconds
    seconds  -= 1


def callbackBtn(BTN):
    global pressedTime, releasedTime, held, checkSolution, interruptFlag, debounceTime
    if (ticks_ms()-debounceTime) > 50:
        interruptFlag= 1
        debounceTime= ticks_ms()
        if pressedTime == None:
            pressedTime = time_ns()
        else :
            releasedTime = time_ns()
            print((releasedTime - pressedTime)/1000000000)
            pressedTime = None
            releasedTime = None
            held = False
            checkSolution = True
            print("button pressed")
        
buttonPin.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler = callbackBtn)


def btnRGB(r,g,b,m):
    R.duty_u16(r*m)
    G.duty_u16(g*m)
    B.duty_u16(b*m)
    
def indRGB(r,g,b, m):
    indR.duty_u16(r*m)
    indG.duty_u16(g*m)
    indB.duty_u16(b*m)

def initButton():
    wordIndex = random.randint(0,3)
    word = words[wordIndex]
    colIndex = random.randint(0,4)
    colour = buttonColours[colIndex]
    indColIndex = random.randint(0,3)
    indColour = indicatorColours[indColIndex]
    return word, colour, indColour

def getSolution():
    needsHold = None
    if (colour == blue) and (word == "Abort"):
        needsHold = True
    elif (numBatteries > 1) and (word =="Detonate"):
        needsHold = False
    elif (colour == white) and ("CAR" in litIndicators):
        needsHold = True
    elif (numBatteries > 2) and ("FRK" in litIndicators):
        needsHold = False
    elif (colour == yellow):
        needsHold = True
    elif (word == "Hold") and (colour == red):
        needsHold = False
    else:
        needsHold = True
        
    if needsHold == False:
        return needsHold, None
    
    releaseDigit = None
    if indColour == blue:
        releaseDigit = 4
    elif indColour == white:
        releaseDigit = 1
    elif indColour == yellow:
        releaseDigit = 5
    else:
        releaseDigit = 1
        
    return needsHold, releaseDigit
        
def mycallback(t):
    pass

# periodic at 1kHz
winLed.value(0)
loseLed.value(0)
tim = Timer()
tim.init(mode = Timer.PERIODIC, callback=callbackTimer, period = 1000)
word, colour, indColour = initButton()
needsHold, releaseDigit = getSolution()
print(releaseDigit)
print(needsHold)
multiplyer = 275
down = True
while True:
    
    if loseLedOn != None:
        if (time() - loseLedOn) >= 1:
            print("lose led off")
            loseLed.value(0)
            loseLedOn = None

    if seconds < 0:
        seconds = 0
        tim.deinit()
    
    if not win:
        if checkSolution:
            timeDigits = f"{timerMin}{timerSec}"
            print(timeDigits)
            print(needsHold)
            print(everHeld)
            print(releaseDigit)
            if (needsHold == everHeld):
                if releaseDigit != None:
                    for d in range(0,len(timeDigits)):
                        if int(timeDigits[d]) == releaseDigit:
                            win = True
                            winLed.value(1)
                    if not win:
                        loseLed.value(1)
                        loseLedOn = time()
                else:
                    win = True
                    winLed.value(1)
                    
            else:
                loseLed.value(1)
                loseLedOn = time()
            checkSolution = False
            everHeld = False
                    
                
    timerMin = (int)((seconds - (seconds%60))/60)
    timerSec = (int)(seconds-(timerMin*60))
    timerText = f"{timerMin:0>2}:{timerSec:0>2}"
    display.fill(0)
    display.text(timerText, 0,0,1)
    display.text(word,64-(len(word)*4),32, 1)
    display.show()
    btnRGB(colour[0], colour[1], colour[2], 275)
    
    if (pressedTime != None):
        if ((time_ns() - pressedTime)/1000000000 > 0.5):
            held = True
            everHeld = True
    
    if held:
        indRGB(indColour[0], indColour[1], indColour[2],multiplyer)
        if multiplyer <= 5:
            down = False
            multiplyer = 5
        elif multiplyer > 275:
            down = True
            multiplyer = 275    
        
        if down:
            multiplyer -= 5
        else :
            multiplyer += 5
    else:
        indRGB(0, 0, 0, 275)
