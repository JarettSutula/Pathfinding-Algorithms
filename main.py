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
Click button on screen = clear grid.
press P = print grid's output to console (for testing).
press I = start BFS.
"""
from collections import deque

import pygame
pygame.init()
pygame.font.init()

# Define colors for screen fill, font
WHITE = (255, 255, 255)
GRAY = (105, 105, 105)
GREEN = (0, 128, 0)
RED = (255, 0, 0)

# FPS for drawing grid.
fps_speed = 60

# Set font and create text objects.
font = pygame.font.SysFont('Calibri', 24)
smaller_font = pygame.font.SysFont('Calibri', 18)
clear_text = font.render('Click to clear the grid', True, WHITE)
start_text = smaller_font.render('Press Q to create start node', True, WHITE)
end_text = smaller_font.render('Press E to create end node', True, WHITE)
obstacle_text_1 = smaller_font.render('Click and drag left mouse', True, WHITE)
obstacle_text_2 = smaller_font.render('to create obstacles', True, WHITE)
obstacle_text_3 = smaller_font.render('Click and drag right mouse', True, WHITE)
obstacle_text_4 = smaller_font.render('to erase obstacles', True, WHITE)

# Set the width and height of the screen. 20x20 of 32 pixel pngs
size = (880, 640)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("pathfinding-algorithms")

# Import grid units as pngs
start_node = pygame.image.load("images/start_node.png").convert()
end_node = pygame.image.load("images/end_node.png").convert()
blank_space = pygame.image.load("images/blank_space.png").convert()
obstacle = pygame.image.load("images/obstacle.png").convert()
unvisited = pygame.image.load("images/unvisited.png").convert()
visited = pygame.image.load("images/visited.png").convert()
path_block = pygame.image.load("images/path.png").convert()
visited_dijkstras = pygame.image.load("images/visited_dijkstras.png").convert()
path_block_dijkstras = pygame.image.load("images/path_dijkstras.png").convert()

# Keep loop running until we quit
done = False

# FPS clock
clock = pygame.time.Clock()


# every node in the grid should start at value = 0 for blank space.
# Track value, its neighbors, and its coordinates on the grid.
class Node:
    def __init__(self, x, y):
        self.value = 0
        self.neighbors = []
        self.x = x
        self.y = y
        self.previous_node = None
        self.visited = False
        self.start_node = False
        self.cost = 0

    # Look in 4 directions around node and add neighbors to self.neighbors
    def add_neighbors(self):
        # make sure we are not going out of bounds!
        # remember... x value = which row it is in. y value = which column it is in.
        # add down neighbor. x + 1.
        if self.x < 19:
            self.neighbors.append(grid[self.x + 1][self.y])
        # add right neighbor
        if self.y < 19:
            self.neighbors.append(grid[self.x][self.y + 1])
        # add up neighbor
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        # add left neighbor
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])

    def add_dfs_neighbors(self):
        # Add them in the order of desired stack - north -> east -> south -> west
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
        # add South neighbor. x + 1.
        if self.x < 19:
            self.neighbors.append(grid[self.x + 1][self.y])
        # add right neighbor
        if self.y < 19:
            self.neighbors.append(grid[self.x][self.y + 1])
        # add North neighbor
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])


# Let's set the grid that we will use for finding paths. 20x20.
# 0 = blank space
# 1 = obstacle
# 2 = start node
# 3 = end node
# 4 = visited
# 5 = unvisited
# 6 = path

# Create the grid, then replace it with new Nodes().
grid = [[0 for a in range(20)] for b in range(20)]

for i in range(20):
    for j in range(20):
        grid[i][j] = Node(i, j)

# Let's set the flags for start_node and end_nodes.
start_node_placed = False
start_pos = [0, 0]
end_node_placed = False
end_pos = [0, 0]

# a deque allows us to quickly append and pop instantly. here will go the nodes to be added and searched.
bfs_queue = deque()
# a "stack" will let us use DFS.
dfs_stack = deque()
# a queue for dijkstras.
dijkstras_queue = deque()

# list to hold path from start to end.
path = []
dijkstras_path = []
# a flag to tell us when to stop searching for the end.
bfs_done = True
dfs_done = True
dijkstras_done = True
# stats for post-algorithm work
visited_nodes = 0
path_length = 0
status = False


# Let's call a function that will render the grid. Pass in start/end node flags.
def render_grid():
    # Loop through the entirety of the grid and render the correct png.
    for i in range(20):
        for j in range(20):
            if grid[i][j].value == 0:
                screen.blit(blank_space, (32 * j, 32 * i))
            elif grid[i][j].value == 1:
                screen.blit(obstacle, (32 * j, 32 * i))
            elif grid[i][j].value == 2:
                screen.blit(start_node, (32 * j, 32 * i))
            elif grid[i][j].value == 3:
                screen.blit(end_node, (32 * j, 32 * i))
            elif grid[i][j].value == 4 and grid[i][j].cost > 0:
                screen.blit(visited_dijkstras, (32 * j, 32 * i))
            elif grid[i][j].value == 4:
                screen.blit(visited, (32 * j, 32 * i))
            elif grid[i][j].value == 5:
                screen.blit(unvisited, (32 * j, 32 * i))
            elif grid[i][j].value == 6 and grid[i][j].cost > 0:
                screen.blit(path_block_dijkstras, (32 * j, 32 * i))
            elif grid[i][j].value == 6:
                screen.blit(path_block, (32 * j, 32 * i))

    # Update the start_node and end_node flags to make sure this is runnable.
    start_flag = False
    end_flag = False
    global start_pos
    global end_pos
    for i in range(20):
        for j in range(20):
            if grid[i][j].value == 2:
                start_flag = True
                start_pos = [i, j]
            if grid[i][j].value == 3:
                end_flag = True
                end_pos = [i, j]
    if not start_flag:
        global start_node_placed
        start_node_placed = False
    if not end_flag:
        global end_node_placed
        end_node_placed = False


# Let's call a function that will clear the grid.
def clear_grid():
    # Loop through the entirety of the grid and set back to 0.
    for i in range(20):
        for j in range(20):
            grid[i][j].value = 0
            grid[i][j].neighbors = []
            grid[i][j].previous_node = None
            grid[i][j].start_node = False
            grid[i][j].visited = False
            grid[i][j].cost = 0
            global path
            path = []
            global dijkstras_path
            dijkstras_path = []
            bfs_queue.clear()
            dfs_stack.clear()
            dijkstras_queue.clear()
            global visited_nodes
            global path_length
            global status
            visited_nodes = 0
            path_length = 0
            status = False


# Let's reset the grid between searches but without clearing the obstacles and start/end nodes
def reset_grid():
    # Loop through the grid and only reset values that are NOT obstacles or nodes.
    for i in range(20):
        for j in range(20):
            if grid[i][j].value > 3:
                grid[i][j].value = 0
            grid[i][j].neighbors = []
            grid[i][j].previous_node = None
            grid[i][j].start_node = False
            grid[i][j].visited = False
            grid[i][j].cost = 0
            global path
            path = []
            global dijkstras_path
            dijkstras_path = []
            bfs_queue.clear()
            dfs_stack.clear()
            dijkstras_queue.clear()
            global visited_nodes
            global path_length
            global status
            visited_nodes = 0
            path_length = 0
            status = False


def print_grid():
    # Print out the grid into console.
    for x in grid:
        for y in x:
            print(y.value, end=" ")
        print()


def print_flags():
    print(start_node_placed)
    print(end_node_placed)


def print_neighbors(i, j):
    for target_node in grid[i][j].neighbors:
        print(target_node.x, target_node.y, target_node.value)
    print()


def clear_start_node():
    # Find our start node and clear it.
    for i in range(20):
        for j in range(20):
            if grid[i][j].value == 2:
                grid[i][j].value = 0


def clear_end_node():
    # Find our start node and clear it.
    for i in range(20):
        for j in range(20):
            if grid[i][j].value == 3:
                grid[i][j].value = 0


def update_stats():
    # at the end of every algorithm run, output the stats.
    for i in range(20):
        for j in range(20):
            # if we have visited a node, count it.
            if grid[i][j].value == 4:
                global visited_nodes
                visited_nodes += 1
            # if our node is a path, count it as visited and as a path node.
            if grid[i][j].value == 6:
                global path_length
                path_length += 1
                visited_nodes += 1


def bfs_start():
    if start_node_placed and end_node_placed:
        for x in grid:
            for y in x:
                y.add_neighbors()
        print("added neighbors for BFS")
        # after adding the correct neighbors, let's try BFS.
        global bfs_done
        bfs_done = False
        # set the starting point with no previous node.
        grid[start_pos[0]][start_pos[1]].start_node = True
        print(grid[start_pos[0]][start_pos[1]].start_node)
        # add the start node to the queue!
        bfs_queue.append(grid[start_pos[0]][start_pos[1]])


def dfs_start():
    if start_node_placed and end_node_placed:
        for x in grid:
            for y in x:
                y.add_dfs_neighbors()
        print("added neighbors for DFS")
        global dfs_done
        dfs_done = False
        # set the starting point with no previous node.
        grid[start_pos[0]][start_pos[1]].start_node = True
        print(grid[start_pos[0]][start_pos[1]].start_node)
        # add the start node to the queue!
        dfs_stack.append(grid[start_pos[0]][start_pos[1]])


def dijkstras_start():
    if start_node_placed and end_node_placed:
        for x in grid:
            for y in x:
                # we can use bfs add_neighbors since they work the same way in same-cost grids.
                y.add_neighbors()
        print("added neighbors for Dijkstra's Algorithm")
        # after adding the correct neighbors, let's try BFS.
        global dijkstras_done
        dijkstras_done = False
        # set the starting point with no previous node.
        grid[start_pos[0]][start_pos[1]].start_node = True
        print(grid[start_pos[0]][start_pos[1]].start_node)
        # add the start node to the queue!
        dijkstras_queue.append(grid[start_pos[0]][start_pos[1]])


# -------- Main Program Loop -----------
while not done:
    # --- Main event loop ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # Check if we clicked the "clear grid" button.
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if 650 < pos[0] < 860 and 90 < pos[1] < 130:
                clear_grid()
                start_node_placed = False
                end_node_placed = False

        # Check for mouse pressed down.
        if event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            if pos[0] < 640:
                # Set the corresponding grid value to new value.
                # If we are left clicking, set value to 1 (obstacle)
                if pygame.mouse.get_pressed()[0]:
                    grid[pos[1] // 32][pos[0] // 32].value = 1

                # If we are right clicking, "erase" by setting value to 0.
                if pygame.mouse.get_pressed()[2]:
                    grid[pos[1] // 32][pos[0] // 32].value = 0

        if event.type == pygame.KEYDOWN:
            # Check for pressing down start_node button
            if event.key == pygame.K_q:
                pos = pygame.mouse.get_pos()
                if pos[0] < 640:
                    clear_start_node()
                    grid[pos[1]//32][pos[0]//32].value = 2
                    start_node_placed = True

            # Check for pressing down end_node button
            if event.key == pygame.K_e:
                pos = pygame.mouse.get_pos()
                if pos[0] < 640:
                    clear_end_node()
                    grid[pos[1]//32][pos[0]//32].value = 3
                    end_node_placed = True

            if event.key == pygame.K_p:
                print_grid()

            if event.key == pygame.K_o:
                print_flags()

            if event.key == pygame.K_i:
                reset_grid()
                bfs_start()

            if event.key == pygame.K_u:
                reset_grid()
                dfs_start()

            if event.key == pygame.K_y:
                reset_grid()
                dijkstras_start()

            if event.key == pygame.K_SPACE:
                reset_grid()

    # run bfs
    if not bfs_done:
        fps_speed = 20
        # do we have any more nodes left in queue?
        if len(bfs_queue) > 0:
            # set our current node (starts at start_node pos, ends at end_node pos)
            current_node = bfs_queue.popleft()
            # change color if we are a neighboring node.
            if current_node.value == 5:
                current_node.value = 4
            # check if we are at the end.
            if current_node.x == end_pos[0] and current_node.y == end_pos[1]:
                print("found end node")
                bfs_done = True
                temp = current_node
                # retrace our steps!
                while not temp.previous_node.start_node:
                    # print(temp.previous_node.y)
                    path.append(temp.previous_node)
                    temp = temp.previous_node
                # change our path visuals.
                for node in path:
                    node.value = 6
                update_stats()
                status = True
                fps_speed = 60

            # if we are not at the end node...
            else:
                # get the neighbors of the current node and add them to queue.
                for neighbor in current_node.neighbors:
                    # If they are not visited and not an obstacle, keep going.
                    if not neighbor.visited and neighbor.value != 1:
                        neighbor.visited = True
                        # keep start node and end node same colors.
                        if neighbor.value != 2 and neighbor.value != 3:
                            neighbor.value = 5
                        neighbor.previous_node = current_node
                        bfs_queue.append(neighbor)

        # if the queue is empty and we don't have the end node yet, no solution.
        else:
            print("no solution")
            bfs_done = True
            update_stats()
            status = False

    # run dfs
    if not dfs_done:
        fps_speed = 20
        # do we have any more nodes left in stack?
        if len(dfs_stack) > 0:
            # set our current node (starts at start_node pos, ends at end_node pos)
            current_node = dfs_stack.pop()
            # change color if we are a neighboring node.
            if current_node.value == 5:
                current_node.value = 4
            # check if we are at the end.
            if current_node.x == end_pos[0] and current_node.y == end_pos[1]:
                print("found end node")
                dfs_done = True
                temp = current_node
                # retrace our steps!
                while not temp.previous_node.start_node:
                    # print(temp.previous_node.y)
                    path.append(temp.previous_node)
                    temp = temp.previous_node
                # change our path visuals.
                for node in path:
                    node.value = 6
                update_stats()
                status = True
                fps_speed = 60

            # if we are not at the end node...
            else:
                # get the neighbors of the current node and add them to queue.
                for neighbor in current_node.neighbors:
                    # If they are not visited and not an obstacle, keep going.
                    if not neighbor.visited and neighbor.value != 1:
                        neighbor.visited = True
                        # keep start node and end node same colors.
                        if neighbor.value != 2 and neighbor.value != 3:
                            neighbor.value = 5
                        neighbor.previous_node = current_node
                        dfs_stack.append(neighbor)

        # if the queue is empty and we don't have the end node yet, no solution.
        else:
            print("no solution")
            dfs_done = True
            update_stats()
            status = False

    # run dijkstra's
    if not dijkstras_done:
        fps_speed = 20
        # do we have any more nodes left in queue?
        if len(dijkstras_queue) > 0:
            # set our current node (starts at start_node pos, ends at end_node pos)
            current_node = dijkstras_queue.popleft()
            # change color if we are a neighboring node and add cost.
            if current_node.value == 5:
                current_node.value = 4
                current_node.cost = 1
            # check if we are at the end.
            if current_node.x == end_pos[0] and current_node.y == end_pos[1]:
                print("found end node")
                dijkstras_done = True
                temp = current_node
                # retrace our steps!
                while not temp.previous_node.start_node:
                    # print(temp.previous_node.y)
                    dijkstras_path.append(temp.previous_node)
                    temp = temp.previous_node
                # change our path visuals.
                for node in dijkstras_path:
                    node.value = 6
                update_stats()
                status = True
                fps_speed = 60

            # if we are not at the end node...
            else:
                # get the neighbors of the current node and add them to queue.
                for neighbor in current_node.neighbors:
                    # If they are not visited and not an obstacle, keep going.
                    if not neighbor.visited and neighbor.value != 1:
                        neighbor.visited = True
                        # keep start node and end node same colors.
                        if neighbor.value != 2 and neighbor.value != 3:
                            neighbor.value = 5
                        neighbor.previous_node = current_node
                        dijkstras_queue.append(neighbor)

        # if the queue is empty and we don't have the end node yet, no solution.
        else:
            print("no solution")
            dijkstras_done = True
            update_stats()
            status = False

    # background image
    screen.fill(GRAY)

    # rendering code
    render_grid()
    screen.blit(clear_text, (660, 100))
    screen.blit(start_text, (660, 550))
    screen.blit(end_text, (665, 590))
    screen.blit(obstacle_text_1, (670, 430))
    screen.blit(obstacle_text_2, (695, 450))
    screen.blit(obstacle_text_3, (665, 490))
    screen.blit(obstacle_text_4, (695, 510))

    # if we want to update our stats, blit the text.
    if visited_nodes > 0:
        stats_1_text = smaller_font.render('Visited Nodes: ' + str(visited_nodes), True, WHITE)
        stats_2_text = smaller_font.render('Path Nodes: ' + str(path_length), True, WHITE)
        stats_3_text = smaller_font.render('Status: ' + ('Succeeded' if status else 'Failed'), True, WHITE if status else RED)
        screen.blit(stats_1_text, (660, 250))
        screen.blit(stats_2_text, (660, 270))
        screen.blit(stats_3_text, (660, 290))

    # update screen and flip
    pygame.display.flip()

    # 60 fps unless we decide otherwise
    clock.tick(fps_speed)

# Quit after the main loop ends (i.e player presses the "x")
pygame.quit()
