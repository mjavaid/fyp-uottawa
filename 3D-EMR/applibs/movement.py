import Adafruit_BBIO.PWM as PWM
from time import sleep

# PLACEHOLDERS: Substitute variables with actual values
TIME_PER_TILE = 2.62 #in sceonds
LEFT_SERVO_TX = "P9_22"
RIGHT_SERVO_TX = "P9_14"
LEFT_SERVO_ON = 0
LEFT_SERVO_OFF = 100
RIGHT_SERVO_ON = 98
RIGHT_SERVO_OFF = 0
DEGREE_TURN_TIME = 0.015
SERVO_FREQUENCY = 33
RIGHT_SERVO_POLARITY = 1
LEFT_SERVO_POLARITY = 0
# END PLACEHOLDERS

RUNNING = False
ENABLED = False

DIRECTIONS = ["FORWARD", "BACKWARDS", "LEFT", "RIGHT"]

def move_forward():
    global ENABLED, RUNNING
    if not ENABLED: return
    PWM.start(LEFT_SERVO_TX, 10, 33, 0)
    PWM.start(RIGHT_SERVO_TX, 98, 33, 1)
    RUNNING = True

def move_backwards():
    if not ENABLED: return
    PWM.start(LEFT_SERVO_TX, 97,33,1)
    PWM.start(RIGHT_SERVO_TX,35,33,0)
    RUNNING = True

def turn_left():
    global ENABLED, RUNNING
    if not ENABLED: return
    PWM.start(LEFT_SERVO_TX, 98,33,1)
    PWM.start(RIGHT_SERVO_TX, 98,33,1)
    RUNNING = True

def turn_right():
    global ENABLED, RUNNING
    if not ENABLED: return
    PWM.start(LEFT_SERVO_TX, 0,33,0)
    PWM.start(RIGHT_SERVO_TX,5,33,0)
    RUNNING = True

def stop():
    global ENABLED, RUNNING
    if not ENABLED: return
    PWM.start(LEFT_SERVO_TX, LEFT_SERVO_OFF,33,0)
    PWM.start(RIGHT_SERVO_TX, RIGHT_SERVO_OFF,33,1)
    RUNNING = False
    
def disable():
    global ENABLED, RUNNING
    if not ENABLED: return
    PWM.stop(LEFT_SERVO_TX)
    PWM.stop(RIGHT_SERVO_TX)
    ENABLED = False
    RUNNING = False
    
def enable():
    global ENABLED, RUNNING   
    if ENABLED: return
    PWM.start(LEFT_SERVO_TX, LEFT_SERVO_OFF, 33, 0)
    PWM.start(RIGHT_SERVO_TX, RIGHT_SERVO_OFF, 33, 1)
    ENABLED = True
    RUNNING = False
    
def executeMovement(ARGS):
    direction = ARGS[0].upper()
    value = int(ARGS[1])
    factor = DEGREE_TURN_TIME
    if direction == "BACKWARDS":
        move_backwards()
        factor = TIME_PER_TILE
    elif direction == "FORWARD":
        move_forward()
        factor = TIME_PER_TILE
    elif direction == "LEFT": 
        turn_left()
        value %= 360
    elif direction == "RIGHT": 
        turn_right()
        value %= 360
    sleep(value * factor)
    stop()
    
if __name__ == "__main__":
    print "movement.py"
    