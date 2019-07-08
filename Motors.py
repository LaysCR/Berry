from gpiozero import Motor
import time
from Berry_compass import Compass

compass = Compass()
seconds = 6
secondsTurn = 0.2

left = Motor(enable=22, forward=23, backward=24)
right = Motor(enable=19, forward=20, backward=21)


def moveFoward():
    error = 90
    stopTurning = time.time() + secondsTurn
    if compass.getAngle() - error < 0:
        while time.time() < stopTurning:
            left.reverse()
            right.forward()
        left.stop()
        right.stop()
    elif compass.getAngle() + error > 360:
        while time.time() < stopTurning:
            left.forward()
            right.reverse()
        left.stop()
        right.stop()

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


try:
    moveFoward()
# Reset by pressing CTRL + C
except KeyboardInterrupt:
    print("Measurement stopped by User")
