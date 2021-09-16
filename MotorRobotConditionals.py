#file determines if motor has to activate to correct path errors 
#Written By James Ross 
import DAC_Control1
#Distance away from needle
robotDistance = None
#Distance of rope dispensed 
motorDistance = None
tension = None 
tether = None
desiredTether = None
desiredTension = None

def main():
    #determines how much to move by in given cycle 
    load_cell = DAC_Control1.getLoadCell()
    robot_correction = 1
    #determines the range of values allowed  
    robot_precision = 1
    #determines how much to move by in given cycle 
    motor_correction = 1
    #determines the range of values allowed  
    motor_precision = 1
    if(desiredTension < tension - robot_precision):
        robotDistance = robotDistance + robot_correction
    elif(desiredTension > tension + robot_precision):
        robotDistance = robotDistance - robot_correction
    else:
        pass
    if(desiredTether < tether - motor_precision):
        motorDistance = motorDistance - motor_correction
    elif(desiredTether > tether + motor_precision):
        motorDistance = motorDistance + motor_correction
    else:
        pass 
    return motorDistance, robotDistance

if __name__ == "__main__":
    main()