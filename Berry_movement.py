from Berry_compass import Compass
import RPi.GPIO as GPIO
import threading
import time

compass = Compass()
left = [22, 23, 24]
right = [19, 20, 21]
freq = 1.5


class Movement(threading.Thread):

    # Constructor
    def __init__(self):
        threading.Thread.__init__(self)

    # Enable pins
    def enablePins(self, ports):
        GPIO.setmode(GPIO.BCM)
        for port in ports:
            GPIO.setup(port, GPIO.OUT)

    # Forward
    def forward(self, side, speed):
        self.enablePins(side)
        pwm = GPIO.PWM(side[0], freq)
        pwm.start(speed)
        GPIO.output(side[0], True)
        GPIO.output(side[1], True)
        GPIO.output(side[2], False)

    # Reverse
    def reverse(self, side, speed):
        self.enablePins(side)
        pwm = GPIO.PWM(side[0], freq)
        pwm.start(speed)
        GPIO.output(side[0], True)
        GPIO.output(side[1], False)
        GPIO.output(side[2], True)

    # Movement
    def moveForward(self, angle, seconds, speedLeft, speedRight):
        print(angle)
        newAngle = compass.getAngle()
        print("New = ", newAngle)
        stop = time.time() + seconds
        while time.time() < stop:
            if newAngle != angle:
                # Correct to Left
                if newAngle > angle:
                    if speedLeft != 100:
                        speedLeft += 20
                        speedRight -= 20
                # Correct to Right
                else:
                    if speedRight != 100:
                        speedLeft -= 20
                        speedRight += 20
            self.forward(left, speedLeft)
            self.forward(right, speedRight)

        print(speedLeft)
        print(speedRight)
        GPIO.cleanup()
        return speedLeft, speedRight

    def moveLeft(self, seconds):
        stop = time.time() + seconds
        while time.time() < stop:
            self.reverse(left, 60)
            self.forward(right, 40)
        GPIO.cleanup()

    def moveRight(self, seconds):
        stop = time.time() + seconds
        while time.time() < stop:
            self.forward(left, 60)
            self.reverse(right, 40)
        GPIO.cleanup()

    # Thread
    def run(self):
        print("right")
        self.move(6)
        time.sleep(2)


# try:
#     while True:
#         motors = Movement()
#         motors.forward(left, 0)
#         motors.forward(right, 0)
#
# except KeyboardInterrupt:
#     print("Measurement stopped by User")
#     GPIO.cleanup()
