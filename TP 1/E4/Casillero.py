

class Casillero:

    def __init__(self, tipo, c, fila, columna):

        self.tipo = tipo.lower()
        self.alias = c
        self.fila = fila
        self.columna = columna
        self.vecinos = []

    def getAlias(self):
        return self.alias

    def setVecinos(self, vecinos):
        self.vecinos = vecinos

    def getVecinos(self):
        return self.vecinos

    def getCoords(self):
        return [self.fila, self.columna]

    def getTipo(self):
        return self.tipo

    def setAlias(self, alias):
        self.alias = alias

