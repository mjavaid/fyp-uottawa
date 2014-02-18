import Adafruit_BBIO.PWM as PWM
from time import sleep

# PLACEHOLDERS: Substitute variables with actual values
CAMERA_SERVO_TX = "P9_14"
SERVO_REVERSE_ON = 5
SERVO_ON = 100
SERVO_OFF = 0
DEGREE_TURN_TIME = 50 / 1000
RESET_TIME = 
SERVO_FREQUENCY = 33
SERVO_POLARITY = 0
# END PLACEHOLDERS

DEGREES_TURNED = 0
ENABLED = False

def turn(DEGREES_TO_TURN=1):
    if not ENABLED: enable()
    PWM.set_duty_cycle(CAMERA_SERVO_TX, SERVO_ON)
    sleep(DEGREES_TO_TURN * DEGREE_TURN_TIME)
    PWM.set_duty_cycle(CAMERA_SERVO_TX, SERVO_OFF)
    DEGREES_TURNED += DEGREES_TO_TURN
    
def reset():
    if not ENABLED:
        if DEGREES_TURNED == 0: return
        else: enable()
    PWM.set_duty_cycle(CAMERA_SERVO_TX, SERVO_REVERSE_ON)
    sleep(DEGREES_TURNED * DEGREE_TURN_TIME)
    PWM.set_duty_cycle(CAMERA_SERVO_TX, SERVO_OFF)
    DEGREES_TURNED = 0

def enable():
    if ENABLED: return
    # Initialize Servo to OFF state
    PWM.start(CAMERA_SERVO_TX, SERVO_OFF, SERVO_FREQUENCY, SERVO_POLARITY)
    STARTED = True

def disable():
    if not ENABLED: return
    PWM.stop(CAMERA_SERVO_TX)

COMMANDS = {
    "LIST": "Lists all the possible commands",
    "ENABLE": "Attaches the servo motor to the PWM library",
    "DISABLE": "Detaches the servo motor from the PWM library",
    "TURN": "Turns the servo motor by the specified amount of degress",
    "RESET": "Resets the servo motor to the default position",
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
        if CMD == "RESET":
            reset()
        if CMD == "TURN":
            turn()
        if CMD == "ENABLE":
            enable()
        if CMD == "DISABLE":
            disable()
        if CMD == "BREAK":
            disable()
            break
