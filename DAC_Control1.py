from pyfirmata import Arduino, util
import time 
import traceback
import os 
board = None 
pin_dir = None
speed = None 
pin_a_encoder = None
pin_b_encoder = None
def start(path):
    board = Arduino(str(path))
    return board 

def read(pin, board):
    try:
        data = pin.read()
        return str(data) 
    except Exception:
        traceback.print_exc()
        return "Unable to read data from Arduino"
        
def write(message, board, pin):
    try:
        pin.write(float(str(message)))
        return "Successfully wrote data to Arduino"
    except Exception:
    	traceback.print_exc()
#This method takes a channelA and channelB to listen on; if there is a change it records the change as either a 1 or -1. No change is defined as a 0. 
#Takes optional parameter to define aLastState
#Returns two integers with the first being the rotation and the second being a counter 
def readPosition(channelA = None, channelB = None, counter = 0, aLastState = None, board = None, bLastState = None, direction = None):
    aState = str(read(channelA, board))
    bState = str(read(channelB, board))
    #Not Updated
    try:
        if(aState != aLastState or bState != bLastState):
            if int(direction) == 1:
                counter = counter + 1
            if int(direction) == 0:
          	   counter = counter - 1
    except Exception:
        pass  
    finally: 
        aLastState = str(read(channelA, board))
        bLastState = str(read(channelB, board))
        return aLastState, bLastState, counter
#Motor Control
#pin 2 and 3 encoder; input; digital
def controlMotor(channelA, channelB, writeChannel, message, numberOfCounts = None, counter = 0, revolution = None, board = None, direct = None):
    #Has not reached desired rotation
    fullCycle = int(34607 / 2)
    counter = 0
    isDone = False
    aLastState = None
    bLastState = None
    direction = direct
    if numberOfCounts is None: 
        numberOfCounts = float(revolution) * fullCycle  
    while not(isDone):
    	if abs(counter) >= numberOfCounts:
            write(str(message), board, writeChannel)
            isDone = True
    	if counter < numberOfCounts:
            aLastState, bLastState, counter = readPosition(channelA=channelA, channelB= channelB,counter=counter, board=board, aLastState = aLastState, bLastState = bLastState, direction = direction)
            print(str(counter))
def initialize():
    global board, pin_dir, speed, pin_a_encoder, pin_b_encoder
    board = start("/dev/ttyACM0")
    it = util.Iterator(board)
    it.start()
    pin_dir = board.get_pin(str("d:9:p"))
    speed = board.get_pin(str("d:10:p")) 
    pin_a_encoder = board.get_pin(str("d:2:i"))
    pin_b_encoder = board.get_pin(str("d:3:i"))
#0 is counter clockwise; 1 is clockwise 
speedVar = str(input("Speed: ")).strip()
dirVar = str(input("Direction: ")).strip()
initialize()
write(speedVar, board, speed)
write(dirVar, board, pin_dir)
controlMotor(pin_a_encoder, pin_b_encoder, speed, "0", None, None, 1, board, int(dirVar))
