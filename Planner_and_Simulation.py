# Last Known Posistion is the last posistion the person was spotted at
# The Search Datum is the esitmated posistion of the person corrected for drift

import math

import Drone_Controller
import Launch_Parameters
import list_converter
import search_leg
import intersect_Calculator


# This function simulates "crappy" data from sensors or camera
def Data_integrity_disturber():
    pass

# Function to calculate drift. Isolated for easy changing or later expansion
def Drift_calc(person_position):
    #Person Posistion is in GPS coordinates

    #Return new position
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
    search_legs = []

    while counter < 40:

        #Calculating the next position to go to
        next_pos = Calc_pos(current_pos,current_bearing, current_d)

        new_leg = search_leg.Search_leg()
        new_leg.start_pos = current_pos
        new_leg.end_pos = next_pos
        new_leg.is_active = True

        search_legs.append(new_leg)
        current_pos = next_pos

        # calculating the new bearing for the next leg of the square
        if  current_bearing > 90:
            current_bearing -= 90
        else:
            current_bearing = 360 + (current_bearing - 90)

        if counter % 2 == 0:
            current_d += d

        counter += 1

    return search_legs

def Calc_dist_to_point(current_pos, target_pos):

    # Math done by ChatGPT
    cur_lat_rad, cur_long_rad = math.radians(current_pos[0]), math.radians(current_pos[1])
    target_lat_rad, target_long_rad = math.radians(target_pos[0]), math.radians(target_pos[1])

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

    return distance_m


def Drone_movement(current_pos, target_pos):

    # Math done by ChatGPT
    cur_lat_rad, cur_long_rad = math.radians(current_pos[0]), math.radians(current_pos[1])
    target_lat_rad, target_long_rad = math.radians(target_pos[0]), math.radians(target_pos[1])

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
        new_drone_pos = target_pos

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

# Route Planner SETUP
    # 1. Calculate search location from launch parameters

# Creating Drone object
drone =  Drone_Controller.Drone_Controller()
drone.drone_base = (55.607124, 12.393114)
drone.position = drone.drone_base

# Target_pos is the Search Datum the first time it runs.
target_pos = Calc_pos(Launch_Parameters.last_known_position, Launch_Parameters.estimated_drift_bearing, Launch_Parameters.estimated_drift_velocity * Launch_Parameters.time_since_contact)

#leg = search_leg.Search_leg()
#leg.start_pos = target_pos
#leg.end_pos = drone.drone_base
#beach = Launch_Parameters.beach_plygon
#leg = intersect_Calculator.calc_intersec(beach, leg)


# Creating a variable to save the last "completed" waypoint for later calculation
prev_waypoint = drone.position

search_legs = Expanding_Square_pattern(target_pos)

modified_search_legs = []

for leg in search_legs:
    modified_search_leg = intersect_Calculator.calc_intersec(Launch_Parameters.beach_plygon, leg)
    modified_search_legs.append(modified_search_leg)

unprocessed_indexes = []
for i in range(len(modified_search_legs)):
    if modified_search_legs[i].is_active == True:
        unprocessed_indexes.append(i)

flight_path = []
current_leg_index = 0

# Can be 1 or -1, an is used to determine the derection of flight in the pattern
path_direction = 1

while True:

    if len(unprocessed_indexes) == 0:
        break

    current_leg = modified_search_legs[current_leg_index]

    if current_leg.is_active and current_leg.intersect_point == None:
        if path_direction == 1:
            flight_path.append(current_leg.end_pos)
        else:
            flight_path.append(current_leg.start_pos)

        unprocessed_indexes.remove(current_leg_index)
        current_leg_index += path_direction

    elif current_leg.is_active and current_leg.intersect_point is not None:

        flight_path.append(current_leg.intersect_point)
        unprocessed_indexes.remove(current_leg_index)

        if len(unprocessed_indexes) == 0:
            break

        next_leg_index = current_leg_index + path_direction
        next_leg = modified_search_legs[next_leg_index]

        if next_leg.is_active == False:

            if (next_leg_index) in unprocessed_indexes:
                unprocessed_indexes.remove(next_leg_index)

            current_leg_index += 4

            if current_leg_index >= len(modified_search_legs):
                current_leg_index = len(modified_search_legs) - 1

                flight_path.append(modified_search_legs[current_leg_index].end_pos)

            path_direction *= -1

        else:
            if  next_leg.intersect_point is None:
                if path_direction == 1:
                    flight_path.append(current_leg.end_pos)
                else:
                    flight_path.append(current_leg.start_pos)

            current_leg_index += path_direction

flight_path.insert(0, drone.drone_base)
flight_path.insert(1, target_pos)
flight_path.append(drone.drone_base)


list_converter.save_kml(flight_path, "C:\\users\\bena3\\downloads\\FlightPath_.kml", "FP")





running = True
# Keeps track of where in the search pattern the drone is
search_pattern_step = 0


while running:


    drone_new_pos = Drone_movement(drone.position, target_pos)

    if drone_new_pos == drone.position:
        #Calculating time/distance flown in last leg of pattern
        last_leg_dist = Calc_dist_to_point(drone.position, prev_waypoint)
        last_leg_time = (last_leg_dist / Launch_Parameters.drone_cruise_speed) + 2 # +2 to add an acceleration "slowdown" and "speedup" for changing directions

        # updating drone time and dist flown
        drone.distance_flown += last_leg_dist
        drone.flight_time += last_leg_time

        #Updating previous waypoint to current position
        prev_waypoint = drone.position
        # Updating target position
        leg = search_legs[search_pattern_step]
        target_pos = leg.end_pos

        # Increments the counter, keeping track of progress in pattern
        search_pattern_step += 1
        if search_pattern_step >= len(search_legs):

            break

    drone.position = drone_new_pos


print(drone.flight_time)
print(drone.distance_flown)

list_converter.save_kml(search_legs, "C:\\users\\bena3\\downloads\\ESPattern_2.kml", "ESPattern")

#for point in waypoints:
#    print("(" + str(point[0]) + ", " + str(point[1]) + "),")

