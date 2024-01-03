# Path to where this code is located
ABS_PATH_ROOT = 'C:/Data/Harvard/T4SG/f23-eng-cdc-niosh/blindspot'

# The location of the driver's head 
DRIVER_HEAD = (352.5016492337469, 339.719522252282, -105.5012320445894)

# List of objects in the mesh file which can obstruct view
FULL_LIST = ["_73f_Bucket_",
    "_73f_Tire_FrontLeft_Detached_",
    "_73f_Tire_BackRight_Detached_",
    "_73f_Tire_BackLeft_Detached_",
    "_73f_Tire_FrontRight_Detached_",
    "Chasis_Detached_",
    "AxleRear_Detached_",
    "BatteryUnit_Detached_",
    "PistonsRear_Detached_",
    "Platform_Detached_",
    "RearHydraulics_Detached_"] # "Cab_Detached_" is omitted, as we assume the windows are clear and so light should pass through them

# String for which component not to include
CAB = ['Cab_Detached_']