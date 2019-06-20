import time
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
    while(distance > 20):
        print("Distance = %1.f cm" % distance)
        distance = ultrasonicSensor.getDistance()
        motors.move(8) # Move foward
##        axes = accelerationSensor.getAcceleration(True)
##        print("x = %.3fG" % axes['x'])
##        print("y = %.3fG" % axes['y'])
##        print("z = %.3fG" % axes['z'])
        time.sleep(0.5)

    # Choose which side to turn
    aux = 1
    while(aux > 0):
        aux -= 1
        angle = gyroscopeSensor.getAngle()
        print("Angle = %1.d degress" % angle)
        distance = ultrasonicSensor.getDistance()
        print("Distance = %1.f cm" % distance)
        motors.move(4) # Turn left
        time.sleep(2)
    while(aux < 2):
        aux += 1
        angle = gyroscopeSensor.getAngle()
        print("Angle = %1.d degress" % angle)
        distance = ultrasonicSensor.getDistance()
        print("Distance = %1.f cm" % distance)
        motors.move(6) # Turn right
        time.sleep(2)

    motors.move(4)
    angle = gyroscopeSensor.getAngle()
    print("Angle = %1.d degress" % angle)
    
# Reset by pressing CTRL + C
except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()
