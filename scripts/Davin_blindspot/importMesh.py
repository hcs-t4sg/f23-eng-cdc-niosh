from tqdm import tqdm
import numpy as np
import trimesh

def importDocument():
    parts_list = [
        "773f_Bucket",
        "773f_Tire_FrontLeft_Detached",
        "773f_Tire_BackRight_Detached",
        "773f_Tire_BackLeft_Detached",
        "773f_Tire_FrontRight_Detached",
        "Chasis_Detached",
        "AxleRear_Detached",
        "BatteryUnit_Detached",
        "Cab_Detached",
        "PistonsRear_Detached",
        "Platform_Detached",
        "RearHydraulics_Detached",
    ]

    for part_i in (pbar := tqdm(parts_list)):
        pbar.set_description(f"Processing {part_i}")
        mesh = trimesh.load(f"mesh_files/{part_i}.stl", force='mesh')

        print("Watertightness:", mesh.is_watertight)
        print("Euler number:", mesh.euler_number)


importDocument()
