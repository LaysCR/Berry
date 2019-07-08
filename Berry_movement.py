from gpiozero import Motor
import threading
import time
from Berry_compass import Compass

compass = Compass()
seconds = 4
secondsTurn = 0.5

left = Motor(enable=22, forward=23, backward=24)
right = Motor(enable=19, forward=20, backward=21)

class Movement(threading.Thread):
    # Constructor
    def __init__(self):
        threading.Thread.__init__(self)

    # Go Forward
    def moveForward(self, seconds):
        error = 90
        if compass.getAngle() - error < 0:
            # Turn Left
            turnLeft(secondsTurn)
        elif compass.getAngle() + error > 360:
            # Turn Right
            turnRight(secondsTurn)

        speedLeft = 0.6
        speedRight = 0.4
        angle = compass.getAngle()
        stop = time.time() + seconds
        while time.time() < stop:
            left.forward(speedLeft)
            right.forward(speedRight)
            newAngle = compass.getAngle()
            if newAngle != angle:
                # Correct to Left
                if newAngle > angle:
                    if speedLeft != 0.9:
                        speedLeft += 0.1
                        speedRight -= 0.1
                # Correct to Right
                else:
                    if speedRight != 0.9:
                        speedLeft -= 0.1
                        speedRight += 0.1

                speedLeft = round(speedLeft, 2)
                speedRight = round(speedRight, 2)
        left.stop()
        right.stop()

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
            turnLeft(secondsTurn)
            turnRight(secondsTurn)
            turnRight(secondsTurn)
            turnLeft(secondsTurn)
        # Reset by pressing CTRL + C
        except KeyboardInterrupt:
            print("Measurement stopped by User")