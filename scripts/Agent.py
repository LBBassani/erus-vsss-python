import math

class Agent:
    def __init__(self):
        self.x = self.y = 0

    def update_position(self, t):
        self.x = t[0]
        self.y = t[1]

    def getx(self):
        return self.x

    def gety(self):
        return self.y

    def getxy(self):
        return int(self.getx()), int(self.gety())

    def distance_to(self, x, y):
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def predicao_adaptativa(self, x, mundo):
        return 4.5 + (x - mundo.FIELD_LEFT) * (3.5 - 4.5) / (mundo.FIELD_RIGHT - mundo.FIELD_LEFT)