import xml.etree.ElementTree as ET
import pybullet as p
import os
import trimesh


def stl_to_obj(input_stl, folder_stl):
    # Charger le fichier STL
    mesh = trimesh.load_mesh(os.path.join(folder_stl, input_stl+".stl"))
    
    # Exporter en format OBJ
    output_obj = "collision_form/"+input_stl+".obj"
    mesh.export(os.path.join(folder_stl, output_obj))


def convert_vhacd2(input_obj, folder_stl) :
    p.connect(p.DIRECT)

    output_obj = os.path.join(folder_stl, "collision_form/"+input_obj+"_vhacd2.obj")
    name_log = "Robot_mesh_urdf/log.txt"

    p.vhacd(os.path.join(folder_stl, "collision_form/"+input_obj+".obj"), output_obj, name_log, depth=10)

def update_urdf(input_stl_list, folder_obj) :
    # Create new urdf
    root = urdf_tree.getroot()

    # Parcours tous les liens du fichier
    for link in root.findall("link"):
        name = link.get("name")  # Récupère le nom du link
        
        if name in input_stl_list:
            print(f"Modification de {name}")
            
            collision = link.find("collision")
            if collision is not None:
                mesh = collision.find(".//mesh")
                if mesh is not None:
                    ancien_fichier = mesh.get("filename")
                    nouveau_fichier = folder_obj + "/" + name + "_vhacd2.obj"

                    # Mettre à jour le nom du fichier
                    mesh.set("filename", nouveau_fichier)
                    print(f"  → {ancien_fichier} remplacé par {nouveau_fichier}")

    # Sauvegarder le fichier modifié
    urdf_tree.write("Robot_mesh_urdf/RobotSpider_With_Col.urdf", encoding="utf-8", xml_declaration=True)



##############################################################################
#############################       Param      ###############################
##############################################################################



folder_stl = "Robot_mesh_urdf/meshes"
folder_obj = "meshes/collision_form"
urdf_tree = ET.parse("Robot_mesh_urdf/RobotSpider.urdf")

input_stl_list = ["Patte_AD", "Patte_AG", "Patte_DD", "Patte_DG", "Rotation_Horrizontale_AD", "Rotation_Horrizontale_AG", "Rotation_Horrizontale_DD", "Rotation_Horrizontale_DG"]


for input_stl in input_stl_list :
        stl_to_obj(input_stl, folder_stl)
        convert_vhacd2(input_stl, folder_stl)
        os.remove(os.path.join(folder_stl, "collision_form/"+input_stl+".obj"))

update_urdf(input_stl_list, folder_obj)

##############################################################################




