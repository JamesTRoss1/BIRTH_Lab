from pyfirmata import Arduino, util, Board, Pin
import time 
import traceback
import os 

board = None
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
def controlMotor(channelA, channelB, writeSpeedChannel, writeDirChannel, InitialSpeedMessage, FinalSpeedMessage, InitialDirMessage, FinalDirMessage, numberOfCounts = None, counter = 0, revolution = None, board = None, direct = None):
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
            write(str(FinalSpeedMessage), board, writeSpeedChannel)
            write(str(FinalDirMessage), board, writeDirChannel)
            isDone = True
    	if counter < numberOfCounts:
            if counter == 0:
                write(str(InitialDirMessage), board, writeDirChannel)
                write(str(InitialSpeedMessage), board, writeSpeedChannel)
            aLastState, bLastState, counter = readPosition(channelA=channelA, channelB= channelB,counter=counter, board=board, aLastState = aLastState, bLastState = bLastState, direction = direction)
            print(str(counter))
            time.sleep(.01)
def arduino():
    global board
    board = start("/dev/ttyACM1")
    it = util.Iterator(board)
    it.start()
	#pin_dir = board.get_pin(str("d:9:p"))
	#speed = board.get_pin(str("d:10:p")) 
	#pin_a_encoder = board.get_pin(str("d:2:i"))
	#pin_b_encoder = board.get_pin(str("d:3:i"))
    #pins = [speed, pin_dir, pin_a_encoder, pin_b_encoder]
    #return board, pins
def startPins():
    global board 
    pin_dir = Pin(board, "9", type="DIGITAL")
    pin_dir.mode = "PWM"
    speed = Pin(board, "10", type="DIGITAL")
    speed.mode = "PWM"
    pin_a_encoder = Pin(board, "10", type="DIGITAL")
    pin_a_encoder.mode = "INPUT"
    pin_a_encoder.enable_reporting()
    pin_b_encoder = Pin(board, "2", type="DIGITAL")
    pin_b_encoder.mode = "INPUT"
    pin_b_encoder.enable_reporting()
    pins = [speed, pin_dir, pin_a_encoder, pin_b_encoder]
    return pins 

arduino()
pins = startPins()
controlMotor(pins[2], pins[3], pins[0], pins[1], "1", "0", "1", "0", None, None, 1, board, "1")