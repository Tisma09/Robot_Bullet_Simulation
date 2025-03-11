import time
import keyboard
import pybullet as p

from world_simulate import WorldSimulate 



################################################################################################
#########################               Main                    ################################
################################################################################################


physics_world = WorldSimulate(p.GUI, "plane.urdf", "Robot_mesh_urdf/RobotSpider_With_Col.urdf")

p.resetDebugVisualizerCamera(
    cameraDistance=0.4,             # Zoom (augmenter pour dézoomer)
    cameraYaw=50,                   # Angle de rotation (0 = face avant)
    cameraPitch=-35,                # Inclinaison vers le bas (-30 pour une vue plongeante)
    cameraTargetPosition=[0, 0, 0], # Point que la caméra vise (centre du robot)
    physicsClientId=physics_world.client_id
)
# DEBUG
#p.configureDebugVisualizer(p.COV_ENABLE_WIREFRAME, 1)


T = 1.0 / 240.0  # Temps cible pour un pas de simulation à 240 Hz
t= 0

while True:
    start_time = time.time()



    # Mode auto
    if p.readUserDebugParameter(physics_world.interface.auto_button_id) % 2 == 0 and physics_world.interface.current_mode == 0 :
        print("Start Auto mode")
        physics_world.interface.init_auto()
        physics_world.bot.init_auto_pos()
    elif p.readUserDebugParameter(physics_world.interface.auto_button_id) % 2 == 1 and physics_world.interface.current_mode == 1 :
        print("End Auto mode")
        physics_world.interface.end_auto()
    # Mode manuel
    elif p.readUserDebugParameter(physics_world.interface.manual_button_id) % 2 == 0 and physics_world.interface.current_mode == 0 :
        print("Start Manual mode")
        physics_world.interface.init_manual()
    elif p.readUserDebugParameter(physics_world.interface.manual_button_id) % 2 == 1 and physics_world.interface.current_mode == 2 :
        print("End Manual mode")
        physics_world.interface.end_manual()
    

    # Move mode
    if physics_world.interface.current_mode == 1 :
        physics_world.bot.autonomous_move(t)
        #keys = p.getKeyboardEvents()
        #if 32 in keys and keys[32] & p.KEY_WAS_TRIGGERED:
            
    if physics_world.interface.current_mode == 2 :
        physics_world.bot.manual_move(physics_world.interface)
    
    # Mise à jour des positions des moteurs
    for joint_index, position in enumerate(physics_world.bot.q):
        if joint_index < physics_world.bot.num_joints: 
            p.setJointMotorControl2(
                bodyIndex=physics_world.bot.id,
                jointIndex=joint_index,
                controlMode=p.POSITION_CONTROL,
                targetPosition=position,
                force=10,
                physicsClientId = physics_world.client_id
            )


    # Avance simulation
    p.stepSimulation(physicsClientId=physics_world.client_id)

     # Calculs temps
    elapsed_time = time.time() - start_time
    sleep_time = max(0, T - elapsed_time)
    time.sleep(sleep_time)
    t += sleep_time

    if keyboard.is_pressed('q'): 
        print("Simulation terminée.")
        break


p.disconnect()