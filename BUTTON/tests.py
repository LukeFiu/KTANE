# PiicoDev SSD1306 demo code
# Show off some features of the PiicoDev OLED driver

import math
from PiicoDev_SSD1306 import *
from PiicoDev_Unified import sleep_ms


sdaPin = Pin(26)
sclPin = Pin(27)
display = create_PiicoDev_SSD1306(bus = 1, sda=sdaPin, scl=sclPin)
word = "Hellooooooo"

while True:
    display.fill(0)
    
    # show the collision count
    display.text(word,64-(len(word)*4),32, 1)
    display.show()
    sleep_ms(10)
