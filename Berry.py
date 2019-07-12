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
    minDistance = 20
    distance = ultrasonicSensor.distance*100
    error = 45
    i = -1
    A0 = 0
    V0 = 0
    S0 = 0
    ttotal = 0
    while distance > minDistance:
        i += 1
        # Prevent angle errors
        if angle - error < 0:
            # Turn Left
            motors.turnLeft(0.2)
            angle = compass.getAngle()
        elif angle + error > 360:
            # Turn Right
            motors.turnRight(0.2)
            angle = compass.getAngle()
        # Go straight
        start = time.time()
        (speedLeft, speedRight) = motors.moveForward(angle, speedLeft, speedRight)
        end = time.time()
        # Acceleration
        (Ax, Ay) = accelerationSensor.getAcceleration()
        distance = ultrasonicSensor.distance*100
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
        ttotal += t
        DeltaS += S * 10000  # Convert from m to cm
    print(ttotal)
    return DeltaS


# Check side
def selectSide(side, seconds):
    angle = gyroscopeSensor.getAngle()
    #    print("Angle = %d" % angle)
    motors.move(side, seconds)
    distance = ultrasonicSensor.getDistance()
    #    print(distance)
    angle = gyroscopeSensor.getAngle()
    #    print("Angle = %d" % angle)
    time.sleep(0.5)
    return distance, angle


try:
    # Instantiate objects
    compass = Compass()
    motors = Movement()
    accelerationSensor = Accelerometer()
    ultrasonicSensor = DistanceSensor(echo=6, trigger=5, queue_len=1)

    D = straight(compass.getAngle())
    print(D)

#    iterations = 5
#    seconds = 0.2
#    while(iterations > 0):
#        iterations -= 1
#        initialAngle = gyroscopeSensor.getAngle()
#        # Choose which side to turn
#        (distanceLeft, angleLeft) = selectSide(4, seconds) #(side, seconds)
#        (distanceRight, angleRight) = selectSide(6, 2*seconds) #(side, 2*seconds)
#        if(distanceLeft > distanceRight and distanceLeft > 30):
#            # Choose left
#            motors.move(4, 2*seconds)
#            time.sleep(1)
#            newAngle = gyroscopeSensor.getAngle()
#            D = moveFoward()
#            seconds = 0.2
#        elif(distanceRight > 30):
#            # Choose right
#            time.sleep(1)
#            newAngle = gyroscopeSensor.getAngle()
#            D = moveFoward()
#            seconds = 0.2
#        else:
#            iterations += 1
#            seconds += 0.2
#        print(D)

# Reset by pressing CTRL + C
except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()
