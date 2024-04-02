

class Aestrella:

    def __init__(self, pinicial, pfinal, tablero):

        self.pinicial = pinicial
        self.pactual = pinicial
        self.pfinal = pfinal
        self.tablero = tablero
        self.pfinalVecinosCoords = [vecino.getCoords() for vecino in tablero[pfinal[0]][pfinal[1]].getVecinos()]
        self.camino = []
        self.encontrarCamino()

    def encontrarCamino(self):

        visitados = [{"punto": self.pinicial, "padre": None}]

        pila_explorar = []

        if self.pactual in self.pfinalVecinosCoords:
            self.camino.append(self.pactual)
            return

        while not self.testObjetivo():

            vecinos = self.tablero[self.pactual[0]][self.pactual[1]].getVecinos()

            for vecino in vecinos:

                if vecino.getTipo() == "estante":
                    continue

                if vecino.getCoords() in [visitado["punto"] for visitado in visitados]:
                    continue

                else:

                    heuristica = abs(vecino.getCoords()[0] - self.pfinal[0]) + abs(vecino.getCoords()[1]
                                                                                   - self.pfinal[1])
                    costo = abs(vecino.getCoords()[0] - self.pinicial[0]) + abs(vecino.getCoords()[1]
                                                                                - self.pinicial[1])

                    pila_explorar.append({"posicion": vecino.getCoords(), "vecino": vecino,
                                          "f_eval": heuristica + costo, "padre": self.pactual})

            pila_explorar = sorted(pila_explorar, key=lambda k: k["f_eval"])

            padre = pila_explorar[0]["padre"]

            self.pactual = pila_explorar[0]["vecino"].getCoords()
            pila_explorar.pop(0)

            visitados.append({"punto": self.pactual, "padre": padre})

        self.camino = []

        self.camino.append(visitados[-1]["punto"])
        self.camino.insert(0, visitados[-1]["padre"])

        while self.camino[0] is not None:

            for visitado in visitados:

                if visitado["punto"] == self.camino[0]:
                    self.camino.insert(0, visitado["padre"])
                    break

        self.camino.pop(0)

    def getCamino(self):

        return self.camino

    def getCosto(self):

        return len(self.camino) - 1

    def testObjetivo(self):

        if self.pfinal == [0, 0] and self.pactual == [0, 0]:
            return True

        if self.pactual in self.pfinalVecinosCoords and self.pfinal != [0, 0]:
            return True

        return False
