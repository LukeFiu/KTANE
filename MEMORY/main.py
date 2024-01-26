from machine import Pin,PWM, I2C
import time
import random

debounceTime = 0
interuptFlag = 0
buttonsPressed = []
stage = 0

sdaPin =  Pin(16, Pin.PULL_UP)
sclPin = Pin(17, Pin.PULL_UP)



buttonZero = Pin(28, Pin.IN, Pin.PULL_UP)
buttonOne = Pin(27, Pin.IN, Pin.PULL_UP)
buttonTwo = Pin(26, Pin.IN, Pin.PULL_UP)
buttonThree = Pin(22, Pin.IN, Pin.PULL_UP)

ZeroA = Pin(3, Pin.OUT, Pin.PULL_UP)
ZeroB = Pin(0, Pin.OUT, Pin.PULL_UP)
ZeroC = Pin(1, Pin.OUT, Pin.PULL_UP)
ZeroD = Pin(2, Pin.OUT, Pin.PULL_UP)
segZero = {"A":ZeroA, "B":ZeroB, "C":ZeroC, "D":ZeroD}

OneA = Pin(7, Pin.OUT, Pin.PULL_UP)
OneB = Pin(4, Pin.OUT, Pin.PULL_UP)
OneC = Pin(5, Pin.OUT, Pin.PULL_UP)
OneD = Pin(6, Pin.OUT, Pin.PULL_UP)
segOne = {"A":OneA, "B":OneB, "C":OneC, "D":OneD}

TwoA = Pin(11, Pin.OUT, Pin.PULL_UP)
TwoB = Pin(8, Pin.OUT, Pin.PULL_UP)
TwoC = Pin(9, Pin.OUT, Pin.PULL_UP)
TwoD = Pin(10, Pin.OUT, Pin.PULL_UP)
segTwo = {"A":TwoA, "B":TwoB, "C":TwoC, "D":TwoD}

ThreeA = Pin(15, Pin.OUT, Pin.PULL_UP)
ThreeB = Pin(12, Pin.OUT, Pin.PULL_UP)
ThreeC = Pin(13, Pin.OUT, Pin.PULL_UP)
ThreeD = Pin(14, Pin.OUT, Pin.PULL_UP)
segThree = {"A":ThreeA, "B":ThreeB, "C":ThreeC, "D":ThreeD}

topA = Pin(18, Pin.OUT, Pin.PULL_UP)
topB = Pin(21, Pin.OUT, Pin.PULL_UP)
topC = Pin(20, Pin.OUT, Pin.PULL_UP)
topD = Pin(19, Pin.OUT, Pin.PULL_UP)
segTop = {"A":topA, "B":topB, "C":topC, "D":topD}

i2c = I2C(0,sda=sdaPin, scl = sclPin, freq=400000)

segments = (segZero, segOne, segTwo, segThree, segTop)
seq = []
stages = []
correct = []
hexStages = {0:0x00, 1:0x01, 2:0x03, 3:0x07, 4:0x0F, 5:0x3F}


digits = {0:(0,0,0,0),
          1:(0,0,0,1),
          2:(0,0,1,0),
          3:(0,0,1,1),
          4:(0,1,0,0),
          5:(0,1,0,1),
          6:(0,1,1,0),
          7:(0,1,1,1),
          8:(1,0,0,0),
          9:(1,0,0,1),
          10:(1,0,1,0),
          11:(1,0,1,1),
          12:(1,1,0,0),
          13:(1,1,0,1),
          14:(1,1,1,0),
          15:(1,1,1,1)}

# register addresses in port=0, bank=1 mode (easier maths to convert)
MCP23008_BASEADDR 	  = const(0x20)
MCP23008_IODIR        = const(0x00) # R/W I/O Direction Register
MCP23008_IPOL         = const(0x01) # R/W Input Polarity Port Register
MCP23008_GPINTEN      = const(0x02) # R/W Interrupt-on-Change Pins
MCP23008_DEFVAL       = const(0x03) # R/W Default Value Register
MCP23008_INTCON       = const(0x04) # R/W Interrupt-on-Change Control Register
MCP23008_IOCON        = const(0x05) # R/W Configuration Register
MCP23008_GPPU         = const(0x06) # R/W Pull-Up Resistor Register
MCP23008_INTF         = const(0x07) # R   Interrupt Flag Register (read clears)
MCP23008_INTCAP       = const(0x08) # R   Interrupt Captured Value For Port Register
MCP23008_GPIO         = const(0x09) # R/W General Purpose I/O Port Register
MCP23008_OLAT         = const(0x0a) # R/W Output Latch Register

def writeMCP23xxxReg(reg, val):
    passVal = bytearray([reg, val])
    i2c.writeto(MCP23008_BASEADDR, passVal)

def writeLEDs(wrVal):
    writeMCP23xxxReg(MCP23008_GPIO, wrVal)

def initI2CIO8():
    writeMCP23xxxReg(MCP23008_IODIR, 0xF0)
    writeMCP23xxxReg(MCP23008_IPOL, 0xF0)
    writeMCP23xxxReg(MCP23008_GPINTEN, 0x0F)
    writeMCP23xxxReg(MCP23008_INTCON, 0x00)
    writeMCP23xxxReg(MCP23008_IOCON, 0x22)
    writeMCP23xxxReg(MCP23008_GPPU, 0x00)


def MCPDisplayStage(stage):
    writeLEDs(hexStages[stage])
 
