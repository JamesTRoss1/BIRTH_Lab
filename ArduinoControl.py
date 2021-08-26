from pyfirmata import Arduino, util
import time 
import traceback
import os 
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
def readPosition(channelA, channelB, counter = 0, aLastState = None, board = None, bLastState = None, direction = None):
    aState = str(read(channelA, board))
    bState = str(read(channelB, board))
    try:
        if aState != aLastState or bState != bLastState:
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
    fullCycle = 34607 / 2
    counter = 0
    isDone = False
    aLastState = None
    bLastState = None
    direction = direct
    if numberOfCounts is None: 
        numberOfCounts = float(revolution) * fullCycle  
        print(numberOfCounts)
    print(str(counter))
    while not(isDone):
    	if abs(counter) >= numberOfCounts:
		    write(str(message), board, writeChannel)
		    isDone = True
    	if counter < numberOfCounts:
		    aLastState, bLastState, counter = readPosition(channelA=channelA, channelB= channelB,counter=counter, board=board, aLastState = aLastState, bLastState = bLastState, direction = direction)
		    print(str(counter))
		    time.sleep(.01)
board = start("/dev/ttyACM1")
print("Board Connected")
it = util.Iterator(board)
it.start()
pin_dir = board.get_pin(str("d:9:p"))
speed = board.get_pin(str("d:10:p")) 
pin_a_encoder = board.get_pin(str("d:2:i"))
pin_b_encoder = board.get_pin(str("d:3:i"))
write("0", board, pin_dir)
write("0", board, speed) 
time.sleep(2)
write("1", board, pin_dir)
direct = 1
write("1", board, speed)
controlMotor(pin_a_encoder, pin_b_encoder, speed, "0", None, None, 1, board, direct)