from pyfirmata import Arduino, util

def start(path):
    board = Arduino(str(path))
    it = util.Iterator(board)
    it.start()
    return board 

def read(channel, board):
    try:
        data = board.get_pin(str(channel))
        return str(data.read())
    except Exception:
        return "Unable to read data from Arduino"
def write(channel, message, board):
    try:
        pin = board.get_pin(str(channel))
        pin.write(int(str(message)))
        return "Successfully wrote data to Arduino"
    except Exception:
        return "Unable to write data to Arduino"
        
#This method takes a channelA and channelB to listen on; if there is a change it records the change as either a 1 or -1. No change is defined as a 0. 
#Takes optional parameter to define aLastState
#Returns two integers with the first being the rotation and the second being a counter 
def readPosition(channelA, channelB, counter = 0, aLastState = None, board = None):
    aState = int(read(str(channelA)))
    #Not Updated
    try:
        if(aState == aLastState):
            return 0 + counter
        #Updated  
        else:
            #Rotating Clockwise; defined as 1 
            if(aState != int(read(str(channelB), board))):
                return 1 + counter
            #Rotating Counterclockwise if equal; defined as -1
            else: 
                return -1 + counter
    except Exception:
        pass  
    finally: 
        aLastState = int(read(str(channelA), board))
#Motor Control
def controlMotor(channelA, channelB, writeChannel, message, numberOfCounts = None, counter = 0, revolution = None, board = None):
    #Has not reached desired rotation
    fullCycle = 34607
    if numberOfCounts == None: 
        numberOfCounts = float(revolution) * fullCycle  
    if counter < numberOfCounts:
        counter = readPosition(channelA=channelA, channelB= channelB, counter=counter, board=board)
    #Reached Desired Rotation
    else:
        write(str(writeChannel), int(message), board)

