import math
import FreeCAD as App
import Part
import numpy as np

# Add path to access constants file
import os, sys
sys.path.append(os.path.dirname(__file__))

import constants

'''
my_create_line():
Parameters:
- pt1, pt2, points on the line in the form (x, y, z)
- obj_name, name of Line Object
Return: 
- Updated active document

Source:
- Updated active documenthttps://wiki.freecad.org/Part_scripting
'''
def my_create_line(pt1, pt2, obj_name):
    obj = App.ActiveDocument.addObject("Part::Line", obj_name)
    # Create object with two coordinate pairs
    # Set each coordinate pair to pt1 and pt2
    obj.X1 = pt1[0]
    obj.Y1 = pt1[1]
    obj.Z1 = pt1[2]

    obj.X2 = pt2[0]
    obj.Y2 = pt2[1]
    obj.Z2 = pt2[2]

    # Recompute the active document to draw the line
    App.ActiveDocument.recompute()
    return obj

# Get constants
driverHead = constants.DRIVER_HEAD

absPathRoot = constants.ABS_PATH_ROOT
TRUCK_NAME = constants.TRUCK_NAME

FULL_LIST = np.load(f'{absPathRoot}/{TRUCK_NAME}_part_names.npy')

doc = App.ActiveDocument

CANDIDATES_SET = set()
NONCANDIDATES_SET = set()

'''
initialize_twodlist():
Parameters:
- thetas, phis: number of theta and phi angles to track
Return:
- empty grid to track rays across each theta and phi -> we use this to track results

Source:
- Updated active documenthttps://wiki.freecad.org/Part_scripting
'''
def initialize_twodlist(thetas, phis):
    bfs_map = []
    new = []
    for i in range (0, thetas):
        for j in range (0, phis):
            new.append(0)
        bfs_map.append(new)
        new = []
    return bfs_map

# Create a grid to track a BFS across good and bad rays
bfs_map = initialize_twodlist(constants.THETAS, constants.PHIS)
xyz_coordinates = initialize_twodlist(constants.THETAS, constants.PHIS)

for name_i in FULL_LIST:
    ray_directions = np.load(f"{absPathRoot}/result_files_npy/{name_i}_directions.npy")
    results = np.load(f"{absPathRoot}/result_files_npy/{name_i}_results.npy")
    thetas = np.load(f"{absPathRoot}/result_files_npy/{name_i}_thetas.npy")
    phis = np.load(f"{absPathRoot}/result_files_npy/{name_i}_phis.npy")

    # Look at each direction and corresponding result
    for direction_j, results_j, theta_j, phi_j in zip(ray_directions, results, thetas, phis):
        direction_j = tuple(direction_j)
        if results_j == True:
            # In the case that the line intersects, we add it to the NON-CANDIDATES SET -- lines we can't see
            # We remove it from the candidates if it had been added as well
            if direction_j in CANDIDATES_SET:
                CANDIDATES_SET.remove(direction_j)
                # We're also tracking if each line is good or not in our BFS grid
                bfs_map[theta_j][phi_j] = 0
                xyz_coordinates[theta_j][phi_j] = (50 * direction_j[0] + driverHead[0], 50 * direction_j[1] + driverHead[1], 50 * direction_j[2] + driverHead[2])

            NONCANDIDATES_SET.add(direction_j)
        else:
            # If no intersection, we add the line to the candidates if it hasn't been blocked yet
            if not direction_j in NONCANDIDATES_SET:
                CANDIDATES_SET.add(direction_j)
                # We're also tracking if each line is visible or not in our BFS grid
                bfs_map[theta_j][phi_j] = 1
                xyz_coordinates[theta_j][phi_j] = (50 * direction_j[0] + driverHead[0], 50 * direction_j[1] + driverHead[1], 50 * direction_j[2] + driverHead[2])

# # THIS BLOCK OF CODE DRAWS IN THE SIGHTLINES WHICH ARE VISIBLE
# for i, direction_i in enumerate(CANDIDATES_SET):
#     sightline_end = [
#         50 * direction_i[0] + driverHead[0],
#         50 * direction_i[1] + driverHead[1],
#         50 * direction_i[2] + driverHead[2],
#     ]
#     my_create_line(driverHead, sightline_end, f"{i}")

