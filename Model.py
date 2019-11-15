class Model:
    # worlds should be a dictionary with entries:
    #   * 'access', corresponding to a list of accessible worlds
    #   * 'variables', corresponding to a list of variables that are true at the world
    def __init__(self, worlds={}):
        self.worlds = worlds
    
    def add_world(self, world_name, accessible_worlds, true_variables):
        self.worlds[world_name] = {'access' : accessible_worlds, 'variables' : true_variables}
    
    def __str__(self):
        string_rep = ''
        for world in self.worlds:
            string_rep += world + ':\n  '

            string_rep += 'accessible worlds:'
            for accessible_world in self.worlds[world]['access']:
                string_rep += '\n    * ' + accessible_world
            string_rep += '\n  '

            string_rep += 'true variables:'
            for variable in self.worlds[world]['variables']:
                string_rep += '\n    * ' + variable
            string_rep += '\n'
        
        return string_rep

def test_Model():
    model = Model({
        'w1' : {
            'access' : ['w2'], 'variables' : ['t', 'x', 'v']
        },
        'w2' : {
            'access' : ['w1', 'w2'], 'variables' : ['x', 'y', 't']
        }
    })
    model.add_world('w3', ['w1', 'w2', 'w3'], ['x', 'y', 'z'])
    print(model)

if __name__ == '__main__':
    test_Model()
