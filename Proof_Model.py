from Model import Model

class Proof_Model(Model):
    def add_world(self, world_name, accessible_worlds=[], variables={}, propositions={}):
        if world_name not in self.worlds:
            self.worlds[world_name] = {
                'access'       : accessible_worlds, 
                'variables'    : variables, 
                'propositions' : propositions
            }

    def is_accessible(self, world, world_to_access):
        if world_to_access in self.worlds[world]['access']:
            return True
        return False
    
    def add_access(self, world, world_to_access):
        if not self.is_accessible(world, world_to_access):
            self.worlds[world]['access'].append(world_to_access)
    
    def is_transitive(self):
        for world in self.worlds:
            for a_world in self.worlds[world]['access']:
                for a_a_world in self.worlds[a_world]['access']:
                    if not self.is_accessible(world, a_a_world):
                        return False
        return True
    
    def make_transitive(self):
        while not self.is_transitive():
            for world_1 in self.worlds:
                for world_2 in self.worlds[world_1]['access']:
                    for world_3 in self.worlds[world_2]['access']:
                        self.add_access(world_1, world_3)
    
    def is_symmetric(self):
        for world in self.worlds:
            for a_world in self.worlds[world]['access']:
                if not self.is_accessible(a_world, world):
                    return False
        return True
    
    def make_symmetric(self):
        for world in self.worlds:
            for a_world in self.worlds[world]['access']:
                self.add_access(a_world, world)
    
    def is_reflexive(self):
        for world in self.worlds:
            if not self.is_accessible(world, world):
                return False
        return True
    
    def make_reflexive(self):
        for world in self.worlds:
            self.add_access(world, world)
    
    def __str__(self):
        string_rep = ''
        for world in self.worlds:
            string_rep += world + ':\n  '

            string_rep += 'accessible worlds:'
            for accessible_world in self.worlds[world]['access']:
                string_rep += '\n    * ' + accessible_world
            string_rep += '\n  '

            string_rep += 'variables:'
            for variable in self.worlds[world]['variables']:
                string_rep += '\n    * ' + variable + ' -- ' + str(self.worlds[world]['variables'][variable])
            string_rep += '\n  '

            string_rep += 'propositions'
            for proposition in self.worlds[world]['propositions']:
                string_rep += '\n    * ' + proposition + ' -- ' + str(self.worlds[world]['propositions'][proposition])
            string_rep += '\n'
        
        return string_rep + '\n--------------------------------'
