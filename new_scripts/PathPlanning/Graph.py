class SimpleGraph(object):
    def __init__(self):
        self.edges = {}

    def neighbors(self, id):
        return self.edges[id]

class GridGraph(object):
    def __init__(self, celulasX, celulasY):
        self.__grade = (celulasX, celulasY)
        self.__occupied = list()
    
    @property
    def grid(self):
        return self.__grade
    
    def occupy(self, cel, obj):
        if self.isInsideGrid(cel):
            self.__occupied.append((cel, obj))
    
    def release(self, cel):
        liberar = self.getOccupier(cel)
        if liberar:
            self.__occupied.remove(liberar)

    def isOccupied(self, cel):
        return self.getOccupier(cel) is not None
    
    def getOccupier(self, cel):
        ocupador = list(filter(lambda x: x[0] == cel, self.__occupied))
        if ocupador:
            return ocupador[0]
        return None
    
    def isInsideGrid(self, cel):
        return cel >= 0 and cel < self.__grade[0]*self.__grade[1]
    
    def whatIsOccupied(self):
        return list(map(lambda x: x[0], self.__occupied))