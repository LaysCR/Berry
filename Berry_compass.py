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

    # Get Acceleration
    def getAxes(self):
        axes = self.hmc5883l.getAxes()
        return axes

    # Thread
    def run(self):
        while(True):
            (angle, minutes)= self.hmc5883l.getHeading()
            print(angle)
            time.sleep(1)

#
# try:
#     compass = Compass()
#     while True:
#         print(compass.getAngle())
#         time.sleep(1)
#
# except KeyboardInterrupt:
#     print("Measurement stopped by User")
