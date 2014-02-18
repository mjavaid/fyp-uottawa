import Adafruit_BBIO.PWM as PWM
from time import sleep
from itertools import izip

# PLACEHOLDERS: Substitute variables with actual values
TIME_PER_TILE = 10 / 1000
LEFT_SERVO_TX = "P9_22"
RIGHT_SERVO_TX = "P9_14"
LEFT_SERVO_ON = 100
LEFT_SERVO_OFF = 0
RIGHT_SERVO_ON = 0
RIGHT_SERVO_OFF = 100
DEGREE_TURN_TIME = 50 / 1000
SERVO_FREQUENCY = 33
RIGHT_SERVO_POLARITY = 0
LEFT_SERVO_POLARITY = 1
# END PLACEHOLDERS

RUNNING = False
ENABLED = False

DIRECTIONS = ["FORWARD", "BACKWARDS", "LEFT", "RIGHT"]

def move_forward():
    if not ENABLED: return
    PWM.set_duty_cycle(LEFT_SERVO_TX, LEFT_SERVO_ON)
    PWM.set_duty_cycle(RIGHT_SERVO_TX, RIGHT_SERVO_ON)
    RUNNING = True

def move_backwards():
    if not ENABLED: return
    PWM.set_duty_cycle(LEFT_SERVO_TX, LEFT_SERVO_REVERSE_ON)
    PWM.set_duty_cycle(RIGHT_SERVO_TX, RIGHT_SERVO_REVERSE_ON)
    RUNNING = True

def turn_left():
    if not ENABLED: return
    PWM.set_duty_cycle(LEFT_SERVO_TX, LEFT_SERVO_REVERSE_ON)
    PWM.set_duty_cycle(RIGHT_SERVO_TX, RIGHT_SERVO_ON)
    RUNNING = True

def turn_right():
    if not ENABLED: return
    PWM.set_duty_cycle(LEFT_SERVO_TX, LEFT_SERVO_ON)
    PWM.set_duty_cycle(RIGHT_SERVO_TX, RIGHT_SERVO_REVERSE_ON)
    RUNNING = True

def stop():
    if not ENABLED: return
    PWM.set_duty_cycle(LEFT_SERVO_TX, LEFT_SERVO_OFF)
    PWM.set_duty_cycle(RIGHT_SERVO_TX, RIGHT_SERVO_OFF)
    RUNNING = False
    
def disable():
    if not ENABLED: return
    PWM.stop(LEFT_SERVO_TX)
    PWM.stop(RIGHT_SERVO_TX)
    ENABLED = False
    RUNNING = False
    
def enable():
    if ENABLED: return
    PWM.start(LEFT_SERVO_TX, LEFT_SERVO_OFF, SERVO_FREQUENCY, LEFT_SERVO_POLARITY)
    PWN.start(RIGHT_SERVO_TX, RIGHT_SERVO_OFF, SERVO_FREQUENCY, RIGHT_SERVO_POLARITY)
    ENABLED = True
    RUNNING = False

NO_ERR, NO_SUCH_FILE_ERR, INVALID_SYNTAX_ERR = 0, 1, 2
def getPath(filename):
    try:
        f = open(filename, 'r')
    except IOError:
        return NO_SUCH_FILE_ERR
    i = 0
    PATH = []
    for line in f:
        line = line.rstrip()
        if line == '': continue
        if i % 2 == 0:
            if line in DIRECTIONS: 
                PATH.append(line)
            else: 
                f.close()
                return INVALID_SYNTAX_ERR, []
        elif i % 2 == 1:
            try:
                PATH.append(int(line))
            except ValueError:
                f.close()
                return INVALID_SYNTAX_ERR, []
        i += 1
    f.close()
    if len(PATH) % 2 != 0: return INVALID_SYNTAX_ERR, []
    return NO_ERR, PATH

def executePath(path):
    for direction,value in izip(*[iter(path)]*2):
        factor = DEGREE_TURN_TIME
        if direction == "BACKWARDS":
            move_backwards()
            factor = TIME_PER_TILE
        elif direction == "FORWARD":
            move_forward()
            factor = TIME_PER_TILE
        elif direction == "LEFT": turn_left()
        elif direction == "RIGHT": turn_right()
        sleep(value * factor)
        
    
COMMANDS = {
    "LIST": "Lists all the possible commands",
    "ENABLE": "Attaches the servo motors to the PWM library",
    "DISABLE": "Detaches the servo motors from the PWM library",
    "LEFT": "Turns the robot left for provided degrees",
    "RIGHT": "Turns the robot right for provided degrees",
    "FORWARD": "Sets the robot in forward motion for the provided sections",
    "BACKWARDS": "Sets the robot in backwards motion the provided sections",
    "RUN_PATH": "Runs the path specified in the filepath provided as the argument to the command",
    "BREAK": "Exit the program"
}

if __name__ == "__main__":
    # README: Perform polarity, frequency, and duty cycle 
    # testing via command line Python to more efficiently 
    # control the servo
    while True:
        CMD = raw_input("ENTER COMMAND: [LIST = Lists Possible Commands] ").upper()
        if CMD == "LIST":
            print "Available Commands:"
            for command in COMMANDS:
                print "\t%s: %s" % (command, COMMANDS[command])
        if "RUN_PATH" in CMD:
            command, filename = CMD.split(" ")
            error, path = getPath(filename)
            if error == NO_ERR: executePath(path)
            else: print "Error: %s" % error
        if "LEFT" in CMD:
            direction, degrees = CMD.split(" ")
            turn_left()
            sleep(int(degrees) * DEGREE_TURN_TIME)
        if "RIGHT" in CMD:
            direction, degrees = CMD.split(" ")
            turn_right()
            sleep(int(degrees) * DEGREE_TURN_TIME)
        if "FORWARD" in CMD:
            direction, tiles = CMD.split(" ")
            turn_right()
            sleep(int(tiles) * TIME_PER_TILE)
        if "BACKWARDS" in CMD:
            direction, tiles = CMD.split(" ")
            turn_right()
            sleep(int(tiles) * TIME_PER_TILE)
        if CMD == "ENABLE":
            enable()
        if CMD == "DISABLE":
            disable()
        if CMD == "BREAK":
            disable()
            break
