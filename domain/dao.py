from persist import *

class Node():
    def __init__(self, prev_node_list, software, algorithm, parameters, result):
        self.prev_node_list = prev_node_list
        self.software = software
        self.algorithm = algorithm
        self.parameters =  parameters
        self.result = result