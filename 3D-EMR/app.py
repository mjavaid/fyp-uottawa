import sys

sys.path.append('./applibs/')

def run():
    from common import SERVER_CONSTANTS
    
    a = SERVER_CONSTANTS()
    print a.HOST, a.PORT

if __name__ == "__main__":
    print "app.py"
    run()
    