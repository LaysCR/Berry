from gpiozero import Motor
import time
from Berry_compass import Compass

compass = Compass()
seconds = 5

left = Motor(enable=22, forward=23, backward=24)
right = Motor(enable=19, forward=20, backward=21)

stop = time.time() + seconds
angle = compass.getAngle()
speedLeft = 0.5
speedRight = 0.5
while time.time() < stop:
    print(speedLeft)
    print(speedRight)
    if compass.getAngle() != angle:
        if compass.getAngle() > angle:
            if speedLeft == 0.9:
                continue
            else:
                speedLeft += 0.1
                speedRight -= 0.1
        else:
            if speedRight == 0.1:
                continue
            else:
                speedLeft -= 0.1
                speedRight += 0.1
    print(angle)
    speedLeft = round(speedLeft, 2)
    speedRight= round(speedRight, 2)
    # left.forward(speedLeft)
    # right.forward(speedRight)
    angle = compass.getAngle()
    time.sleep(0.5)