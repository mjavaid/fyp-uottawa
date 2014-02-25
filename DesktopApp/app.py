# Main Application File
# Adding a comment!
import sys

sys.path.append('./applibs/')

from gui import createApplication

if __name__ == "__main__":
    app = createApplication()
    app.executeGUI()
