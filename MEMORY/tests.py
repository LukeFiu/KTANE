# Initialising all the required libraries
import board
import busio
from digitalio import Direction
from adafruit_mcp230xx.mcp23008 import MCP23008
i2c = busio.I2C(board.SCL, board.SDA)
# Adding the MCP23008
mcp = MCP23008(i2c)
# This assumes that you are using the default address [ i.e. all address 
# pins are grounded]
#
#
#
# Defining two outputs on pins 0 and 1
pin0 = mcp.get_pin(0)
pin0.direction = Direction.OUTPUT
pin1 = mcp.get_pin(1)
pin1.direction = Direction.OUTPUT
#
#
# We can now control the pins by setting them to true or false, true being 
# high
pin0.value = True
pin1.value = True
#
# and switch them off again by using
pin0.value = False
pin1.value = False
#
#
# We can also use the pins as inputs.
# We will activate the internal pullup as well
#
# first , we need another library
import digitalio
pin2 = mcp.get_pin(2)
pin2.direction = digitalio.Direction.INPUT
pin2.pull = digitalio.Pull.UP
#
#
# Reading the pin value is now as easy as 
pin2.value
#
# This will return True if the pin is high ( its default state with pullups # activated, of False if pulled low, by for example a switch of button )