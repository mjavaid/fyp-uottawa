# Main Application File

import sys

sys.path.append('./applibs/')

from gui import APPLICATION

if __name__ == "__main__":
    app = APPLICATION()
    app.executeGUI()
