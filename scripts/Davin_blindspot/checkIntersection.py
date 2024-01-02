import numpy as np
import trimesh
import math

import os, sys
sys.path.append(os.path.dirname(__file__))

import constants

driverHead = constants.DRIVER_HEAD

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

def generateSightLineDirections(N = 200):
    
    vectors = []
    inverseGoldenRatio = (5**0.5 - 1)/2

    ray_origin = []
    ray_directions = []

    for i in range(0, N):
        theta = 2 * math.pi * i * inverseGoldenRatio
        phi = math.acos(1 - 2 * (i+0.5) / N)

        ray_origin.append(driverHead)
        direction = ( math.cos(theta) * math.sin(phi) * 100, math.sin(theta) * math.sin(phi) * 100, math.cos(phi) * 100 )
        ray_directions.append(
            (round(direction[0], 6), round(direction[1], 6), round(direction[2], 6))
        )

    return ray_origin, ray_directions 

for name_i in FULL_LIST:
    print(name_i)
    absPathRoot = constants.ABS_PATH_ROOT
    points_i = np.load(f'{absPathRoot}/mesh_files_npy/{name_i}_points.npy')
    faces_i = np.load(f'{absPathRoot}/mesh_files_npy/{name_i}_faces.npy')

    mesh = trimesh.Trimesh(vertices = points_i, faces = faces_i)
    mesh = trimesh.ray.ray_triangle.RayMeshIntersector(mesh)
    
    ray_origin, ray_directions = generateSightLineDirections(300)
    
    ret = mesh.intersects_any(ray_origin, ray_directions)

    np.save(f"{absPathRoot}/result_files_npy/{name_i}_directions.npy", np.array(ray_directions))
    np.save(f"{absPathRoot}/result_files_npy/{name_i}_results.npy", np.array(ret))