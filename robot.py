import pybullet as p
import numpy as np
import math

from interface import Interface

class Robot:

    def __init__(self, client_id, path, robot_start_pos, robot_start_orientation):

        self.world_parent_id = client_id
        self.id = p.loadURDF(path, 
                            robot_start_pos, 
                            robot_start_orientation,
                            flags=p.URDF_USE_SELF_COLLISION | p.URDF_USE_SELF_COLLISION_EXCLUDE_PARENT,
                            physicsClientId=client_id)
        self.num_joints = p.getNumJoints(self.id, physicsClientId=client_id)
        self.q = np.zeros(self.num_joints)


    ############################################################################################
    #########################               Manual Mode              ###########################
    ############################################################################################

    def manual_move(self, interface) :
        """
        Mouvement en mode manuel puis vérification de collision
        Parameters: 
            debug_parameters
        Returns:
        """
        self.q[1] = p.readUserDebugParameter(interface.param_ARR_H, physicsClientId=interface.world_parent_id)
        self.q[2] = p.readUserDebugParameter(interface.param_ARR_V1, physicsClientId=interface.world_parent_id)
        self.q[3] = p.readUserDebugParameter(interface.param_ARR_V2, physicsClientId=interface.world_parent_id)

    ############################################################################################
    #########################             Autonomous Mode            ###########################
    ############################################################################################

    def init_auto_pos(self):
        pass



    def autonomous_move(self):
        pass
