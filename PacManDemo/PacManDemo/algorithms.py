from node import *

class Algorithms:
    def __init__(self):
        self.solution = []
        self.sol_ptr = 0
        self.depth = 1
        self.nodes = 1
        self.check_list = []
        self.explored = []

    def depth_first_search(self, start_node):
        self.check_list.append(start_node)
        while self.check_list:
            node = self.check_list.pop()
            self.explored.append(node)
            if not start_node.compare(node):
                self.solution.append(node.direction)
                self.depth += 1
                self.nodes += 1
                return
            node.expand()
            neighbor_indices = [i for i in range(len(node.nodes))]
            for _ in range(len(node.nodes)):
                i = random.choice(neighbor_indices)
                neighbor_indices.remove(i)
                if not self.is_in_explored(node.nodes[i]):
                    self.check_list.append(node.nodes[i])
                    
    # def breadth_first_search(self, start_node):
    #     self.check_list.append(start_node)
    #     while self.check_list:
    #         node = self.check_list.pop()
    #         self.explored.append(node)
    #         if not start_node.compare(node):
    #             self.solution.append(node.direction)
    #             self.depth += 1
    #             self.nodes += 1
    #             return
    #         node.expand_randomly()
    #         for i in range(len(node.nodes)):
    #             if not self.is_in_explored(node.nodes[i]):
    #                 self.check_list.append(node.nodes[i])
                
    def is_in_explored(self, node):
        for i in range(len(self.explored)):
            if node.compare(self.explored[i]):
                return True
        return False
            
            
    