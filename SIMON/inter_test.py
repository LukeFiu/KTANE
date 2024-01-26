from machine import Pin,PWM
import time
import random

interrupt_flag=0
ingame_flag = 0
debounce_time=0

MAX_LEVEL = 100
sequence = []
sound = []
player_sequence = []
buttons_pressed = []
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

def callback_grn(GRN_BTN):
    global interrupt_flag, debounce_time, ingame_flag, buttons_pressed
    if (time.ticks_ms()-debounce_time) > 400:
        interrupt_flag= 1
        debounce_time=time.ticks_ms()
        if ingame_flag == 0:
            ingame_flag = 1
        GRN_LED.toggle()
        buttons_pressed.append(GRN_LED)
        print("grn button pressed")

GRN_BTN.irq(trigger=Pin.IRQ_RISING, handler=callback_grn)

def callback_red(RED_BTN):
    global interrupt_flag, debounce_time, buttons_pressed
    if (time.ticks_ms()-debounce_time) > 400:
        interrupt_flag= 1
        debounce_time=time.ticks_ms()
        RED_LED.toggle()
        buttons_pressed.append(RED_LED)
        print("red button pressed")

RED_BTN.irq(trigger=Pin.IRQ_RISING, handler=callback_red)

def callback_yel(YEL_BTN):
    global interrupt_flag, debounce_time, buttons_pressed
    if (time.ticks_ms()-debounce_time) > 400:
        interrupt_flag= 1
        debounce_time=time.ticks_ms()
        YEL_LED.toggle()
        buttons_pressed.append(YEL_LED)
        print("yel button pressed")

YEL_BTN.irq(trigger=Pin.IRQ_RISING, handler=callback_yel)

def callback_blu(BLU_BTN):
    global interrupt_flag, debounce_time, buttons_pressed
    if (time.ticks_ms()-debounce_time) > 400:
        interrupt_flag= 1
        debounce_time=time.ticks_ms()
        BLU_LED.toggle()
        buttons_pressed.append(BLU_LED)
        print("blu button pressed")

BLU_BTN.irq(trigger=Pin.IRQ_RISING, handler=callback_blu)

def generateSequence():
    global sequence
    sequence = []
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
        
    print(f"level=\'{level}\'")
    
    for i in range(level):
        sequence[i].high()
        #tone(sound[i])
        time.sleep(0.500)
        sequence[i].low()
        time.sleep(0.200)
        

def right_sequence():
    global level, velocity, MAX_LEVEL
    
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
    global level, velocity, ingame_flag
    
    for i in range(4):
        for l in leds:
            l.high()
        time.sleep(0.250)
        
        for l in leds:
            l.low()
        time.sleep(0.250)
        
    level = 1
    ingame_flag = 0
    velocity = 1000
    
def get_sequence():
    global level, player_sequence, sequence, leds, buttons_pressed
    player_sequence = []
    buttons_pressed = []
    i = 0
    while i < level:
        for l in leds:
            l.low()
            
        if len(player_sequence) <= i:
            try:
                player_sequence.append(buttons_pressed.pop(0))
            except:
                time.sleep(1)
            continue
                
        else:
            if player_sequence[i] != sequence[i]:
                wrong_sequence()
                break
            elif i == level-1:
                right_sequence()
                break
                
        i += 1
        

while True:
    if ingame_flag == 1:
        time.sleep(1)
        if level == 1:
            generateSequence()
        show_sequence()
        for l in leds:
            l.low()
        get_sequence()
        continue
    
    
        
    for l in leds:
        l.high()
        time.sleep(0.1)
        l.low()
        if ingame_flag == 1:
            GRN_LED.low()
            break
        
    
        