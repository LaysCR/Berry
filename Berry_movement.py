import RPi.GPIO as GPIO
import threading
import time

left = [19, 20, 21]
right = [22, 23, 24]

class Movement(threading.Thread):
    # Constructor
    def __init__(self):
        threading.Thread.__init__(self)

    # Enable pins
    def enablePins(self, ports):
        GPIO.setmode(GPIO.BCM)
        for port in ports:
            GPIO.setup(port, GPIO.OUT)

    # Foward
    def foward(self, side):
        self.enablePins(side)
        GPIO.output(side[0], True)
        GPIO.output(side[1], True)
        GPIO.output(side[2], False)
        
    # Reverse
    def reverse(self, side):
        self.enablePins(side)
        GPIO.output(side[0], True)
        GPIO.output(side[1], False)
        GPIO.output(side[2], True)

    # Movement
    def move(self, direction):
        if(direction == 8):
            self.foward(left)
            self.foward(right)
        elif(direction == 2):
            self.reverse(left)
            self.reverse(right)
        elif(direction == 6):
            self.foward(right)
            self.reverse(left)
        elif(direction == 4):
            self.foward(left)
            self.reverse(right)
        else:
            print("Direcao invalida!!")
        time.sleep(0.2)
        GPIO.cleanup()
    
    # Thread
    def run(self):
        print("foward")
        self.move(8)
        time.sleep(2)
        print("reverse")
        self.move(2)
        time.sleep(2)
        print("left")
        self.move(4)
        time.sleep(2)
        print("right")
        self.move(6)
        time.sleep(2)
        
