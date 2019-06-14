from i2clibraries import i2c_hmc5883l
import threading
import time

class Compass(threading.Thread):
    # Constructor
    def __init__(self):
        hmc5883l = i2c_hmc5883l.i2c_hmc5883l(1)
        hmc5883l.setContinuousMode()
        hmc5883l.setDeclination(-20, 54)
        self.angle = hmc5883l.getHeadingString()
        threading.Thread.__init__(self)

    # Thread
    def run(self):
        aux = 5
        while(aux > 0):
            aux-= 1
            print(self.angle)
            time.sleep(0.5)