def display(digit:int, segment):
    segment["A"].value(digits[digit][3])
    segment["B"].value(digits[digit][2])
    segment["C"].value(digits[digit][1])
    segment["D"].value(digits[digit][0])
    
def heapPerms(a, size):
    if size == 1:
        print(a)
        seq.append(a.copy())

        return

    for i in range(size):
        heapPerms(a, size-1)
        
        if size & 1:
            a[0], a[size-1] =  a[size-1], a[0]
        else:
            a[i], a[size-1] = a[size-1], a[i]
        
        
def initMemory():    
    seq.clear()
    stages.clear()
    correct.clear()
    a = [1,2,3,4]
    n = len(a)
    heapPerms(a,n)   

    print(stages)
    for i in range(0,5):
        stage = random.choice(seq)
        while len(stage) > 4:
            del stage[-1]
        print(stage)
        stage.append(random.randrange(1,5))
        print(stage)
        print()
        stages.append(stage)
    
    print(stages)
    getCorrect(stages)
    stage = 0
    print(correct)
        
def displayStage(stage:int, stages):
    for i in range(0, len(stages[stage])):
        display(stages[stage][i],segments[i])
        
def blankSegments():
    for seg in segments:
        display(15,seg)
        
        
def callbackZero(buttonZero):
    global interuptFlag, debounceTime, buttonsPressed
    if (time.ticks_ms()-debounceTime) > 400:
        interuptFlag= 1
        debounceTime=time.ticks_ms()
        buttonsPressed.append(0)
        print("button Zero pressed")
        
buttonZero.irq(trigger=Pin.IRQ_RISING, handler=callbackZero)

def callbackOne(buttonOne):
    global interuptFlag, debounceTime, buttonsPressed
    if (time.ticks_ms()-debounceTime) > 400:
        interuptFlag= 1
        debounceTime=time.ticks_ms()
        buttonsPressed.append(1)
        print("button One pressed")
        
buttonOne.irq(trigger=Pin.IRQ_RISING, handler=callbackOne)

def callbackTwo(buttonTwo):
    global interuptFlag, debounceTime, buttonsPressed
    if (time.ticks_ms()-debounceTime) > 400:
        interuptFlag= 1
        debounceTime=time.ticks_ms()
        buttonsPressed.append(2)
        print("button Two pressed")
        
buttonTwo.irq(trigger=Pin.IRQ_RISING, handler=callbackTwo)

def callbackThree(buttonThree):
    global interuptFlag, debounceTime, buttonsPressed
    if (time.ticks_ms()-debounceTime) > 400:
        interuptFlag= 1
        debounceTime=time.ticks_ms()
        buttonsPressed.append(3)
        print("button Three pressed")
        
buttonThree.irq(trigger=Pin.IRQ_RISING, handler=callbackThree)

def getButtonPress():
    buttonsPressed.clear()
    while True:
        if len(buttonsPressed) != 0:
            return buttonsPressed.pop(0)
        
def checkButton(pressed, stage):
    print(f"pressed: ", pressed)
    print(f"stage: ", stage)
    print(f"correct: ",correct[stage])
    if pressed == correct[stage]:
        return True
    return False
    

def getCorrect(stages):
    for stage in range(0,len(stages)): 
        topDigit = stages[stage][4]
        if stage == 0:
            if topDigit == 1:
                correct.append(1)
            elif topDigit == 2:
                correct.append(1)
            elif topDigit == 3:
                correct.append(2)
            elif topDigit == 4:
                correct.append(3)
        elif stage == 1:
            if topDigit == 1:
                correct.append(stages[stage].index(4))
            elif topDigit == 2:
                correct.append(correct[0])
            elif topDigit == 3:
                correct.append(0)
            elif topDigit == 4:
                correct.append(correct[0])
        elif stage == 2:
            if topDigit == 1:
                #get the location of the digit that coresponds to the index of correct solution number two
                #from the second stage get the digit from the button pressed in stage two then find the index of the same number in stage 3
                correct.append(stages[stage].index(stages[1][correct[1]]))
            elif topDigit == 2:
                correct.append(stages[stage].index(stages[0][correct[0]]))
            elif topDigit == 3:
                correct.append(2)
            elif topDigit == 4:
                correct.append(stages[stage].index(4))
        elif stage ==  3:
            if topDigit == 1:
                correct.append(correct[0])
            elif topDigit == 2:
                correct.append(0)
            elif topDigit == 3:
                correct.append(correct[1])
            elif topDigit == 4:
                correct.append(correct[1])
        elif stage == 4:
            if topDigit == 1:
                correct.append(stages[stage].index(stages[0][correct[0]]))
            elif topDigit == 2:
                correct.append(stages[stage].index(stages[1][correct[1]]))
            elif topDigit == 3:
                correct.append(stages[stage].index(stages[3][correct[3]]))
            elif topDigit == 4:
                correct.append(stages[stage].index(stages[2][correct[2]]))
        

initMemory()
initI2CIO8()
writeMCP23xxxReg(MCP23008_IODIR, 0x00)
MCPDisplayStage(stage)
while True:
    #display stage
    displayStage(stage, stages)
    #check for button press
    button = getButtonPress()
    #if correct increment stage else reset to stage 1
    if checkButton(button, stage):
        print("success")
        blankSegments()
        stage += 1
        MCPDisplayStage(stage)
        if stage == 5:
            break

    else:
        print("fail")
        initMemory()
        stage=0
        MCPDisplayStage(stage)

     


