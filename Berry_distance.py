import RPi.GPIO as GPIO
import time
import threading

GPIO_TRIGGER = 5
GPIO_ECHO = 6

class Distance(threading.Thread):
    # Constructor
    def __init__(self):
        threading.Thread.__init__(self)

    def setPins(self):
        #GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)
        # Set GPIO direction (IN/ OUT)
        GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(GPIO_ECHO, GPIO.IN)
        
    def getDistance(self):
        self.setPins()
        # set Trigger to HIGH
        GPIO.output(GPIO_TRIGGER, True)
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)
        StartTime = time.time()
        StopTime = time.time()
        # save StartTime
        while GPIO.input(GPIO_ECHO) == 0:
            StartTime = time.time()
        # save time of arrival
        while GPIO.input(GPIO_ECHO) == 1:
            StopTime = time.time()
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
        GPIO.cleanup()
        return distance

    # Thread
    def run(self):
        aux = 5
        while(aux > 0):
            aux-= 1
            dist = self.getDistance()
            print ("Distance = %1.f cm" % dist)
            time.sleep(0.5)
