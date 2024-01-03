import math
import FreeCAD as App
import Part
import numpy as np

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
    obj.X1 = pt1[0]
    obj.Y1 = pt1[1]
    obj.Z1 = pt1[2]

    obj.X2 = pt2[0]
    obj.Y2 = pt2[1]
    obj.Z2 = pt2[2]

    App.ActiveDocument.recompute()
    return obj

driverHead = (352.5016492337469, 339.719522252282, -105.5012320445894)

FULL_LIST = [
    "_73f_Bucket_",
    "_73f_Tire_FrontLeft_Detached_",
    "_73f_Tire_BackRight_Detached_",
    "_73f_Tire_BackLeft_Detached_",
    "_73f_Tire_FrontRight_Detached_",
    "Chasis_Detached_",
    "AxleRear_Detached_",
    "BatteryUnit_Detached_",
    "PistonsRear_Detached_",
    "Platform_Detached_",
    "RearHydraulics_Detached_",
] 

doc = App.ActiveDocument

CANDIDATES_SET = set()
NONCANDIDATES_SET = set()

def initialize_twodlist():
    bfs_map = []
    new = []
    for i in range (0, 30):
        for j in range (0, 15):
            new.append(0)
        bfs_map.append(new)
        new = []
    return bfs_map

bfs_map = initialize_twodlist()
xyz_coordinates = initialize_twodlist()

for name_i in FULL_LIST:

    absPathRoot = 'C:/Data/Harvard/T4SG/f23-eng-cdc-niosh/blindspot'
    ray_directions = np.load(f"{absPathRoot}/result_files_npy/{name_i}_directions.npy")
    results = np.load(f"{absPathRoot}/result_files_npy/{name_i}_results.npy")
    thetas = np.load(f"{absPathRoot}/result_files_npy/{name_i}_thetas.npy")
    phis = np.load(f"{absPathRoot}/result_files_npy/{name_i}_phis.npy")

    for direction_j, results_j, theta_j, phi_j in zip(ray_directions, results, thetas, phis):
        direction_j = tuple(direction_j)
        if results_j == True:
            # Intersects
            if direction_j in CANDIDATES_SET:
                CANDIDATES_SET.remove(direction_j)
                bfs_map[theta_j][phi_j] = 0
                xyz_coordinates[theta_j][phi_j] = (50 * direction_j[0] + driverHead[0], 50 * direction_j[1] + driverHead[1], 50 * direction_j[2] + driverHead[2])

            NONCANDIDATES_SET.add(direction_j)
        else:
            # No intersection
            if not direction_j in NONCANDIDATES_SET:
                CANDIDATES_SET.add(direction_j)
                bfs_map[theta_j][phi_j] = 1
                xyz_coordinates[theta_j][phi_j] = (50 * direction_j[0] + driverHead[0], 50 * direction_j[1] + driverHead[1], 50 * direction_j[2] + driverHead[2])

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

#bfs setup
queue = []
queue.append(find_first_zero(bfs_map))
visited = set()
border = set()
directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

while queue:
    current_row, current_col = queue.pop(0)

    if bfs_map[current_row][current_col] == 0:
        for dr, dc in directions:
            next_row, next_col = current_row + dr, current_col + dc

            if 0 <= next_row < len(bfs_map) and 0 <= next_col < len(bfs_map[0]):
                if (next_row, next_col) not in visited:
                    queue.append((next_row, next_col))
                    visited.add((next_row, next_col))
                    if bfs_map[next_row][next_col] == 1:
                        border.add((next_row, next_col))
# , key=lambda x: x[1]       
# 

def are_adjacent_cells(cell_a, cell_b, num_rows, num_cols):
    if cell_a[0] == cell_b[0]:
        if abs(cell_a[1] - cell_b[1]) == 1 or abs(cell_a[1] - cell_b[1]) == num_cols - 1:
            return True
        
    if cell_a[1] == cell_b[1]:
        if abs(cell_a[0] - cell_b[0]) == 1 or abs(cell_a[0] - cell_b[0]) == num_rows - 1:
            return True
        
    return False

def are_diagonal_cells(cell_a, cell_b, num_rows, num_cols):
    if abs(cell_a[0] - cell_b[0]) == 1 and abs(cell_a[1] - cell_b[1]) == 1:
        return True
    
    return False

sorted_border = [border.pop()]

counter = 0

while len(border) > 0:
    prev_elem = sorted_border[-1]

    if len(sorted_border) == counter:
        break

    
    counter += 1
    found = False
    for elem in border:
        if are_adjacent_cells(elem, prev_elem, 30, 15):
            border.remove(elem)
            sorted_border.append(elem)
            found = True
            break
    if not found:
        for elem in border:
            if are_diagonal_cells(elem, prev_elem, 30, 15):
                border.remove(elem)
                sorted_border.append(elem)
                break

xyz_points = []
for coordinate in sorted_border:
    #find (xyz) coordinate of border points
    if xyz_coordinates[coordinate[0]][coordinate[1]] != 0:
        xyz_points.append(xyz_coordinates[coordinate[0]][coordinate[1]])

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
    