# finds first 0 and starts there (first element in queue)
def find_first_zero(matrix):
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            if matrix[row][col] == 0:
                return ((row, col))

# We have a grid of lines which are visible and invisible, we now go through it to group together lines which are visible/not
# This will let us visualize a blind spot clearly
# We only want the border
# We use a breadth-first search to do this
queue = []
queue.append(find_first_zero(bfs_map))
visited = set()
border = set()
directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

# While there's still lines in the existing group, w ekee psearching
while queue:
    current_row, current_col = queue.pop(0)

    # If a line is not visible, then we check its surroundings
    if bfs_map[current_row][current_col] == 0:
        for dr, dc in directions:
            # We check each neighbor
            next_row, next_col = current_row + dr, current_col + dc

            # We visit all neighbouring areas if they have not been visited yet
            if 0 <= next_row < len(bfs_map) and 0 <= next_col < len(bfs_map[0]):
                if (next_row, next_col) not in visited:
                    queue.append((next_row, next_col))
                    visited.add((next_row, next_col))
                    
                    # if nearby areas are 1s (visible), we track this border
                    if bfs_map[next_row][next_col] == 1:
                        border.add((next_row, next_col))


# Function determining if two cells (rays) are adjacent in the BFS board
def are_adjacent_cells(cell_a, cell_b, num_rows, num_cols):
    if cell_a[0] == cell_b[0]:
        if abs(cell_a[1] - cell_b[1]) == 1 or abs(cell_a[1] - cell_b[1]) == num_cols - 1:
            return True
        
    if cell_a[1] == cell_b[1]:
        if abs(cell_a[0] - cell_b[0]) == 1 or abs(cell_a[0] - cell_b[0]) == num_rows - 1:
            return True
        
    return False

# Function determining if two cells (rays) are diagonal on the BFS board
def are_diagonal_cells(cell_a, cell_b, num_rows, num_cols):
    if abs(cell_a[0] - cell_b[0])%(num_rows - 2) == 1 and abs(cell_a[1] - cell_b[1]) %(num_cols - 2)== 1:
        return True
    
    return False

# We now want to sort our border cells to be in a single contiguous order
sorted_border = [border.pop()]

counter = 0
print(border)

# To do this, we continue until the border is depleted
# We start with a random part on the border and we look for adjacent pieces of the border
while len(border) > 0:
    i = 1
    prev_elem = sorted_border[-i]
    print(prev_elem)

    # This trigger is here in case we hit an infinite loop so we can break out -- this happens when parts of the border are essentially nested and won't be hit
    # Then we want to break out of the loop here since they are never depleted elements
    if len(sorted_border) == counter:
        break
    counter += 1

    # We look for a cell which is adjacent to the previous one
    found = False

    # We check for adjacent cells first -> these take priority
    for elem in border:
        # If we find one, place it into sorted order and move onto next element
        if are_adjacent_cells(elem, prev_elem, constants.THETAS, constants.PHIS):
            border.remove(elem)
            sorted_border.append(elem)
            found = True
            break
    # If no adjacent cell, try diagonal cells
    if not found:
        for elem in border:
            if are_diagonal_cells(elem, prev_elem, constants.THETAS, constants.PHIS):
                border.remove(elem)
                sorted_border.append(elem)
                found = True
                break


print(sorted_border)
# Now we draw each coordinate of the sorted border in order
xyz_points = []
for coordinate in sorted_border:
    #find (xyz) coordinate of border points
    if xyz_coordinates[coordinate[0]][coordinate[1]] != 0:
        xyz_points.append(xyz_coordinates[coordinate[0]][coordinate[1]])

# Create objects for each successive section of the border
for point in range(len(xyz_points)):
    p1 = xyz_points[point]
    if point == len(xyz_points) - 1:
        p2 = xyz_points[0]
    else:
        p2 = xyz_points[point+1]
    
    wire=Part.makePolygon([driverHead, p1, p2, driverHead])
    # obj = Part.show(wire)
    # vp = obj.ViewObject
    # vp.LineColor = (1.0, 0.0, 0.0)
    # vp.LineWidth = 2.0
    face=Part.Face(wire)
    obj=Part.show(face)
    vp = obj.ViewObject
    vp.ShapeColor = (1.0, 0.0, 0.0)
    vp.Transparency = 50
    
