import pygame
import sys

# Initialize pygame
pygame.init()

# Creating the windown/screewherein the simulation will be rendered
screen = pygame.display.set_mode((800,800))
pygame.display.set_caption("Simulation_Debug")



running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Creating a dark blue background
    screen.fill((0,0,80))

    # Updates the full Surface to the screen object
    pygame.display.flip()


