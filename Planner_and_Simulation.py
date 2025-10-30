# Last Known Posistion is the last posistion the person was spotted at
# The Search Datum is the esitmated posistion of the person corrected for drift

import math
from xmlrpc.client import DateTime

import pygame
import Drone_Controller


import Launch_Parameters


# This function simulates "crappy" data from sensors or camera
def Data_integrity_disturber():
    pass

# Function to calculate drift. Isolated for easy changing or later expansion
def Drift_calc(person_position):
    pass

def Expanding_Square_pattern(datum):
    # Sets the size of the value d in Expanding Square Searches
    d = 20

    #Keeps track of the d_value currently in use
    current_d = d

    #Counts the amount of legs calculated so far
    counter = 1

    #Getting initial bearing from drift estimation
    current_bearing = Launch_Parameters.estimated_drift_bearing

    current_pos = datum

    # List for storing point in search pattern
    waypoints = []

    while counter < 40:

        #Calculating the next position to go to
        next_pos = Calc_pos(current_pos,current_bearing, current_d)
        waypoints.append(next_pos)
        current_pos = next_pos

        # calculating the new bearing for the next leg of the square
        if  current_bearing > 90:
            current_bearing -= 90
        else:
            current_bearing = 360 + (current_bearing - 90)

        if counter % 2 == 0:
            current_d += d

        counter += 1

    return waypoints



def Drone_movement( current_pos, target):

    # Math done by ChatGPT
    cur_lat_rad, cur_long_rad = math.radians(current_pos[0]), math.radians(current_pos[1])
    target_lat_rad, target_long_rad = math.radians(target[0]), math.radians(target[1])

    # Differences
    dlon = target_long_rad - cur_long_rad

    # Bearing calculation
    x = math.sin(dlon) * math.cos(target_lat_rad)
    y = math.cos(cur_lat_rad) * math.sin(target_lat_rad) - \
        math.sin(cur_lat_rad) * math.cos(target_lat_rad) * math.cos(dlon)
    bearing_rad = math.atan2(x, y)
    bearing_deg = (math.degrees(bearing_rad) + 360) % 360  # Normalize to 0–360°

    # Distance using the haversine formula
    R = 6371000  # Earth radius in meters
    dlat = target_lat_rad - cur_lat_rad
    a = math.sin(dlat/2)**2 + math.cos(cur_lat_rad) * math.cos(target_lat_rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance_m = R * c

    # Checking if distance to target is higher than speed in m.
    if distance_m >= Launch_Parameters.drone_cruise_speed:
        new_drone_pos = Calc_pos(current_pos, bearing_deg, Launch_Parameters.drone_cruise_speed)

    # if distance is less than speed, set posistion to target
    else:
        new_drone_pos = target

    return new_drone_pos



def Calc_pos(pos, bearing, distance):

    # Haversine Function Setup

    R = 6371000 #Radius of the Earth
    # Calculation from previous project, modified using ChatGPT (Next 6 lines)
    lat_rad = math.radians(pos[0])
    long_rad = math.radians(pos[1])
    bearing_rad = math.radians(bearing)

    new_lat_rad = math.asin(math.sin(lat_rad) * math.cos(distance / R) + math.cos(lat_rad) * math.sin(distance / R) * math.cos(bearing_rad))

    new_long_rad = long_rad + math.atan2(
        math.sin(bearing_rad) * math.sin(distance / R) * math.cos(lat_rad),
        math.cos(distance / R) - math.sin(lat_rad) * math.sin(new_lat_rad)
    )

    new_lat = math.degrees(new_lat_rad)
    new_long = math.degrees(new_long_rad)

    new_position = (new_lat,new_long)

    return new_position



# Initialize pygame
pygame.init()
# Creating the windown/screewherein the simulation will be rendered
screen = pygame.display.set_mode((1920,1080))
pygame.display.set_caption("Simulation_Debug")

# Route Planner SETUP
    # 1. Calculate search location from launch parameters

# Creating Drone object
drone =  Drone_Controller.Drone_Controller()
drone.position = (55.702499,12.571936)

# Target_pos is the Search Datum the first time it runs.
target_pos = Calc_pos(Launch_Parameters.last_known_position, Launch_Parameters.estimated_drift_bearing, Launch_Parameters.estimated_drift_velocity * Launch_Parameters.time_since_contact)

waypoints = Expanding_Square_pattern(target_pos)

running = True
# Keeps track of where in the search pattern the drone is
search_pattern_step = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Creating a dark blue background
    screen.fill((0,0,80))

    drone_new_pos = Drone_movement(drone.position, target_pos)
    if drone_new_pos == drone.position:
        # Updating target position
        target_pos = waypoints[search_pattern_step]

        # Increments the counter, keeping track of progress in pattern
        search_pattern_step += 1


    drone.position = drone_new_pos



    # Updates the full Surface to the screen object
    pygame.display.flip()


