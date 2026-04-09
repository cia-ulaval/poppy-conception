from std_msgs.msg import String

class MotorMsgMapper:

    def __init__(self):
        self.NameIdMap = {
            "r_hip_x": 21,
            "r_hip_z": 22,
            "r_hip_y": 23,
            "r_knee_y": 24,
            "r_ankle_y": 25,
            "l_hip_x": 11,
            "l_hip_z": 12,
            "l_hip_y": 13,
            "l_knee_y": 14,
            "l_ankle_y": 15,
            "abs_y": 31,
            "abs_x": 32,
            "abs_z": 33,
            "bust_y": 34,
            "bust_x": 35,
            "head_z": 36,
            "head_y": 37,
            "l_shoulder_y": 41,
            "l_shoulder_x": 42,
            "l_arm_z": 43,
            "l_elbow_y": 44,
            "r_shoulder_y": 51,
            "r_shoulder_x": 52,
            "r_arm_z": 53,
            "r_elbow_y": 54
            }
            
            
    
    def _map_motor_name_to_id(self, motor_name:String) -> int:
        if motor_name in self.NameIdMap:
            return self.NameIdMap[motor_name]
        else:
            raise ValueError(f"Motor name '{motor_name}' not found in mapping.")

    def map_motor_names_to_ids(self, motor_names:list[String]) -> list:
        return [self._map_motor_name_to_id(name) for name in motor_names]

        
        