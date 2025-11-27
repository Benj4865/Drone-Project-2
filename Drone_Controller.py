# This program is to simulate the drone controller, so it can be isolated from the simulation
# and it can be used for later implementation in a real drone.

class Drone_Controller:

    velocity = 0
    bearing = 0
    altitude = 0
    position = (0,0)
    flight_time = 0
    battery_left = 100
    distance_flown = 0

    #Static Variable
    drone_base = (0,0)