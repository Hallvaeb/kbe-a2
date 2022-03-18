from Zones.Zone import Zone
from IDGenerator import IDGenerator
import requests

URL = "http://127.0.0.1:3030/bot"

class Space(Zone):


    def __init__(self, args):
        if (len(args) == 1):
            self.__init__2(args)
        else:
            self.__init__1(args)
    
    def __init__1(self, args):
        """
            Adds prototype space to KB
        """
        # INPUT args: [length, width, height, energyEfficiency, role]
        self.type = "space"
        self.length = args[0]
        self.width = args[1]
        self.height = args[2]
        self.energyEfficiency = args[3]
        
        # Finding unique role:
        role_core = args[4]+"_"
        
        i = 1
        role = role_core + str(i)
        while(Space.is_role_in_KB(role)):
            i += 1
            role = role_core + str(i)
        self.role = role
        self.space_id = IDGenerator.create_space_prototype_ID(self)

        self.add_to_KB()
        return self
        

    def __init__2(self, args):
        """
            Space is being used and created in construction
        """
        # INPUT args: [role]
        self.type = "space"
        role = args[0]
        if not Space.is_role_in_KB(role):
            return -1 
        self.space_id = IDGenerator.create_space_prototype_ID(self)
        # TODO: get arguments of space with role
        # space_args = get_arguments_of_space_prototype(self.space_id)
        # self.length = space_args[0]
        # self.width = space_args[1]
        # self.height = space_args[2]
        # self.energyEfficiency = space_args[3]
        # self.role = space_args[4]



    def is_role_in_KB(role):
        QUERY = ('''
        PREFIX bot:<https://w3id.org/bot#>
		SELECT ?role 
		WHERE {
			?space bot:hasRole ?role.
		FILTER ( EXISTS { ?space bot:hasRole "''' + str(role) + '''"} )
		}
        ''')

        PARAMS = {"query": QUERY}
        r = requests.get(url = URL, params = PARAMS) 
        data = r.json()
		
        if (len(data['results']['bindings']) == 0 ):
            return 0
        return 1
        

    def add_to_KB(self):
        try:
            UPDATE = ('''
            PREFIX bot:<https://w3id.org/bot#>
            INSERT {
                bot:''' + str(self.space_id) + ''' a bot:Space.
                bot:''' + str(self.space_id) + ''' bot:hasLength "''' + str(self.length) + '''".
                bot:''' + str(self.space_id) + ''' bot:hasWidth "''' + str(self.width) + '''".
                bot:''' + str(self.space_id) + ''' bot:hasHeight "''' + str(self.height) + '''".
                bot:''' + str(self.space_id) + ''' bot:energyEfficiency "''' + str(self.energyEfficiency) + '''".
                bot:''' + str(self.space_id) + ''' bot:hasRole "''' + str(self.role) + '''".
                }
            WHERE {
            }
            ''')
            PARAMS = {"update": UPDATE}
            r = requests.post(url = URL+"/update", data = PARAMS) 
            return 1
        except:
            return 0
    
    def remove(self):

        try:
            UPDATE = ('''
            PREFIX bot:<https://w3id.org/bot#>
			DELETE {
                bot:''' + str(self.space_id) + ''' a bot:Space.
                bot:''' + str(self.space_id) + ''' bot:hasLength "''' + str(self.length) + '''".
                bot:''' + str(self.space_id) + ''' bot:hasWidth "''' + str(self.width) + '''".
                bot:''' + str(self.space_id) + ''' bot:hasHeight "''' + str(self.height) + '''".
                bot:''' + str(self.space_id) + ''' bot:energyEfficiency "''' + str(self.energyEfficiency) + '''".
                bot:''' + str(self.space_id) + ''' bot:hasRole "''' + str(self.role) + '''".
                }
            WHERE {
            bot:''' + str(self.space_id) + ''' a bot:Space.
            bot:''' + str(self.space_id) + ''' bot:hasLength "''' + str(self.length) + '''".
            bot:''' + str(self.space_id) + ''' bot:hasWidth "''' + str(self.width) + '''".
            bot:''' + str(self.space_id) + ''' bot:hasHeight "''' + str(self.height) + '''".
            bot:''' + str(self.space_id) + ''' bot:energyEfficiency "''' + str(self.energyEfficiency) + '''".
            bot:''' + str(self.space_id) + ''' bot:hasRole "''' + str(self.role) + '''".
                }''')
            
            PARAMS = {"update": UPDATE}
            r = requests.post(url = URL+"/update", data = PARAMS) 
            return 1
        except:
            return 0

    def add_zone(self, adjacent_space_id): #adds zones (here adjacent spaces) to the space as well as the list adjacentZones
        try:
            UPDATE = ('''
            PREFIX bot:<https://w3id.org/bot#>
            INSERT {
                bot:''' + str(self.space_id) + ''' a bot:Space.
                bot:''' + str(self.space_id) + ''' bot:adjacentZone bot:''' + str(adjacent_space_id) + '''.
                }
            WHERE {
            }
            ''')
            PARAMS = {"update": UPDATE}
            r = requests.post(url = URL+"/update", data = PARAMS) 
            
            #add the adjacent zone to the list of adjacent zones to this space.
            self.adjacentZones.append(str(adjacent_space_id))
            return 1
        except:
            return 0

    def get_args_from_KB(self):
        
        QUERY = ('''
        SELECT *
        WHERE {
	        ?space a bot:Space.
            ?space bot:hasLength ?length.
            ?space bot:hasWidth ?width.
            ?space bot:hasHeight ?height.
            ?space bot:energyEfficiency ?energyEfficiency.
            ?space bot:hasRole ?role
	        FILTER (EXISTS { ?space bot:hasRole "'''+str(self.role)+'''"})
}
        ''')

        PARAMS = {"query": QUERY}
        r = requests.get(url = URL, params = PARAMS) 
        data = r.json()
		
        if (len(data['results']['bindings']) == 0 ):
            return 0
        return 1
        
        
        pass

    def get_storey(self):
        pass
        #Må her inn i KB

    def get_zones(self):
        return self.adjacentZones

    def get_ID(self):
        return self.space_id

    def get_type(self):
        return self.type
    
    def get_height(self):
        return self.height

    def get_width(self):
        return self.width
    
    def get_length(self):
        return self.length

    def get_area(self):
        return self.length*self.width

    def get_volume(self):
        return self.length*self.width*self.height

    def get_energyEfficiency(self):
        return self.energyEfficiency


