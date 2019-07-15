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

    # Stop motors
    def stop(self):
        left.stop()
        right.stop()

    # Go Forward
    def moveForward(self, angle, speedLeft, speedRight):
        left.forward(speedLeft)
        right.forward(speedRight)
        ###########################################
        case = None
        limit = None
        error = 100
        # Special cases
        if angle - error < 0:
            case = 1
            limit = 360 + (angle - error)
        elif angle + error > 359:
            case = 2
            limit = (angle + error) - 360
        else:
            case = 0
        ###########################################
        newAngle = compass.getAngle()
        if newAngle != angle:
            # Regular cases
            if case == 0:
                # Correct to Left
                if newAngle > angle:
                    speedLeft = 0.5
                    speedRight = 0.1
                # Correct to Right
                else:
                    speedLeft = 0.1
                    speedRight = 0.5
            # Special cases
            elif case == 1:
                # Correct to Left
                if limit < newAngle < 359:
                    speedLeft = 0.1
                    speedRight = 0.5
                elif 0 < newAngle < angle:
                    speedLeft = 0.1
                    speedRight = 0.5
                # Correct to Right
                else:
                    speedLeft = 0.5
                    speedRight = 0.1
            elif case == 2:
                # Correct to Right
                if 0 < newAngle < limit:
                    speedLeft = 0.5
                    speedRight = 0.1
                elif angle < newAngle < 359:
                    speedLeft = 0.5
                    speedRight = 0.1
                # Correct to Left
                else:
                    speedLeft = 0.1
                    speedRight = 0.5

            speedLeft = round(speedLeft, 2)
            speedRight = round(speedRight, 2)

        return speedLeft, speedRight

    # Turn Left
    def turnLeft(self, secondsTurn):
        print("Turning Left ")
        stop = time.time() + secondsTurn
        while time.time() < stop:
            left.backward(0.6)
            right.forward(0.4)
            # time.sleep(secondsTurn)
        self.stop()

    # Turn Right
    def turnRight(self, secondsTurn):
        print("Turning Right ")
        stop = time.time() + secondsTurn
        while time.time() < stop:
            left.forward(0.6)
            right.backward(0.4)
            # time.sleep(secondsTurn)
        self.stop()

    # Turn Back
    def turnBack(self, angle):
        print("Turning back from ", angle)
        newAngle = angle
        back = - 55
        aux = 105
        while not back - 50 < newAngle < back + 50:
            if angle < 180:
                back = angle + aux
                self.turnLeft(0.2)
            else:
                back = angle - aux
                self.turnRight(0.2)
            newAngle = compass.getAngle()
            print(newAngle)
            time.sleep(1)
        self.stop()
        print("GOAL = ", back)
        return back

    # Thread
    def run(self):
        try:
            moveForward(seconds)
        # Reset by pressing CTRL + C
        except KeyboardInterrupt:
            print("Measurement stopped by User")

#
# try:
#     motors = Movement()
#     angle = compass.getAngle()
#     motors.turnBack(angle)
#
# except KeyboardInterrupt:
#     print("Measurement stopped by User")

