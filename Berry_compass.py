from i2clibraries import i2c_hmc5883l
import threading
import time

class Compass(threading.Thread):
    # Constructor
    def __init__(self):
        self.hmc5883l = i2c_hmc5883l.i2c_hmc5883l(1)
        self.hmc5883l.setContinuousMode()
        self.hmc5883l.setDeclination(-20, 54)
        threading.Thread.__init__(self)

    # Get Headings
    def getAngle(self):
        (angle, minutes)= self.hmc5883l.getHeading()
        return angle
    
    # Thread
    def run(self):
        aux = 5
        while(aux > 0):
            aux-= 1
            (angle, minutes)= self.hmc5883l.getHeading()
            print(angle)
            time.sleep(1)
