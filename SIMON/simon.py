from machine import Pin,PWM
import time
import random

MAX_LEVEL = 100
sequence = []
sound = []
player_sequence = []
level = 1
note = 0
velocity = 1000

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

while True:
    print(level)
    if level == 1:
        generateSequence()
    
    for l in leds:
        l.high()
        time.sleep(100)
        l.low()
        
    if GRN_BTN.value == 0 or level !=1:
        time.sleep(1000)
        show_sequence()
        get_sequence()
            
            
            
    
        
        
def generateSequence():
    random.seed(Pin(27).value())
    
    for i in range(MAX_LEVEL + 1):
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
        time.sleep(200)
        
        
def check_btn(button, sound, led):
    if button.value == 1:
        led.high()
        tone(sound)
        player_sequence.append(led)
        return True
    return False
        

def get_sequence():
    flag = 0
    
    for i in range(level):
        flag = 0
        while flag == 0:
            for j in range(1,5):
                flag = check_btn(buttons[j], sounds[j], leds[j])
                if player_sequence[i] != sequence[i]:
                    wrong_sequence()
                    return
                leds[j].low()
                break
            right_sequence()
            

def right_sequence():
    global level
    global velocity
    
    for l in leds:
        l.low()
    time.sleep(250)
    
    for l in leds:
        l.high()
    time.sleep(500)
    
    for l in leds:
        l.low()
    time.sleep(500)
    
    
    if level <= MAX_LEVEL:
        level += 1
    
    velocity -= 50
    

def wrong_sequence():
    global level, velocity
    
    for i in range(4):
        for l in leds:
            l.high()
        time.sleep(250)
        
        for l in leds:
            l.low()
        time.sleep(250)
        
    level = 1
    velocity = 1000
        
   
        