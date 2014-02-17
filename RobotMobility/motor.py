import Adafruit_BBIO.PWM as PWM

RUNNING = False
STARTED = False

def stop():
    print "Stopping Motors...\n"
    PWM.set_duty_cycle("P9_14",0)
    PWM.set_duty_cycle("P9_22",100)

def start():
    global RUNNING, STARTED
    RUNNING = True
    print "Starting Motors...\n"
    if STARTED:
        PWM.set_duty_cycle("P9_14",97)
        PWM.set_duty_cycle("P9_22",5)
    else:
        STARTED = True
        PWM.start("P9_22",5,33,0)
        PWM.start("P9_14",97,33,1)

if __name__ == "__main__":
    while True:
	userInput = str(raw_input("Enter Command: "))
        userInput = userInput.upper()
        if userInput == "BREAK":
            stop()
            break
        elif userInput == "START":
            if RUNNING:
                print "Already Running!\n" 
                continue
            start()
        elif userInput == "STOP":
            if not STARTED:
                print "Start Motors First Doofus!\n"
                continue
            if not RUNNING: 
                print "Already Stopped!\n"
                continue
            RUNNING = False
            stop()
        else: print "Invalid Command!\n"

