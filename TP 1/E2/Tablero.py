from Casillero import Casillero
import random
import urllib.error
import matplotlib.pyplot as plt
from Aestrella import Aestrella
import time

RED = "\033[1;31m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"


class Tablero:

    def __init__(self):

        self.filas = 21
        self.columnas = 13

        self.coordsObjA = []
        self.coordsObjB = []
        self.vecinosObjA = []
        self.vecinosObjB = []

        self.agenteA = []
        self.agenteB = []
        self.caminoA = []
        self.caminoB = []

        self.tablero = []
        self.generarTablero()
        self.crearAgente()
        self.plotearTablero()

    def generarTablero(self):

        c = 1

        # Algoritmo de generación de tablero

        for i in range(self.filas):
            fila = []
            for j in range(self.columnas):

                if i == 0 or i == 5 or i == 10 or i == 15 or i == 20 or j == 0 or j == 3 or j == 6 or j == 9 or j == 12:
                    fila.append(Casillero("pasillo", None, i, j))

                else:

                    fila.append(Casillero("estante", c, i, j))
                    c += 1

            self.tablero.append(fila)

        # Algoritmo de asignación de vecinos

        for i in range(self.filas):
            for j in range(self.columnas):

                vecinos = []

                if i > 0:
                    vecinos.append(self.tablero[i - 1][j])
                if i < self.filas - 1:
                    vecinos.append(self.tablero[i + 1][j])
                if j > 0:
                    vecinos.append(self.tablero[i][j - 1])
                if j < self.columnas - 1:
                    vecinos.append(self.tablero[i][j + 1])

                self.tablero[i][j].setVecinos(vecinos)

    def crearAgente(self):

        while True:

            #columna = random.randint(0, self.columnas - 1)
            #fila = random.randint(0, self.filas - 1)

            columna = 0
            fila = 10

            if self.tablero[fila][columna].getTipo() == "pasillo":
                self.agenteA = [fila, columna]
                break

        while True:

            columna = 12
            fila = 10

            if self.tablero[fila][columna].getTipo() == "pasillo":
                self.agenteB = [fila, columna]
                break

    def objetivoAleatorio(self):

        self.coordsObjA = []
        self.coordsObjB = []

        while True:

            columna = random.randint(0, self.columnas - 1)
            fila = random.randint(0, self.filas - 1)

            if self.tablero[fila][columna].getTipo() == "estante":
                self.coordsObjA = [fila, columna]

                for vecino in self.tablero[fila][columna].getVecinos():
                    if vecino.getTipo() == "pasillo":
                        self.vecinosObjA.append(vecino.getCoords())

                break

        while True:

            columna = random.randint(0, self.columnas - 1)
            fila = random.randint(0, self.filas - 1)

            if self.tablero[fila][columna].getTipo() == "estante" and self.coordsObjA != [fila, columna]:
                self.coordsObjB = [fila, columna]

                for vecino in self.tablero[fila][columna].getVecinos():
                    if vecino.getTipo() == "pasillo":
                        self.vecinosObjB.append(vecino.getCoords())

                break

        print(f"{GREEN}Objetivos generados: {RESET}{self.coordsObjA} - {self.coordsObjB}")

        self.plotearTablero()

    def objetivoManual(self, objA, objB):

        self.coordsObjA = []
        self.coordsObjB = []

        for i in range(self.filas):
            for j in range(self.columnas):
                if self.tablero[i][j].getAlias() == objA:
                    self.coordsObjA = [i, j]

                    for vecino in self.tablero[i][j].getVecinos():
                        if vecino.getTipo() == "pasillo":
                            self.vecinosObjA.append(vecino.getCoords())

                elif self.tablero[i][j].getAlias() == objB:
                    self.coordsObjB = [i, j]

                    for vecino in self.tablero[i][j].getVecinos():
                        if vecino.getTipo() == "pasillo":
                            self.vecinosObjB.append(vecino.getCoords())

        if not self.coordsObjA or not self.coordsObjB:
            print(f"{RED}Algun punto no exite en el tablero{RESET}")
            self.coordsObjA = []
            self.coordsObjB = []
            self.plotearTablero()

            return

        print(f"{GREEN}Objetivos ingresados:{RESET} {self.coordsObjA} - {self.coordsObjB}")

        self.plotearTablero()

    def recorrer(self):

        if not self.coordsObjA or not self.coordsObjB:

            print(f"{RED}No se han ingresado los objetivos{RESET}")
            return

        punto_inicialA = self.agenteA
        punto_inicialB = self.agenteB

        print(f"{GREEN}Recorriendo...{RESET}")

        a_estrella_A = Aestrella(self.agenteA, self.coordsObjA, self.tablero)
        a_estrella_B = Aestrella(self.agenteB, self.coordsObjB, self.tablero)

        self.caminoA = a_estrella_A.getCamino()
        print(f"{GREEN}Camino encontrado para A. Imprimiendo camino.{RESET}")
        print(f"{GREEN}Camino A: {RESET}{self.caminoA}")

        self.caminoB = a_estrella_B.getCamino()
        print(f"{GREEN}Camino encontrado para B. Imprimiendo camino.{RESET}")
        print(f"{GREEN}Camino B: {RESET}{self.caminoB}")

        self.plotearTablero()

        while self.caminoA or self.caminoB:

            if self.caminoA:

                if self.caminoA[0] == self.agenteB and self.agenteB in self.vecinosObjB:

                    print(f"{RED}Solicitando al agenteB liberar el espacio...{RESET}")

                    for vecino in self.tablero[self.agenteB[0]][self.agenteB[1]].getVecinos():
                        if vecino.getTipo() == "pasillo" and self.agenteA != vecino.getCoords():
                            self.caminoB.append(vecino.getCoords())

                elif self.caminoA[0] == self.agenteB:

                    print(f"{RED}Colisión detectada{RESET}")

                    a_estrella_A = Aestrella(self.agenteA, self.coordsObjA, self.tablero, restricciones=[self.agenteB])
                    self.caminoA = a_estrella_A.getCamino()
                    print(f"{GREEN}Camino reculado para A.{RESET}")
                    print(f"{GREEN}Camino A: {RESET}{self.caminoA}")

                else:

                    self.agenteA = self.caminoA.pop(0)
                    self.plotearTablero()
                    time.sleep(2)

            if self.caminoB:

                if self.caminoB[0] == self.agenteA and self.agenteA in self.vecinosObjA:

                    print(f"{RED}Solicitando al agenteA liberar el espacio...{RESET}")

                    for vecino in self.tablero[self.agenteA[0]][self.agenteA[1]].getVecinos():
                        if vecino.getTipo() == "pasillo" and self.agenteB != vecino.getCoords():
                            self.caminoA.append(vecino.getCoords())

                elif self.caminoB[0] == self.agenteA:

                    self.agenteB = self.agenteB

                else:

                    self.agenteB = self.caminoB.pop(0)
                    self.plotearTablero()
                    time.sleep(2)

        print(f"{GREEN}Recorrido finalizado{RESET}")

    def plotearTablero(self):

        plt.figure(figsize=(9, 15))
        plt.title("Layout", fontsize=20, pad=20)

        plt.gca().set_facecolor("lightyellow")

        plt.gca().invert_yaxis()
        plt.tick_params(axis='x', top=True, labeltop=True, bottom=False, labelbottom=False)

        for i in range(self.filas):
            for j in range(self.columnas):

                if self.agenteA == [i, j]:
                    plt.plot(j, i, "go", markersize=25)

                elif self.agenteB == [i, j]:
                    plt.plot(j, i, "bo", markersize=25)

                elif [i,j] in self.caminoA:
                    plt.plot(j, i, "gs", markersize=25, alpha=0.5)

                elif [i,j] in self.caminoB:
                    plt.plot(j, i, "bs", markersize=25, alpha=0.5)

                elif self.tablero[i][j].getTipo() == "pasillo":
                    plt.plot(j, i, "ks", markersize=25)

                else:

                    if self.coordsObjA == [i, j]:
                        plt.plot(j, i, "gs", markersize=25)

                    elif self.coordsObjB == [i, j]:
                        plt.plot(j, i, "bs", markersize=25)

                    else:
                        plt.plot(j, i, "rs", markersize=25)

                    plt.text(j, i, self.tablero[i][j].getAlias(), fontsize=12, ha="center", va="center")

        plt.show()



