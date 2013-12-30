import gui
from sys import version_info

if __name__ == "__main__":
    req_version = (2,7)
    cur_version = version_info
    if req_version <= cur_version:
        app = gui.createApp([None, None])
        app.runGUI()
    else:
        print "Python 2.7 required to run application!"
