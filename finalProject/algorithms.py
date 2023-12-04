from node import *
from player import *
import random

class Algorithms:
    def __init__(self, food_positions):
        self.name = ""
        self.start_node = Node(player(0, 0, 0, 0), [[]], 0, 0, [], 0)
        self.solution = []
        self.solution_ptr = 0
        self.explore_ptr = 0
        self.depth = 1
        self.nodes = 1
        self.check_list = []
        self.explored = []
        self.cost = 0
        self.food_positions = food_positions
        self.goal_position = (-1, -1)
        
    def depth_first_search(self):
        self.check_list.append(self.start_node)
        while self.check_list:
            node = self.check_list.pop()
            self.nodes += 1
            if not self.start_node.compare(node) and not self.is_in_explored(node):
                self.start_node = node.copy()
                if node.is_goal:
                    self.solution = node.path
                    self.depth = node.depth
                return
            self.explored.append(node)
            node.expand()
            neighbor_indices = [i for i in range(len(node.nodes))]
            for _ in range(len(node.nodes)):
                i = random.choice(neighbor_indices)
                neighbor_indices.remove(i)
                if not self.is_in_explored(node.nodes[i]):
                    self.check_list.append(node.nodes[i])
                    
    def breadth_first_search(self):
        self.check_list.insert(0, self.start_node)
        while self.check_list:
            node = self.check_list.pop(0)
            if not self.start_node.compare(node) and not self.is_in_explored(node):
                self.start_node = node.copy()
                if node.is_goal:
                    self.solution = node.path
                    self.depth = node.depth
                return
            self.explored.append(node)
            node.expand()
            for i in range(len(node.nodes)):
                if not self.is_in_explored(node.nodes[i]):
                    self.check_list.append(node.nodes[i])
                    self.nodes += 1
                    
    def uniform_cost_search(self):
        self.check_list.insert(0, self.start_node)
        while self.check_list:
            self.sort_check_list("ucs")
            node = self.check_list.pop(0)
            if not self.start_node.compare(node) and not self.is_in_explored(node):
                self.start_node = node.copy()
                if node.is_goal:
                    self.solution = node.path
                    self.depth = node.depth
                    self.cost = node.cost
                return
            self.explored.append(node)
            node.expand()
            for i in range(len(node.nodes)):
                if not self.is_in_explored(node.nodes[i]):
                    self.check_list.append(node.nodes[i])
                    self.nodes += 1
                    
    def greedy_search(self):
        if self.goal_position == (-1, -1):
            self.find_nearest_food()
        self.check_list.insert(0, self.start_node)
        while self.check_list:
            self.sort_check_list("greedy")
            node = self.check_list.pop(0)
            if not self.start_node.compare(node) and not self.is_in_explored(node):
                self.start_node = node.copy()
                if node.is_goal:
                    self.solution = node.path
                    self.depth = node.depth
                    self.cost = node.heuristic_value
                return
            self.explored.append(node)
            node.expand()
            for i in range(len(node.nodes)):
                if not self.is_in_explored(node.nodes[i]):
                    node.nodes[i].heuristic_value = self.heuristic(node.nodes[i])
                    self.check_list.append(node.nodes[i])
                    self.nodes += 1 
                    
    def a_star_search(self):
        if self.goal_position == (-1, -1):
            self.find_nearest_food()
        self.check_list.insert(0, self.start_node)
        while self.check_list:
            self.sort_check_list("a_star")
            node = self.check_list.pop(0)
            if not self.start_node.compare(node) and not self.is_in_explored(node):
                self.start_node = node.copy()
                if node.is_goal:
                    self.solution = node.path
                    self.depth = node.depth
                    self.cost = node.cost + node.heuristic_value
                return
            self.explored.append(node)
            node.expand()
            for i in range(len(node.nodes)):
                if not self.is_in_explored(node.nodes[i]):
                    node.nodes[i].heuristic_value = self.heuristic(node.nodes[i])
                    self.check_list.append(node.nodes[i])
                    self.nodes += 1
                
    def is_in_explored(self, node):
        for i in range(len(self.explored)):
            if node.compare(self.explored[i]):
                return True
        return False
            
    def sort_check_list(self, mode):
        length = len(self.check_list)
        for i in range(length - 1):
            if mode == "ucs":
                min_cost = self.check_list[i].cost
            if mode == "a_star":
                min_f = self.check_list[i].cost + self.check_list[i].heuristic_value
            min_id = i
            for j in range(1, length):
                if mode == "ucs" and self.check_list[j].cost < min_cost:
                    min_cost = self.check_list[j].cost
                    min_id = j
                if mode == "a_star" and (self.check_list[j].cost + self.check_list[j].heuristic_value) < min_f:
                    min_f = (self.check_list[j].cost + self.check_list[j].heuristic_value)
                    min_id = j
            if min_id != i:
                self.check_list[i], self.check_list[min_id] = self.check_list[i].swap(self.check_list[min_id])
 

    def find_nearest_food(self):
        current_x, current_y = self.start_node.PacMan.get_matrix_position()
        nearest_food_position = None
        nearest_food_distance = float('inf')
        for food_position in self.food_positions:
            food_x, food_y = food_position
            distance = ((food_x - current_x) ** 2 + (food_y - current_y) ** 2) ** 0.5
            if distance < nearest_food_distance:
                nearest_food_distance = distance
                nearest_food_position = food_position
        self.goal_position = nearest_food_position

    def heuristic(self, node):
        PacMan_x, PacMan_y = node.PacMan.get_matrix_position()
        return (abs(PacMan_y - self.goal_position[0]) + abs(PacMan_x - self.goal_position[1])) * 1.5
