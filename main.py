"""
Author: Jarett Sutula
Pathfinding Algorithms Thesis Project

General controls:
Left click mouse = place obstacle block.
Right click mouse = set grid block back to blank block.
press Q = place starting node wherever mouse is hovering.
press E = place ending node wherever mouse is hovering.
Click 'Clear Grid' button on screen = clear grid.
Click buttons on right side = Run different algorithms

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
BLACK = (0, 0, 0)

# FPS for drawing grid.
fps_speed = 60

# Set font and create text objects.
font = pygame.font.SysFont('Calibri', 24)
smaller_font = pygame.font.SysFont('Calibri', 18)
smallest_font = pygame.font.SysFont('Calibri', 12)
clear_text = font.render('Click to clear the grid', True, WHITE)
start_text = smaller_font.render('Press Q to create start node', True, WHITE)
end_text = smaller_font.render('Press E to create end node', True, WHITE)
obstacle_text_1 = smaller_font.render('Click and drag left mouse', True, WHITE)
obstacle_text_2 = smaller_font.render('to create obstacles', True, WHITE)
obstacle_text_3 = smaller_font.render('Click and drag right mouse', True, WHITE)
obstacle_text_4 = smaller_font.render('to erase obstacles', True, WHITE)
diagonal_priority1 = smallest_font.render('diagonal movement', True, WHITE)
diagonal_priority2 = smallest_font.render('priority for A*', True, WHITE)
show_f = smallest_font.render('show f values', True, WHITE)

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

# Import algorithm buttons as pngs.
astar = pygame.image.load("images/astar.png").convert()
bfs = pygame.image.load("images/bfs.png").convert()
da = pygame.image.load("images/da.png").convert()
dfs = pygame.image.load("images/dfs.png").convert()
on = pygame.image.load("images/on.png").convert()
off = pygame.image.load("images/off.png").convert()


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
        # track f, g, h for A* calculations.
        self.f = 0
        self.g = 0
        self.h = 0

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
# # a queue for dijkstras.
# dijkstras_queue = deque()

# 'sets' for A*. Need one of them to be closed so we can compare.
a_star_open = []
a_star_closed = []
# list to hold path from start to end.
path = []
# dijkstras_path = []

# a flag to tell us when to stop searching for the end.
bfs_done = True
dfs_done = True
dijkstras_done = True
a_star_done = True

# stats for post-algorithm work
visited_nodes = 0
path_length = 0
status = False

# a flag to track if A* is using diagonal movement heuristic.
diagonal_movement = False
show_f_values = False

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
            elif grid[i][j].value == 4:
                screen.blit(visited, (32 * j, 32 * i))
            elif grid[i][j].value == 5:
                screen.blit(unvisited, (32 * j, 32 * i))
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
            grid[i][j].f = 0
            grid[i][j].g = 0
            grid[i][j].h = 0
            global path
            path = []
            bfs_queue.clear()
            dfs_stack.clear()
            global visited_nodes
            global path_length
            global status
            visited_nodes = 0
            path_length = 0
            status = False
            global a_star_open
            global a_star_closed
            a_star_open = []
            a_star_closed = []


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
            grid[i][j].f = 0
            grid[i][j].g = 0
            grid[i][j].h = 0
            global path
            path = []
            bfs_queue.clear()
            dfs_stack.clear()
            global visited_nodes
            global path_length
            global status
            visited_nodes = 0
            path_length = 0
            status = False
            global a_star_open
            global a_star_closed
            a_star_open = []
            a_star_closed = []


def print_grid():
    # Print out the grid into console.
    for x in grid:
        for y in x:
            print(y.value, end=" ")
        print()


# Let the loop know that we shouldn't be accepting inputs at the moment.
def is_running():
    if not dfs_done or not bfs_done or not dijkstras_done or not a_star_done:
        return True
    else:
        return False


def print_neighbors(i, j):
    for target_node in grid[i][j].neighbors:
        print(target_node.x, target_node.y, target_node.value)
    print()


def print_f_values():
    for i in range(20):
        for j in range(20):
            if grid[i][j].f > 0:
                target_node = grid[i][j]
                f_val = smallest_font.render(str(target_node.f), True, BLACK)
                screen.blit(f_val, (target_node.y * 32 + 12, target_node.x * 32 + 12))


def print_cost_values():
    for i in range(20):
        for j in range(20):
            if grid[i][j].cost > 0:
                target_node = grid[i][j]
                cost_value = smallest_font.render(str(target_node.cost), True, BLACK)
                screen.blit(cost_value, (target_node.y * 32 + 12, target_node.x * 32 + 12))


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


def calculate_heuristic(node_a, node_b):
    # Since we only have 4 directions, use Manhattan Distance between node a and node b.
    # Manhattan Distance is the absolute value of (node_a.x - node_b.x) - absolute value of (node_a.y - node_b.y).
    if not diagonal_movement:
        x = abs(node_a.x - node_b.x)
        y = abs(node_a.y - node_b.y)

    # Manhattan Distance with an emphasis on diagonal movement.
    # on much larger grids, this can increase computation time.
    else:
        x = abs(node_a.x - node_b.x) ** 2
        y = abs(node_a.y - node_b.y) ** 2

    return x + y


def bfs_start():
    reset_grid()
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
        # add the start node to the queue!
        bfs_queue.append(grid[start_pos[0]][start_pos[1]])


def dfs_start():
    reset_grid()
    if start_node_placed and end_node_placed:
        for x in grid:
            for y in x:
                y.add_dfs_neighbors()
        print("added neighbors for DFS")
        global dfs_done
        dfs_done = False
        grid[start_pos[0]][start_pos[1]].start_node = True
        dfs_stack.append(grid[start_pos[0]][start_pos[1]])


def dijkstras_start():
    reset_grid()
    if start_node_placed and end_node_placed:
        for x in grid:
            for y in x:
                # we can use bfs add_neighbors since they work the same way in same-cost grids.
                y.add_neighbors()
        print("added neighbors for Dijkstra's Algorithm")
        global dijkstras_done
        dijkstras_done = False
        grid[start_pos[0]][start_pos[1]].start_node = True
        bfs_queue.append(grid[start_pos[0]][start_pos[1]])


def a_star_start():
    reset_grid()
    if start_node_placed and end_node_placed:
        for x in grid:
            for y in x:
                y.add_neighbors()
        print("added neighbors for A* Algorithm")
        global a_star_done
        a_star_done = False
        grid[start_pos[0]][start_pos[1]].start_node = True
        a_star_open.append(grid[start_pos[0]][start_pos[1]])


# -------- Main Program Loop -----------
while not done:
    # --- Main event loop ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # Check if we clicked on the right side for various buttons.
        # "clear grid" text.
        if event.type == pygame.MOUSEBUTTONUP and not is_running():
            pos = pygame.mouse.get_pos()
            if 650 < pos[0] < 860 and 90 < pos[1] < 130:
                clear_grid()
                start_node_placed = False
                end_node_placed = False

            # Check if we clicked BFS.
            elif 650 < pos[0] < 690 and 150 < pos[1] < 190:
                bfs_start()

            # Check if we clicked DFS.
            elif 710 < pos[0] < 750 and 150 < pos[1] < 190:
                dfs_start()

            # Check if we clicked Dijkstra's.
            elif 770 < pos[0] < 810 and 150 < pos[1] < 190:
                dijkstras_start()

            # Check if we clicked A*.
            elif 830 < pos[0] < 870 and 150 < pos[1] < 190:
                a_star_start()

            # Check if we clicked Diagonal Movement Heuristic button.
            elif 830 < pos[0] < 870 and 210 < pos[1] < 250:
                if diagonal_movement:
                    diagonal_movement = False
                else:
                    diagonal_movement = True

            # Check if we clicked show f values button.
            elif 830 < pos[0] < 870 and 270 < pos[1] < 310:
                if show_f_values:
                    show_f_values = False
                else:
                    show_f_values = True

        # Check for mouse pressed down.
        if event.type == pygame.MOUSEMOTION and not is_running():
            pos = pygame.mouse.get_pos()
            if pos[0] < 640:
                # Set the corresponding grid value to new value.
                # If we are left clicking, set value to 1 (obstacle)
                if pygame.mouse.get_pressed()[0]:
                    grid[pos[1] // 32][pos[0] // 32].value = 1

                # If we are right clicking, "erase" by setting value to 0.
                if pygame.mouse.get_pressed()[2]:
                    grid[pos[1] // 32][pos[0] // 32].value = 0

        if event.type == pygame.KEYDOWN and not is_running():
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

            # Print out grid into console for debugging.
            if event.key == pygame.K_p:
                print_grid()

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
        if len(bfs_queue) > 0:
            # set our current node (starts at start_node pos, ends at end_node pos)
            current_node = bfs_queue.popleft()
            # change color if we are a neighboring node and add cost.
            if current_node.value == 5:
                current_node.value = 4
            # check if we are at the end.
            if current_node.x == end_pos[0] and current_node.y == end_pos[1]:
                print("found end node")
                dijkstras_done = True
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
                    if not neighbor.visited and neighbor.value != 1 and neighbor.value != 2:
                        neighbor.visited = True
                        neighbor.cost = current_node.cost + 1
                        # keep start node and end node same colors.
                        if neighbor.value != 2 and neighbor.value != 3:
                            neighbor.value = 5
                        neighbor.previous_node = current_node
                        bfs_queue.append(neighbor)

        # if the queue is empty and we don't have the end node yet, no solution.
        else:
            print("no solution")
            dijkstras_done = True
            update_stats()
            status = False

    # run A*
    if not a_star_done:
        fps_speed = 20
        # store end node, as we need to use it to estimate the distance.
        a_star_end = grid[end_pos[0]][end_pos[1]]
        # do we have any more nodes left in list?
        if len(a_star_open) > 0:
            # set our current node. Needs to be the lowest F cost on open list.
            # for starting node, all f values will be zero so it will remain the starting node.
            winning_index = 0
            for i in range(len(a_star_open)):
                if a_star_open[i].f < a_star_open[winning_index].f:
                    winning_index = i

            # now, winning_index should be the index of lowest F cost node.
            current_node = a_star_open[winning_index]
            # change color if we are a neighboring node.
            if current_node.value == 5:
                current_node.value = 4

            # check if we are at the end.
            if current_node.x == end_pos[0] and current_node.y == end_pos[1]:
                print("found end node")
                a_star_done = True
                temp = current_node
                # retrace our steps!
                while not temp.previous_node.start_node:
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
                # we need to move the node from the open list to the closed one.
                a_star_open.remove(current_node)
                a_star_closed.append(current_node)

                # get the neighbors of the current node and give them g, f, h values.
                # .. but only if they are not in the closed list already or they are an obstacle.
                for neighbor in current_node.neighbors:
                    if neighbor.value == 1 or neighbor in a_star_closed:
                        # if they are, just ignore everything else and go to next neighbor.
                        continue
                    placeholder = current_node.g + 1

                    # now we need to see if the neighbor is in the open list.
                    # if it is, just update the g value if we need to.
                    if neighbor in a_star_open:
                        if placeholder < neighbor.g:
                            neighbor.g = placeholder

                    # if it's not in either open or closed set, put it in the open set.
                    else:
                        if not neighbor.visited and neighbor.value != 1:
                            neighbor.visited = True
                            # keep start node and end node same colors.
                            if neighbor.value != 2 and neighbor.value != 3:
                                neighbor.value = 5
                        neighbor.g = placeholder
                        a_star_open.append(neighbor)

                    # track previous node.
                    neighbor.previous_node = current_node
                    # update h and f according to heuristic and g.
                    neighbor.h = calculate_heuristic(neighbor, a_star_end)
                    neighbor.f = neighbor.g + neighbor.h

        # if the open list is empty and we don't have the end node yet, no solution.
        else:
            print("no solution")
            a_star_done = True
            update_stats()
            status = False

    # background image
    screen.fill(GRAY)

    # rendering code
    render_grid()
    if show_f_values:
        print_f_values()

    print_cost_values()

    # render text on screen.
    screen.blit(clear_text, (660, 100))
    screen.blit(start_text, (660, 550))
    screen.blit(end_text, (665, 590))
    screen.blit(obstacle_text_1, (670, 430))
    screen.blit(obstacle_text_2, (695, 450))
    screen.blit(obstacle_text_3, (665, 490))
    screen.blit(obstacle_text_4, (695, 510))

    # render algorithm buttons.
    screen.blit(bfs, (650, 150))
    screen.blit(dfs, (710, 150))
    screen.blit(da, (770, 150))
    screen.blit(astar, (830, 150))

    # Conditionals for A* and Dijkstra's that can be triggered.
    if diagonal_movement:
        screen.blit(on, (830, 210))
    else:
        screen.blit(off, (830, 210))
    if show_f_values:
        screen.blit(on, (830, 270))
    else:
        screen.blit(off, (830, 270))

    # Display A* conditional labels
    screen.blit(diagonal_priority1, (725, 220))
    screen.blit(diagonal_priority2, (740, 230))
    screen.blit(show_f, (750, 285))

    # if we want to update our stats, blit the text.
    if visited_nodes > 0:
        stats_1_text = smaller_font.render('Visited Nodes: ' + str(visited_nodes), True, WHITE)
        stats_2_text = smaller_font.render('Path Nodes: ' + str(path_length), True, WHITE)
        stats_3_text = smaller_font.render('Status: ' + ('Succeeded' if status else 'Failed'), True, WHITE if status else RED)
        screen.blit(stats_1_text, (660, 320))
        screen.blit(stats_2_text, (660, 340))
        screen.blit(stats_3_text, (660, 360))

    # update screen and flip
    pygame.display.flip()

    # 60 fps unless we decide otherwise
    clock.tick(fps_speed)

# Quit after the main loop ends (i.e player presses the "x")
pygame.quit()
