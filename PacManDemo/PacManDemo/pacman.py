class PacMan:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.turn_allowed = [False, False, False, False]
        self.direction = ""
        self.state = "stop"
        
    def find_position(self):
        x = self.x + 1
        y = self.y + 1
        return y, x
     
    def move(self):
        if self.direction == "u" and self.turn_allowed[0]:
            self.y -= 1
        elif self.direction == "r" and self.turn_allowed[1]:
            self.x += 1
        elif self.direction == "d" and self.turn_allowed[2]:
            self.y += 1
        elif self.direction == "l" and self.turn_allowed[3]:
            self.x -= 1
            
    def check_state(self):
        if self.direction == "":
            self.state = "stop"
            return
        count = 0
        directions = ["u", "r", "d", "l"]
        dir_id = directions.index(self.direction)
        for i in range(4):
            if i != dir_id and self.turn_allowed[i]:
                count += 1
        if count > 1 or not self.turn_allowed[dir_id]:
            self.state = "stop"
            self.direction = ""
        else:
            self.state = "run"
