import numpy as np
import trimesh
import math

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

'''
generateSightLines():
Parameters: 
- n, the number of sightlines
- origin, (x, y, z) coordinates of the camera
Returns: a list of n sightlines, each a vector from the given origin

Sources: 
- https://arxiv.org/pdf/0912.4540.pdf
- https://extremelearning.com.au/how-to-evenly-distribute-points-on-a-sphere-more-effectively-than-the-canonical-fibonacci-lattice/
'''

def generateSightLineDirections(N = 200):
    
    vectors = []
    inverseGoldenRatio = (5**0.5 - 1)/2

    for i in range(0, N):
        theta = 2 * math.pi * i * inverseGoldenRatio
        phi = math.acos(1 - 2 * (i+0.5) / N)

        direction = ( math.cos(theta) * math.sin(phi) * 100, math.sin(theta) * math.sin(phi) * 100, math.cos(phi) * 100 )
        vectors.append(
            (round(direction[0], 6), round(direction[1], 6), round(direction[2], 6))
        )

    return vectors 

def generateSightLineDirectionsGridded(theta_angles = 30, phi_angles = 15):
    
    ray_directions = []
    ray_origin = []
    thetas = []
    phis = []

    for i in range(0, theta_angles):
        for j in range(0, phi_angles):
            theta = 2 * math.pi * i / theta_angles
            phi = math.pi * j / phi_angles
            thetas.append(i)
            phis.append(j)
            ray_origin.append(driverHead)
            direction = (math.cos(theta) * math.sin(phi) * 100, math.sin(theta) * math.sin(phi) * 100, math.cos(phi) * 100 )
            ray_directions.append((round(direction[0], 6), round(direction[1], 6), round(direction[2], 6)))

    return ray_origin, ray_directions, thetas, phis


for name_i in FULL_LIST:
    absPathRoot = 'C:/Data/Harvard/T4SG/f23-eng-cdc-niosh/blindspot'
    points_i = np.load(f'{absPathRoot}/mesh_files_npy/{name_i}points.npy')
    faces_i = np.load(f'{absPathRoot}/mesh_files_npy/{name_i}faces.npy')

    mesh = trimesh.Trimesh(vertices = points_i, faces = faces_i)
    mesh = trimesh.ray.ray_triangle.RayMeshIntersector(mesh)
    
    ray_origin, ray_directions, thetas, phis = generateSightLineDirectionsGridded()
    ret = mesh.intersects_any(ray_origin, ray_directions)

    np.save(f"{absPathRoot}/result_files_npy/{name_i}_directions.npy", np.array(ray_directions))
    np.save(f"{absPathRoot}/result_files_npy/{name_i}_results.npy", np.array(ret))
    np.save(f"{absPathRoot}/result_files_npy/{name_i}_thetas.npy", np.array(thetas))
    np.save(f"{absPathRoot}/result_files_npy/{name_i}_phis.npy", np.array(phis))
