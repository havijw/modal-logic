class Model:
    # requires: worlds is a list of names of worlds as strings
    #           access is a set of tuples of elements of worlds,
    #               which define an accessibility function on worlds
    #           variables is a dictionary consisting of pairs
    #               proposition:[worlds at which proposition is true]
    def __init__(self, worlds=[], access=[], variables={}):
        self.worlds    = worlds
        self.access    = access
        self.variables = variables

    def valuation(self, variable, world):
        if variable not in self.variables:
            return False
        if world in self.variables[variable]:
            return True
        return False
    
    def __str__(self):
        return ''.join(['Worlds: ', str(self.worlds), '\nAccessibility Relations: ', str(self.access), 'Valuations: ', str(self.variables)])

def test_Model():
    worlds = ['w1', 'w2', 'w3', 'w4']
    access = [('w1', 'w2'), ('w2', 'w3'), ('w2', 'w2'), ('w1', 'w4')]
    variables = {'a':['w1', 'w3'], 'b':['w1', 'w2'], 'c':['w3', 'w4']}

    mod = Model(worlds, access, variables)
    print(mod)
    print('Model valuation of a at w2:', str(mod.valuation('a', 'w2')))

if __name__ == '__main__':
    test_Model()
