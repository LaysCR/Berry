import RPi.GPIO as GPIO
import pigpio
import threading
import time
from Berry_distance import Distance

left = [19, 20, 21]     # RIGHT
right = [22, 23, 24]    # LEFT
freq = 10000
pi = pigpio.pi()

class Movement(threading.Thread):
    # Constructor
    def __init__(self):
        threading.Thread.__init__(self)

    # Enable pins
    def enablePins(self, ports):
        GPIO.setmode(GPIO.BCM)
        for port in ports:
            GPIO.setup(port, GPIO.OUT)

# pi.set_PWM_dutycycle(4,   0) # PWM off
# pi.set_PWM_dutycycle(4,  64) # PWM 1/4 on
# pi.set_PWM_dutycycle(4, 128) # PWM 1/2 on
# pi.set_PWM_dutycycle(4, 192) # PWM 3/4 on
# pi.set_PWM_dutycycle(4, 255) # PWM full on

    # Foward
    def foward(self, side):
        self.enablePins(side)
        if side == left: #RIGHT
            # pi.set_PWM_dutycycle(19, 255)
            pwmLeft = GPIO.PWM(19, freq)
            pwmLeft.ChangeDutyCycle(100)
        elif side == right:  #LEFT
            # pi.set_PWM_dutycycle(22, 128)
            pwmRight = GPIO.PWM(22, freq)
            pwmRight.ChangeDutyCycle(10)
        GPIO.output(side[0], True)
        GPIO.output(side[1], True)
        GPIO.output(side[2], False)

    # Reverse
    def reverse(self, side):
        self.enablePins(side)
        # if side == left:
        #     pwmLeft = GPIO.PWM(19, freq)
        #     pwmLeft.ChangeDutyCycle(100)
        # elif side == right:
        #     pwmRight = GPIO.PWM(22, freq)
        #     pwmRight.ChangeDutyCycle(10)
        GPIO.output(side[0], True)
        GPIO.output(side[1], False)
        GPIO.output(side[2], True)

    # Movement
    def move(self, direction, seconds):
        stop = time.time() + seconds
        while(time.time() < stop):
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
#        time.sleep(0.2)
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
