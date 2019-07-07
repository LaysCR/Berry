from gpiozero import Motor
import time
from Berry_compass import Compass

compass = Compass()
seconds = 2

left = Motor(enable=22, forward=23, backward=24)
right = Motor(enable=19, forward=20, backward=21)


def moveFoward():

    stop = time.time() + seconds
    angle = compass.getAngle()
    print("INICIAL = ", angle)
    speedLeft = 0.6
    speedRight = 0.4
    error = 10
    limit = 0
    correction = False

    while time.time() < stop:
        print(speedLeft)
        print(speedRight)
        left.forward(speedLeft)
        right.forward(speedRight)
        newAngle = compass.getAngle()
        print("NOVO INICIAL = ", newAngle)
        if newAngle != angle:
            # Look for special condition
            if angle + error > 360:
                correction = True
                limit = abs(360 - (angle + error))
                print(limit)
            elif angle - error < 0:
                correction = True
                limit = 360 - abs(angle - error)
                print(limit)
            # Regular condition
            if correction is False:
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
            # Special condition
            else:
                # Correct to Left
                if limit < newAngle < angle or newAngle > limit > angle or limit > angle > newAngle:
                    print("ESQUERDA", limit)
                    if speedRight != 0.9:
                        speedLeft -= 0.1
                        speedRight += 0.1
                # Correct to Right
                elif limit < angle < newAngle or angle < newAngle < limit or newAngle < limit < angle:
                    print("DIREITA", limit)
                    if speedLeft != 0.9:
                        speedLeft += 0.1
                        speedRight -= 0.1

        left.stop()
        right.stop()
        speedLeft = round(speedLeft, 2)
        speedRight= round(speedRight, 2)
        angle = compass.getAngle()
        print("ANGULO FINAL = ", angle)
        # time.sleep(2)


try:
    moveFoward()
# Reset by pressing CTRL + C
except KeyboardInterrupt:
    print("Measurement stopped by User")