import threading
from Berry_distance import Distance
from Berry_acceleration import Accelerometer
from Berry_compass import Compass
from Berry_movement import Movement

try:
    move = Movement()
    move.start()
##    distance = Distance()
##    distance.start()
##    speed = Accelerometer()
##    speed.start()
##    compass = Compass()
##    compass.start()
    
# Reset by pressing CTRL + C
except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()
