from IDGenerator import IDGenerator
from Zones.Site import Site
from Zones.Building import Building
from Zones.Storey import Storey
from Zones.Space import Space
import pathlib
import random

path_to_dfa_folder = str(pathlib.Path().absolute().as_posix())+"/DFAs/"

class DFABuilder():

    
    def append_to_design_DFA(design_id, type, length, width, height, x, y):
        # zone_id is for the children blocks added:
        zone_id = IDGenerator.create_dfa_zone_ID()
        
        f = open(path_to_dfa_folder + "Templates/" + type +".dfa", "r")
        txt = f.read()
        txt_replaced = txt.replace("<LENGTH>", str(length))
        txt_replaced = txt_replaced.replace("<WIDTH>", str(width))
        txt_replaced = txt_replaced.replace("<HEIGHT>", str(height))
        txt_replaced = txt_replaced.replace("block1", str(zone_id))
        txt_replaced = txt_replaced.replace("block2", str(zone_id) + "_X")
        txt_replaced = txt_replaced.replace("<X>", str(x))
        txt_replaced = txt_replaced.replace("<Y>", str(y))
        f.close()

        f = open(path_to_dfa_folder + "Products/" + design_id + ".dfa", "a")
        f.write(txt_replaced)
        f.close

    def make_design_template(): 
        #Design
        design_id = IDGenerator.create_design_ID()
        f = open(path_to_dfa_folder + "Templates/design.dfa", "r")
        txt = f.read()
        txt = txt.replace("<ID>", design_id) #TODO replace order 13 with automated id.
        f.close()
        #Design
        f = open(path_to_dfa_folder + "Products/" + design_id + ".dfa", "w")
        #TODO switch "building_12" with IDGenerator
        f.write(txt)
        f.close
        return design_id

    def generate_DFA(IDs_list):
        """
            DFABuilder.generate_DFA([site_id, building_id, storey_id, space_ids])
            Makes design template and adds all zones specified by their ids.
            Returns: path to produced dfa file.
            In future: generate_DFA() takes list of ids. If given site contains more buildings
            than what is given in the argument building_ids list, only the buildings given
            in the argument list will be colored, while the others are grey.
        """
        design_id = DFABuilder.make_design_template()

        site_id_list = IDs_list[0]
        for id in site_id_list:
            site_args = Site.get_args_from_KB(id)
            DFABuilder.append_to_design_DFA(design_id, "site", site_args[1], site_args[2], 1,0,0)

        building_id_list = IDs_list[1]
        for id in building_id_list:
            building_args = Building.get_args_from_KB(id)
            DFABuilder.append_to_design_DFA(design_id, "building", building_args[1], building_args[2], building_args[3], int(site_args[1])/2, int(site_args[2])/2)
        
        # Logical flaw... need to make sure these storey heights are applied to the right buildings
        print("building args:", building_args[0], building_args[1], building_args[2], building_args[3], building_args[4])
        height_of_storey = int(float(building_args[3])/float(len(building_args[5])))
        storey_id_list = IDs_list[2]
        for id in storey_id_list:        
            storey_args = Storey.get_args_from_KB(id)
            DFABuilder.append_to_design_DFA(design_id, "storey", building_args[1], building_args[2], height_of_storey, int(site_args[1])/2, int(site_args[2])/2)
        
        space_id_list = IDs_list[3]
        for space_id in space_id_list:
            print(space_id)
            space_args = Space.get_args_from_KB(space_id)
            print(len(space_args))
            print(space_args[0], space_args[1], space_args[2])
            DFABuilder.append_to_design_DFA(design_id, "Space", space_args[1], space_args[2], space_args[3], int(site_args[1])/2, int(site_args[2])/2)

        return path_to_dfa_folder+"Products/"+design_id+".dfa"
            
    def generate_DFA_with_existing_flats(floors):
        design_id = DFABuilder.make_design_template()
        for i in range(0, int(floors)):
            DFABuilder.append_existing_flat_to_design(i, random.randint(1, 3), design_id)
        return path_to_dfa_folder+"Products/"+design_id+".dfa"
        

    def append_existing_flat_to_design(floornumber, flatnumber, design_id): #floornumber starts at zero
        height = 3*floornumber
        uniqe = IDGenerator.create_dfa_zone_ID()
        f = open(path_to_dfa_folder + "/Templates/flat_" + str(flatnumber) +".dfa", "r")
        txt = f.read()
        txt = txt.replace("<HEIGHT>", str(height))
        txt = txt.replace("<UQ>", str(uniqe))
        f.close()

        f = open(path_to_dfa_folder + "Products/" + design_id + ".dfa", "a")
        f.write(txt)
        f.close        
