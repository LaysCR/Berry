import time
import math
import threading
from Berry_distance import Distance
from Berry_acceleration import Accelerometer
from Berry_compass import Compass
from Berry_movement import Movement

try:
    # Instantiate objects
    motors = Movement()
    ultrasonicSensor = Distance()
    gyroscopeSensor = Compass()
    accelerationSensor = Accelerometer()
    distance = ultrasonicSensor.getDistance()

    # Move foward and detect obstacles
    x = []
    y = []
    angle = []
    dist = []
    
    while(distance > 20):
        
##        print("Distance = %1.f cm" % distance)
        distance = ultrasonicSensor.getDistance()
        dist.append(int(distance))
        motors.move(8) # Move foward
        axes = accelerationSensor.getAcceleration(True)
        x.append(axes['x'])
        y.append(axes['y'])
        angle.append(gyroscopeSensor.getAngle())
        time.sleep(0.1)
    for i in range(len(x)):
        x[i] = abs(x[i])
    print(x)
    print(y)
    # Velocity
    Vx = []
    Vy = []
    t = 0.2
    for i in range(2, len(x)):
        Vx.append((x[i] + x[i-1])*t/2)
        Vy.append((y[i] + y[i-1])*t/2)
    # Distance
    Sx = []
    Sy = []
    for i in range(len(Vx)-1):
        Sx.append((Vx[i] + Vx[i+1])*t/2)
        Sy.append((Vy[i] + Vy[i+1])*t/2)
    DeltaS = 0
    for i in range(len(Sx)):
        S = math.sqrt(Sx[i]*Sx[i] + Sy[i]*Sy[i])
        DeltaS += S*100
    print(DeltaS)
    # Each instant is 0.2s (from the sleep(0.2) in move method)
##    print(Vx)
##    print(Vy)
##    print(Sx)
##    print(Sy)
    # Choose which side to turn
##    aux = 1
##    while(aux > 0):
##        aux -= 1
##        angle = gyroscopeSensor.getAngle()
##        print("Angle = %1.d degress" % angle)
##        distance = ultrasonicSensor.getDistance()
##        print("Distance = %1.f cm" % distance)
##        motors.move(4) # Turn left
##        time.sleep(2)
##    while(aux < 2):
##        aux += 1
##        angle = gyroscopeSensor.getAngle()
##        print("Angle = %1.d degress" % angle)
##        distance = ultrasonicSensor.getDistance()
##        print("Distance = %1.f cm" % distance)
##        motors.move(6) # Turn right
##        time.sleep(2)
##
##    motors.move(4)
##    angle = gyroscopeSensor.getAngle()
##    print("Angle = %1.d degress" % angle)
##    
# Reset by pressing CTRL + C
except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()
