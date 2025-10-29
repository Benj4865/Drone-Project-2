import pygame
import sys

# Initialize pygame
pygame.init()

# Creating the windown/screewherein the simulation will be rendered
screen = pygame.display.set_mode((1000,1000))
pygame.display.set_caption("Simulation_Debug")


# Position declaration
last_known_position = (0,0)
person_position = (0,0)
drone_position = (0,0)
drone_base = (0,0)


# Function to calculate drift. Isolated for easy changing or later expansion
def Drift_calc():
    pass





running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Creating a dark blue background
    screen.fill((0,0,80))

    # Updates the full Surface to the screen object
    pygame.display.flip()


