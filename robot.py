import pybullet as p
import numpy as np

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

    def autonomous_move(self, t, 
                        A_hip=0.5, A_knee=0.5, 
                        omega=2*np.pi, delta=np.pi/4):
        """
        Parametres :
        t      : temps (float)
        A_hip  : amplitude pour l'articulation de hanche
        A_knee : amplitude pour l'articulation de genou
        omega  : fréquence angulaire du cycle de marche
        delta  : déphasage entre hanche et genou pour une même patte

        Return :
        numpy.array de 8 angles (en radians)
        """
        # Déphasages pour chaque patte.
        # Ici, pour un trot, on oppose les pattes diagonales :
        # Patte avant gauche (AG) et patte arrière droite (ARD) : phase 0
        # Patte avant droite (AD) et patte arrière gauche (ARG) : phase pi
        phases = {
            'AG': 0,
            'AD': np.pi,
            'ARG': np.pi,
            'ARD': 0
        }
        
        # Initialisation du vecteur de 8 joints
        q = np.zeros(8)
        
        # Calcul pour chaque patte
        self.q[1] = A_hip * np.sin(omega * t + phases['AG'])
        self.q[3] = A_knee * np.sin(omega * t + phases['AG'] + delta)
        
        self.q[13] = A_hip * np.sin(omega * t + phases['AD'])
        self.q[15] = A_knee * np.sin(omega * t + phases['AD'] + delta)
        
        self.q[9] = A_hip * np.sin(omega * t + phases['ARG'])
        self.q[11] = A_knee * np.sin(omega * t + phases['ARG'] + delta)
        
        self.q[5] = A_hip * np.sin(omega * t + phases['ARD'])
        self.q[7] = A_knee * np.sin(omega * t + phases['ARD'] + delta)
