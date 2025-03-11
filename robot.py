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
        self.q[1] = p.readUserDebugParameter(interface.param_AD_H, physicsClientId=interface.world_parent_id)
        self.q[3] = p.readUserDebugParameter(interface.param_AD_V, physicsClientId=interface.world_parent_id)
        self.q[13] = p.readUserDebugParameter(interface.param_AG_H, physicsClientId=interface.world_parent_id)
        self.q[15] = p.readUserDebugParameter(interface.param_AG_V, physicsClientId=interface.world_parent_id)
        self.q[9] = p.readUserDebugParameter(interface.param_DD_H, physicsClientId=interface.world_parent_id)
        self.q[11] = p.readUserDebugParameter(interface.param_DD_V, physicsClientId=interface.world_parent_id)
        self.q[5] = p.readUserDebugParameter(interface.param_DG_H, physicsClientId=interface.world_parent_id)
        self.q[7] = p.readUserDebugParameter(interface.param_DG_V, physicsClientId=interface.world_parent_id)


    ############################################################################################
    #########################             Autonomous Mode            ###########################
    ############################################################################################

    def init_auto_pos(self):
        self.q[1] = -np.pi/6
        self.q[3] = 0
        
        self.q[13] = -np.pi/6
        self.q[15] = 0
        
        self.q[9] = -np.pi/6
        self.q[11] = 0
        
        self.q[5] = -np.pi/6
        self.q[7] = 0



    def autonomous_move(self, t, 
                        A_hip=0.785398, A_knee=0.2, 
                        omega=2*np.pi, delta=np.pi/2, 
                        q_offset=1, phase_offset=np.pi/6):

        """
        Paramètres corrigés pour un trot synchrone :
        t        : temps
        A_hip    : amplitude hanche (mouvement avant/arrière)
        A_knee   : amplitude genou (négatif pour la levée de patte)
        omega    : pulsation (2π = 1 Hz)
        delta    : déphasage hanche/genou (π/2 pour lever après la poussée)
        q_offset : écartement de base des hanches pour éviter un chevauchement"
        """
    
        
        # Configuration des phases pour un TROT (diagonales synchronisées)
        phases = {
            'AG': 0,          # Avant Gauche phase 0
            'ARD': phase_offset,         # Arrière Droite phase 0 (diagonale synchrone)
            'AD': np.pi + phase_offset,      # Avant Droite phase π
            'ARG': np.pi + phase_offset      # Arrière Gauche phase π
        }

        # Pattes Avant Gauche (AG) et Arrière Droite (ARD)
        self.q[1] = -q_offset + A_hip * np.sin(omega * t + phases['AG'])   # Hanche AG
        self.q[3] = A_knee * np.sin(omega * t + phases['AG'] + delta)     # Genou AG
        self.q[5] = -q_offset + A_hip * np.sin(omega * t + phases['ARD'])  # Hanche ARD
        self.q[7] = A_knee * np.sin(omega * t + phases['ARD'] + delta)    # Genou ARD

        # Pattes Avant Droite (AD) et Arrière Gauche (ARG)
        self.q[13] = -q_offset + A_hip * np.sin(omega * t + phases['AD'])  # Hanche AD
        self.q[15] = A_knee * np.sin(omega * t + phases['AD'] + delta)     # Genou AD
        self.q[9] = -q_offset + A_hip * np.sin(omega * t + phases['ARG'])  # Hanche ARG
        self.q[11] = A_knee * np.sin(omega * t + phases['ARG'] + delta)    # Genou ARG

        return self.q
