"""
Author: Jarett Sutula
Pathfinding Algorithms Thesis Project

For now, this will serve as the main file for the project.
As the project grows, this will be split into separate files for
ease of reading and working.

General controls:
Left click mouse = place obstacle block.
Right click mouse = set grid block back to blank block.
press Q = place starting node wherever mouse is hovering.
press E = place ending node wherever mouse is hovering.
press space bar = clear grid.
press P = print grid's output to console (for testing).
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

# Let's set the flags for start_node and end_nodes.
start_flag = False
end_flag = False

# Let's call a function that will render the grid.
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


# Let's call a function that will clear the grid.
def clear_grid():
    # Loop through the entirety of the grid and set back to 0.
    for i in range(20):
        for j in range(20):
            grid[i][j] = 0


def print_grid():
    # Print out the grid into console.
    for x in grid:
        for y in x:
            print(y, end=" ")
        print()


def clear_start_node():
    # Find our start node and clear it.
    for i in range(20):
        for j in range(20):
            if grid[i][j] == 2:
                grid[i][j] = 0


def clear_end_node():
    # Find our start node and clear it.
    for i in range(20):
        for j in range(20):
            if grid[i][j] == 3:
                grid[i][j] = 0

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # Check for mouse pressed down.
        if event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            # Set the corresponding grid value to new value.
            # If we are left clicking, set value to 1 (obstacle)
            if pygame.mouse.get_pressed()[0]:
                grid[pos[0] // 32][pos[1] // 32] = 1

            # If we are right clicking, "erase" by setting value to 0.
            if pygame.mouse.get_pressed()[2]:
                grid[pos[0] // 32][pos[1] // 32] = 0

        if event.type == pygame.KEYDOWN:
            # Check for pressing down start_node button
            if event.key == pygame.K_q:
                pos = pygame.mouse.get_pos()
                clear_start_node()
                grid[pos[0]//32][pos[1]//32] = 2
                start_flag = True

            # Check for pressing down end_node button
            if event.key == pygame.K_e:
                pos = pygame.mouse.get_pos()
                clear_end_node()
                grid[pos[0]//32][pos[1]//32] = 3
                end_flag = True

            if event.key == pygame.K_SPACE:
                clear_grid()

            if event.key == pygame.K_p:
                print_grid()

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
