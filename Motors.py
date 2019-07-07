from gpiozero import Motor
import time
from Berry_compass import Compass

compass = Compass()
seconds = 4

left = Motor(enable=22, forward=23, backward=24)
right = Motor(enable=19, forward=20, backward=21)


def moveFoward():

    stop = time.time() + seconds
    angle = compass.getAngle()
    print("INICIAL = ", angle)
    speedLeft = 0.5
    speedRight = 0.5
    error = 10
    limit = 0
    correction = False

    while time.time() < stop:
        print(speedLeft)
        print(speedRight)
        newAngle = compass.getAngle()
        print("NOVO INICIAL = ", newAngle)
        if newAngle != angle:
            # Look for special condition
            if newAngle + error > 360:
                correction = True
                limit = abs(360 - (newAngle + error))
            elif newAngle - error < 0:
                correction = True
                limit = 360 - abs(newAngle - error)
            # Regular condition
            if correction is False:
                # Correct to Left
                if newAngle > angle:
                    if speedLeft == 0.9:
                        continue
                    else:
                        speedLeft += 0.1
                        speedRight -= 0.1
                # Correct to Right
                else:
                    if speedRight == 0.9:
                        continue
                    else:
                        speedLeft -= 0.1
                        speedRight += 0.1
            # Special condition
            else:
                # Correct to Left
                if limit > 0:
                    if speedLeft == 0.9:
                        continue
                    else:
                        speedLeft += 0.1
                        speedRight -= 0.1
                # Correct to Right
                elif limit < 360:
                    if speedRight == 0.9:
                        continue
                    else:
                        speedLeft -= 0.1
                        speedRight += 0.1

        speedLeft = round(speedLeft, 2)
        speedRight= round(speedRight, 2)
        left.forward(speedLeft)
        right.forward(speedRight)
        angle = compass.getAngle()
        print("ANGULO FINAL = ", angle)
        time.sleep(0.5)


moveFoward()
