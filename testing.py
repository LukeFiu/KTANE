from machine import Pin, I2C

import time
            
sdaPin =  Pin(20)
sclPin = Pin(21)

i2c = I2C(0,sda=sdaPin, scl = sclPin, freq=400000)
     
# register addresses in port=0, bank=1 mode (easier maths to convert)
MCP23008_BASEADDR     = const(0x20)
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


def doI2CIO8():
    # Lock the I2C device before accessing I2C

    # Initialize the I2CIO-8 card
    initI2CIO8()

    writeMCP23xxxReg(MCP23008_IODIR, 0x00)
   
    ledVal = 0x00
    while True:
        writeLEDs(ledVal)
        time.sleep(0.5)
        ledVal += 1


    
doI2CIO8()
