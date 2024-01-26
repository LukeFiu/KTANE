from machine import Pin,PWM
import time
import random

MAX_LEVEL = 100
sequence = []
sound = []
player_sequence = []
level = 1
note = 0
velocity = 1

GRN_SOUND = 261
RED_SOUND = 293
YEL_SOUND = 329
BLU_SOUND = 349
BAD_SOUND = 233


GRN_LED_PIN = 13
RED_LED_PIN = 12
YEL_LED_PIN = 11
BLU_LED_PIN = 10

GRN_LED = Pin(13, Pin.OUT)
RED_LED = Pin(12, Pin.OUT)
YEL_LED = Pin(11, Pin.OUT)
BLU_LED = Pin(10, Pin.OUT)

GRN_BTN = Pin(18, Pin.IN, Pin.PULL_UP)
RED_BTN = Pin(19, Pin.IN, Pin.PULL_UP)
YEL_BTN = Pin(20, Pin.IN, Pin.PULL_UP)
BLU_BTN = Pin(21, Pin.IN, Pin.PULL_UP)

leds = [GRN_LED, RED_LED, YEL_LED, BLU_LED]
buttons = [GRN_BTN, RED_BTN, YEL_BTN, BLU_BTN]
sounds = [GRN_SOUND, RED_SOUND, YEL_SOUND, BLU_SOUND]

p23 = Pin(3, Pin.OUT)
PIEZO = PWM(p23)

        
def generateSequence():
    random.seed(Pin(27).value())
    
    for i in range(MAX_LEVEL):
        sequence.append(random.randint(BLU_LED_PIN, GRN_LED_PIN))
        
        note = None
        if sequence[i] == BLU_LED_PIN:
            sequence[i] = BLU_LED
            note = BLU_SOUND
        elif sequence[i] == YEL_LED_PIN:
            sequence[i] = YEL_LED
            note = YEL_SOUND
        elif sequence[i] == RED_LED_PIN:
            sequence[i] = RED_LED
            note = YEL_SOUND
        elif sequence[i] == GRN_LED_PIN:
            sequence[i] = GRN_LED
            note = GRN_SOUND
            
        sound.append(note)
        

def tone(freq):
    PIEZO.freq(freq)
    PIEZO.duty_u16(32757)
    time.sleep(velocity)
    PIEZO.duty_ns(0)
        
def show_sequence():
    for l in leds:
        l.low()
        
    print("level=")
    print(level)
    
    for i in range(level):
        sequence[i].high()
        tone(sound[i])
        sequence[i].low()
        time.sleep(0.200)
        
        
def check_btn(button, sound, led):
    if button.value == 1:
        led.high()
        tone(sound)
        player_sequence.append(led)
        return 1
    return 0
        

def get_sequence():
    print("get_sequence")
    flag = 0
    
    i = 0
    while i < level:
        print(f"i is \'{i}\'")
        flag = 0
        while flag == 0:
            print ("flag is 0")
            j = 0
            while j < 4:
                print(f"j is \'{j}\'")
                flag = check_btn(buttons[j], sounds[j], leds[j])
                if flag == 1:
                    if player_sequence[i] != sequence[i]:
                        wrong_sequence()
                        return
                    else:
                        right_sequence()
                    leds[j].low()
                    break
                j += 1            
        i += 1
            

def right_sequence():
    global level
    global velocity
    
    print("Right Sequence")
    
    for l in leds:
        l.low()
    time.sleep(0.250)
    
    for l in leds:
        l.high()
    time.sleep(0.500)
    
    for l in leds:
        l.low()
    time.sleep(0.500)
    
    
    if level <= MAX_LEVEL:
        level += 1
    
    velocity -= 50
    

def wrong_sequence():
    global level, velocity
    
    print("Wrong Sequence")
    
    for i in range(4):
        for l in leds:
            l.high()
        time.sleep(0.250)
        
        for l in leds:
            l.low()
        time.sleep(0.250)
        
    level = 1
    velocity = 1000
        
   
while True:
    if level == 1:
        sequence = []
        generateSequence()
        
    
    for l in leds:
        l.high()
        time.sleep(0.1)
        l.low()
        
    if GRN_BTN.value() == 0 or level !=1:
        time.sleep(1)
        show_sequence()
        get_sequence()