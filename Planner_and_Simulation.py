import math
import pygame



import Launch_Parameters


# This function simulates "crappy" data from sensors or camera
def Data_integrity_disturber():
    pass

# Function to calculate drift. Isolated for easy changing or later expansion
def Drift_calc(person_position):
    pass

def Lawnmower_pattern():
    pass

def Drone_movement( current_pos, target, heading, ):

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




def Calc_start_pos():

    # Haversine Function Setup

    R = 6371000 #Radius of the Earth
    # Calculation from previous project, modified using ChatGPT (Next 6 lines)
    lat_rad = math.radians(Launch_Parameters.last_known_position[0])
    long_rad = math.radians(Launch_Parameters.last_known_position[1])
    bearing_rad = math.radians(Launch_Parameters.estimated_drift_bearing)
    distance_floated = Launch_Parameters.estimated_drift_velocity * Launch_Parameters.time_since_contact

    new_lat_rad = math.asin(math.sin(lat_rad) * math.cos(distance_floated / R) + math.cos(lat_rad) * math.sin(distance_floated / R) * math.cos(bearing_rad))

    new_long_rad = long_rad + math.atan2(
        math.sin(bearing_rad) * math.sin(distance_floated / R) * math.cos(lat_rad),
        math.cos(distance_floated / R) - math.sin(lat_rad) * math.sin(new_lat_rad)
    )

    new_lat = math.degrees(new_lat_rad)
    new_long = math.degrees(new_long_rad)

    estimated_starting_posistion = (new_lat,new_long)

    return estimated_starting_posistion



# Initialize pygame
pygame.init()
# Creating the windown/screewherein the simulation will be rendered
screen = pygame.display.set_mode((1000,1000))
pygame.display.set_caption("Simulation_Debug")

# Route Planner SETUP
    # 1. Calculate search location from launch parameters

starting_pos = Calc_start_pos()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Creating a dark blue background
    screen.fill((0,0,80))


    # Updates the full Surface to the screen object
    pygame.display.flip()


