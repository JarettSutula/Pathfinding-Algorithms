"""
Author: Jarett Sutula
Pathfinding Algorithms Thesis Project

For now, this will serve as the main file for the project.
As the project grows, this will be split into separate files for
ease of reading and working.
"""

import pygame
pygame.init()

# Define white for screen fill later
WHITE = (255, 255, 255)

# Set the width and height of the screen. 20x20 of 32 pixel pngs
size = (640, 640)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("pathfinding-algorithms")

# Import grid units as pngs
start_node = pygame.image.load("images/start_node.png").convert()
end_node = pygame.image.load("images/end_node.png").convert()
blank_space = pygame.image.load("images/blank_space.png").convert()
obstacle = pygame.image.load("images/obstacle.png").convert()

# Keep loop running until we quit
done = False

# FPS clock
clock = pygame.time.Clock()

# Let's set the grid that we will use for finding paths. 20x20.
# 0 = blank space
# 1 = obstacle
# 2 = start node
# 3 = end node
grid = [[0 for i in range(20)] for j in range(20)]
# grid[4][5] = 1
# grid[5][10] = 2
# grid[3][19] = 3


# Let's call a function that will render the graphs.
def render_grid():
    # Loop through the entirety of the grid and render the correct png.
    for i in range(20):
        for j in range(20):
            if grid[i][j] == 0:
                screen.blit(blank_space, (32 * i, 32 * j))
            elif grid[i][j] == 1:
                screen.blit(obstacle, (32 * i, 32 * j))
            elif grid[i][j] == 2:
                screen.blit(start_node, (32 * i, 32 * j))
            elif grid[i][j] == 3:
                screen.blit(end_node, (32 * i, 32 * j))


# -------- Main Program Loop -----------
while not done:
    # --- Main event loop ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # Check for mouse pressed down.
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            # Set the corresponding grid value to new value.
            # If we are left clicking (1), set value to 1.
            if event.button == 1:
                grid[pos[0]//32][pos[1]//32] = 1

            # If we are right clicking (3), "erase" by setting value to 0.
            elif event.button == 3:
                grid[pos[0] // 32][pos[1] // 32] = 0

    # background image
    screen.fill(WHITE)

    # rendering code
    render_grid()

    # update screen and flip
    pygame.display.flip()

    # 60 fps unless we decide otherwise
    clock.tick(60)

# Quit after the main loop ends (i.e player presses the "x")
pygame.quit()
