from i2clibraries import i2c_adxl345
import threading
import time
from os import system


class Accelerometer(threading.Thread):
    # Constructor
    def __init__(self):
        self.adxl345 = i2c_adxl345.i2c_adxl345(1)
        self.adxl345.setScale(16)
        threading.Thread.__init__(self)

    # Get Acceleration
    def getAcceleration(self):
        self.adxl345.setOption(0x1E, 47)
        self.adxl345.setOption(0x1F, 230)
        self.adxl345.setOption(0x20, 229)
        # print(self.adxl345.getOptions(0x1E))
        # print(self.adxl345.getOptions(0x1F))
        # print(self.adxl345.getOptions(0x20))
        (x, y, z) = self.adxl345.getAxes()
        # Convert from G's to m/s2
        x = round(x*9.81, 2)
        y = round(y*9.81, 2)
        z = round(z*9.81, 2)

        return x, y

    # Thread
    def run(self):
        while True:
            print(self.getAcceleration())
            time.sleep(1)

#
# try:
#     accelerometer = Accelerometer()
#     while True:
#         print("Axes", accelerometer.getAcceleration())
#         time.sleep(0.3)
#         system('clear')
#         # print("Correction", accelerometer.setCorrection())
#
# except KeyboardInterrupt:
#     print("Measurement stopped by User")
#     GPIO.cleanup()
