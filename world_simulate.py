import pybullet as p
import pybullet_data

from robot import Robot
from interface import Interface

class WorldSimulate:

    def __init__(self, client_type, env_path, robot_path):
        self.client_type = client_type
        self.client_id = p.connect(client_type)

        self.ground_id = self.load_world(env_path)
        self.bot = self.load_object(robot_path)

        self.interface = Interface(self.client_id) if client_type == p.GUI else None


    def load_world(self, env_path):
        """
        Load env_path
        Parameters: 
            env_path (str) : URDF file of env_path
        Returns: 
            ground_id (int) : Index of the PyBullet object
        """
        
        p.setAdditionalSearchPath(pybullet_data.getDataPath(), physicsClientId=self.client_id)  # used by loadURDF
        p.setGravity(0, 0, -9.81, physicsClientId=self.client_id)

        ground_id = p.loadURDF(env_path, physicsClientId=self.client_id)
        
        return ground_id

    def load_object(self, robot_path):
        """
        Load robot
        Parameters: 
            robot_path (str) : URDF file of robot
        Returns: 
            robot (Robot) : Object of class Robot
        """
        robot_start_pos = [0, 0, 0.2]
        robot_start_orientation = p.getQuaternionFromEuler([0, 0, 0])
    
        bot = Robot(self.client_id, 
                        robot_path, 
                        robot_start_pos, 
                        robot_start_orientation)
        
        p.changeVisualShape(bot.id, -1, rgbaColor=[0.6, 0, 0, 1], physicsClientId=self.client_id) 
        for i in range(0, 16) :
            if i%2 == 0:
                p.changeVisualShape(bot.id, i, rgbaColor=[0, 0, 0, 1], physicsClientId=self.client_id)  # Noir
            else :
                p.changeVisualShape(bot.id, i, rgbaColor=[0.6, 0, 0, 1], physicsClientId=self.client_id)  # Rouge

            
        return bot
