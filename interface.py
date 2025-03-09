import pybullet as p
import numpy as np

class Interface:

    def __init__(self, client_id):
        self.world_parent_id = client_id

        self.current_mode = 0 
        """ 1 : Mode Auto
            2 : Mode Manuel
            3 : Mode ..."""
        
        self.auto_button_id = p.addUserDebugParameter("Mode Auto", 1, 0, 1, physicsClientId=client_id)
        self.manual_button_id = p.addUserDebugParameter("Mode Manuel", 1, 0, 1, physicsClientId=client_id)

        self.param_AD_H = p.addUserDebugParameter("Joint AD_H Position", -2.356194, 0.785398, 0.0, physicsClientId=client_id)
        self.param_AD_V = p.addUserDebugParameter("Joint AD_V Position", -1.570796, 1.570796, 0.0, physicsClientId=client_id)

        self.param_AG_H = p.addUserDebugParameter("Joint AG_H Position", -2.356194, 0.785398, 0.0, physicsClientId=client_id)
        self.param_AG_V = p.addUserDebugParameter("Joint AG_V Position", -1.570796, 1.570796, 0.0, physicsClientId=client_id)

        self.param_DD_H = p.addUserDebugParameter("Joint DD_H Position", -2.356194, 0.785398, 0.0, physicsClientId=client_id)
        self.param_DD_V = p.addUserDebugParameter("Joint DD_V Position", -1.570796, 1.570796, 0.0, physicsClientId=client_id)

        self.param_DG_H = p.addUserDebugParameter("Joint DG_H Position", -2.356194, 0.785398, 0.0, physicsClientId=client_id)
        self.param_DG_V = p.addUserDebugParameter("Joint DG_V Position", -1.570796, 1.570796, 0.0, physicsClientId=client_id)

        
    def initAuto(self):
        pass

"""
    def initManual(self):
        self.param_AD_H = p.addUserDebugParameter("Joint AD_H Position", -2.356194, 0.785398, 0.0, physicsClientId=client_id)
        self.param_AD_V = p.addUserDebugParameter("Joint AD_V Position", -1.570796, 1.570796, 0.0, physicsClientId=client_id)

        self.param_AG_H = p.addUserDebugParameter("Joint AG_H Position", -2.356194, 0.785398, 0.0, physicsClientId=client_id)
        self.param_AG_V = p.addUserDebugParameter("Joint AG_V Position", -1.570796, 1.570796, 0.0, physicsClientId=client_id)

        self.param_DD_H = p.addUserDebugParameter("Joint DD_H Position", -2.356194, 0.785398, 0.0, physicsClientId=client_id)
        self.param_DD_V = p.addUserDebugParameter("Joint DD_V Position", -1.570796, 1.570796, 0.0, physicsClientId=client_id)

        self.param_DG_H = p.addUserDebugParameter("Joint DG_H Position", -2.356194, 0.785398, 0.0, physicsClientId=client_id)
        self.param_DG_V = p.addUserDebugParameter("Joint DG_V Position", -1.570796, 1.570796, 0.0, physicsClientId=client_id)
"""
