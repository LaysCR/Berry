import time
import threading
from gpiozero import Motor
from Berry_compass import Compass

compass = Compass()

left = Motor(enable=22, forward=23, backward=24)
right = Motor(enable=19, forward=20, backward=21)


class Movement(threading.Thread):
    # Constructor
    def __init__(self):
        threading.Thread.__init__(self)

    # Go Forward
    def moveForward(self, angle, speedLeft, speedRight):
        left.forward(speedLeft)
        right.forward(speedRight)
        newAngle = compass.getAngle()
        if newAngle != angle:
            # Correct to Left
            if newAngle > angle:
                if speedLeft < 1:
                    speedLeft += 0.1
                    speedRight -= 0.1
            # Correct to Right
            else:
                if speedRight < 1:
                    speedLeft -= 0.1
                    speedRight += 0.1
            speedLeft = round(speedLeft, 2)
            speedRight = round(speedRight, 2)
        return speedLeft, speedRight

    # Turn Left
    def turnLeft(self, secondsTurn):
        stopTurning = time.time() + secondsTurn
        while time.time() < stopTurning:
            left.backward()
            right.forward()
        left.stop()
        right.stop()

    # Turn Right
    def turnRight(self, secondsTurn):
        stopTurning = time.time() + secondsTurn
        while time.time() < stopTurning:
            left.forward()
            right.backward()
        left.stop()
        right.stop()

    # Thread
    def run(self):
        try:
            moveForward(seconds)
        # Reset by pressing CTRL + C
        except KeyboardInterrupt:
            print("Measurement stopped by User")


# try:
#     motors = Movement()
#     accelerationSensor = Accelerometer()
#
#     motors.moveForward(compass.getAngle())
#
# except KeyboardInterrupt:
#     print("Measurement stopped by User")
#     GPIO.cleanup()
