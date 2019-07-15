import time
import math
import threading
from gpiozero import Motor
from Berry_gpiozero import Movement
from gpiozero import DistanceSensor
from Berry_compass import Compass
from Berry_acceleration import Accelerometer


# Move forward and detect obstacles
def straight(angle):
    speedLeft = 0.6
    speedRight = 0.4
    DeltaS = 0
    minDistance = 30
    distance = ultrasonicSensor.distance*100
    error = 45
    A0 = 0
    V0 = 0
    while distance > minDistance:
        # Go straight
        start = time.time()
        (speedLeft, speedRight) = motors.moveForward(angle, speedLeft, speedRight)
        end = time.time()
        distance = ultrasonicSensor.distance*100
        # Acceleration
        (Ax, Ay) = accelerationSensor.getAcceleration()
        # time.sleep(0.2)
        A = math.sqrt(Ax * Ax + Ay * Ay)
        # Convert to seconds
        t = end - start
        # Velocity
        V = (A0 + A) * t / 2
        # Distance
        S = (V + V0) * t / 2
        V0 = V
        A0 = A
        DeltaS += S * 10000  # Convert from m to cm
    motors.stop()
    return angle, round(DeltaS, 2)


# Check side
def selectSide():
    seconds = 0.3
    print("Inicial angle = ", compass.getAngle())
    # Check Left
    motors.turnLeft(seconds)
    distanceLeft = ultrasonicSensor.distance*100
    print(distanceLeft)
    time.sleep(0.5)
    # Go back
    motors.turnRight(seconds)
    time.sleep(0.5)
    # Check Right
    motors.turnRight(seconds)
    distanceRight = ultrasonicSensor.distance*100
    print(distanceRight)
    time.sleep(0.5)
    # Go back
    motors.turnLeft(seconds)
    time.sleep(0.5)
    # Choose side
    if distanceLeft > distanceRight:
        motors.turnLeft(seconds)
        side = 'Left'
    else:
        motors.turnRight(seconds)
        side = 'Right'
    motors.stop()
    time.sleep(1)
    print("Choose angle = ", compass.getAngle())
    return compass.getAngle(), side


# Go back
def goBack(distance, angle):
    speedLeft = 0.6
    speedRight = 0.4
    DeltaS = 0
    A0 = 0
    V0 = 0
    print("Going back in angle = ", angle)
    while distance > DeltaS:
        # Go straight
        start = time.time()
        (speedLeft, speedRight) = motors.moveForward(angle, speedLeft, speedRight)
        end = time.time()
        # Acceleration
        (Ax, Ay) = accelerationSensor.getAcceleration()
        # time.sleep(0.2)
        A = math.sqrt(Ax * Ax + Ay * Ay)
        # Convert to seconds
        t = end - start
        # Velocity
        V = (A0 + A) * t / 2
        # Distance
        S = (V + V0) * t / 2
        V0 = V
        S0 = S
        A0 = A
        DeltaS += S * 10000  # Convert to cm
        DeltaS = round(DeltaS, 2)
    motors.stop()
    print("Distance = ", DeltaS, "Angle = ", compass.getAngle())


def findPath():
    while True:
        print("SELECT SIDE")
        (angle, side) = selectSide()
        if ultrasonicSensor.distance * 100 < 30:
            break
        sideSelected.append(side)
        print("STRAIGHT")
        (direction, distance) = straight(angle)
        directionVector.append(direction)
        distanceVector.append(distance)


try:
    # Instantiate objects
    compass = Compass()
    motors = Movement()
    accelerationSensor = Accelerometer()
    ultrasonicSensor = DistanceSensor(echo=6, trigger=5, queue_len=1)

    distanceVector = []
    directionVector = []
    sideSelected = []
    while True:
        findPath()
        print(distanceVector)
        print(directionVector)
        # Go back one block
        lastDistance = distanceVector[-1]
        lastDirection = directionVector[-1]
        oppositeAngle = motors.turnBack(lastDirection)
        goBack(lastDistance, oppositeAngle)
        distanceVector.pop(-1)
        directionVector.pop(-1)
        # Go to another side
        unusedAngle = motors.turnBack(lastDirection)
        # MUDAR PARA > 0 PARA FINALIZAR A BUSCA
        # (atualmente segue apenas um lado da posicao inicial)
        if len(selectSide()) > 1:
            print(selectSide())
            if sideSelected[-1] == 'Left':
                motors.turnRight(0.3)
            else:
                motors.turnRight(0.3)
            sideSelected.pop(-1)
        else:
            break

# Reset by pressing CTRL + C
except KeyboardInterrupt:
    print("Measurement stopped by User")
