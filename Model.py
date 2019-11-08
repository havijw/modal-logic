class Model:
    # requires: worlds is a list of names of worlds as strings
    #           access is a set of tuples of elements of worlds,
    #               which define an accessibility function on worlds
    #           variables is a dictionary consisting of pairs
    #               proposition:[worlds at which proposition is true]
    def __init__(self, worlds=[], access=[], variables={}):
        self.worlds    = worlds
        self.access    = access
        self.variables = list(variables.keys())
