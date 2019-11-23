from Model import Model

class Proof_Model(Model):
    def add_world(self, world_name, accessible_worlds=[], variables={}, propositions={}):
        if world_name not in self.worlds:
            self.worlds[world_name] = {
                'access'       : accessible_worlds, 
                'variables'    : variables, 
                'propositions' : propositions
            }
    
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
        
        return string_rep
