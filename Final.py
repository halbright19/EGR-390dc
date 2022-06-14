import pyfirmata
import os # Used for keyboard interrupt
from led_matrix import LedMatrix # "Library" written by Sawyer McLane

board = pyfirmata.Arduino('COM3') # Set up board

# Start iterator to receive input data
it = pyfirmata.util.Iterator(board)
it.start()

# Control pins
button = board.get_pin('d:2:i') # For resetting
pot = board.get_pin('a:2:i') # Potentiometer for setting/switching mode 

# Joystick
vrX = board.get_pin('a:0:i')
vrY = board.get_pin('a:1:i')

# 8 X 8 LED Module
dataIn = 12
load = 11
clock = 10
maxInUse = 1
matrix = LedMatrix(board, dataIn, load, clock) # Initlizes pins
matrix.setup()

xMat = 1
yMat = 1
# https://stackoverflow.com/questions/18449136/initialize-empty-matrix-in-python
mat = [ [ 0 for i in range(8) ] for j in range(8) ] # 8 by 8 matrix

def incrementVal(val, clear):
    if val < 8:  # Prevents val from exceeding 8
        val += 1
        if clear: # Clear if in move point mode and val changes
            matrix.clear()
    return val

def decrementVal(val, clear): 
    if val > 1: # Prevents val from going below 1
        val -= 1
        if clear: # Clear if in move point mode and val changes
            matrix.clear()
    return val

def reset(): # Sets dot position to upper left
    matrix.clear()
    global xMat, yMat, mat
    xMat = 1 
    yMat = 1
    mat = [ [ 0 for i in range(8) ] for j in range(8) ]
    mat[0][7] = 1
          
def main(oldMode): #True -> move point, False -> sketch
    global xMat, yMat, mat
    while True:
        if (button.read()): # Reset on button press
            reset()
        potVal = pot.read() # Allows user to change operating mode
        if (potVal < .25): # Pot turned to right
            mode = False; # Sketch (has memory, like an Etch A Sketch)
        elif (potVal > .75): # Pot turned to left
            mode = True # Move point
        if (mode != oldMode): # Calls reset only on mode change
            oldMode = mode # Updates old mode with current mode
            reset()
        x = vrX.read() # Reads joystick x value
        y = vrY.read() #Reads joystick y value
        if (type(x) is not None and y is not None): # Prevents none type error
            if (abs(x-0.5) > abs(y-0.5)): # Horizontal
                if (x > .75): # Right
                    xMat = incrementVal(xMat, mode)
                elif (x < 0.25): # Left
                    xMat = decrementVal(xMat, mode)
            else: # Vertical
                 if (y < .25): # Up
                    yMat = decrementVal(yMat, mode)
                 elif (y > .75): # Down
                    yMat = incrementVal(yMat, mode)
            if mode: # Move point mode
                matrix.maxSingle(xMat, int(2**(yMat-1))) # Draws single point to matrix
            else: # Sketch mode
                mat[xMat-1][8-yMat] = 1 # Rotation 90 degrees counter clockwise 
                matrix.draw_matrix(mat) # Draws entire matrix stored in mat
            
try:
    potVal = pot.read() # Reads potentiometer
    if (potVal < .25): # Pot turned to right
        oldMode = False; # Sketch (has memory, like an Etch A Sketch) 
    elif (potVal > .75): # Pot turned to left
        oldMode = True # Move point
    main(potVal) # Move point
        
except KeyboardInterrupt: # Allows user to quit with ctrl+C
    board.exit()
    os._exit(1)