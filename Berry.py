import time
import math
import threading
from Berry_distance import Distance
from Berry_acceleration import Accelerometer
from Berry_compass import Compass
from Berry_movement import Movement


# Move foward and detect obstacles
def moveFoward():
    x = []
    y = []
    z = []
    angle = []
    dist = []
    distance = ultrasonicSensor.getDistance()

    while (distance > 30):
        #        print("Distance = %1.f cm" % distance)
        dist.append(int(distance))
        motors.move(8, 0.2)  # Move foward
        axes = accelerationSensor.getAcceleration()
        x.append(axes['y'])
        y.append(axes['x'])
        # time.sleep(0.2)
        distance = ultrasonicSensor.getDistance()
    # Velocity
    Vx = []
    Vy = []
    t = 0.2
    for i in range(0, len(x)):
        if (i == 0):
            Vx.append(x[i] * t / 2)
            Vy.append(x[i] * t / 2)
        else:
            Vx.append((x[i] + x[i - 1]) * t / 2)
            Vy.append((y[i] + y[i - 1]) * t / 2)
    # Distance
    Sx = []
    Sy = []
    for i in range(0, len(Vx)):
        if (i == 0):
            Sx.append(Vx[i] * t / 2)
            Sy.append(Vy[i] * t / 2)
        else:
            Sx.append((Vx[i] + Vx[i - 1]) * t / 2)
            Sy.append((Vy[i] + Vy[i - 1]) * t / 2)
    Dx = 0
    Dy = 0
    DeltaS = 0
    for i in range(len(Sx)):
        Dx += Sx[i] * 100
        Dy += Sy[i] * 100
        S = math.sqrt(Sx[i] * Sx[i] + Sy[i] * Sy[i])
        DeltaS += S * 100  # Convert from m to cm

    # Each instant is 0.2s (from the sleep(0.2) in move method)
    print(x)
    print(y)
    #    print(Vx)
    #    print(Vy)
    #    print(Sx)
    #    print(Sy)
    print(Dx)
    print(Dy)
    print(DeltaS)
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
    motors = Movement()
    ultrasonicSensor = Distance()
    gyroscopeSensor = Compass()
    accelerationSensor = Accelerometer()

    #    print(accelerationSensor.getAcceleration())

    D = moveFoward()

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
