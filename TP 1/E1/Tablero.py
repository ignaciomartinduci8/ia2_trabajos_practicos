from Casillero import Casillero
import random
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

        self.coordsObj = []

        self.agente = []
        self.camino = []

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

            columna = random.randint(0, self.columnas - 1)
            fila = random.randint(0, self.filas - 1)

            if self.tablero[fila][columna].getTipo() == "pasillo":
                self.agente = [fila, columna]
                break

    def objetivoAleatorio(self):

        self.coordsObj = []

        while True:

            columna = random.randint(0, self.columnas - 1)
            fila = random.randint(0, self.filas - 1)

            if self.tablero[fila][columna].getTipo() == "estante":
                self.coordsObj = [fila, columna]
                break

        print(f"{GREEN}Objetivo generado: {RESET}{self.coordsObj}")

        self.plotearTablero()

    def objetivoManual(self, obj):

        self.coordsObj = []

        for i in range(self.filas):
            for j in range(self.columnas):
                if self.tablero[i][j].getAlias() == obj:
                    self.coordsObj = [i, j]

        if not self.coordsObj:
            print(f"{RED}El alias no existe en el tablero{RESET}")
            self.coordsObj = []
            self.coordsObj_vecinos = []
            self.plotearTablero()

            return

        print(f"{GREEN}Objetivo ingresado:{RESET} {self.coordsObj}")

        self.plotearTablero()

    def recorrer(self):

        if not self.coordsObj:

            print(f"{RED}No se ha ingresado el objetivo{RESET}")
            return

        punto_inicial = self.agente

        print(f"{GREEN}Recorriendo...{RESET}")

        a_estrella = Aestrella(self.agente, self.coordsObj, self.tablero)

        self.camino = a_estrella.getCamino()
        print(f"{GREEN}Camino encontrado. Imprimiendo camino.{RESET}")
        print(f"{GREEN}Camino: {RESET}{self.camino}")

        for punto in self.camino:

            self.agente = punto
            self.plotearTablero()
            time.sleep(1)

        print(f"{GREEN}Recorrido finalizado{RESET}")

    def plotearTablero(self):

        plt.figure(figsize=(9, 15))
        plt.title("Layout", fontsize=20, pad=20)

        plt.gca().set_facecolor("lightyellow")

        plt.gca().invert_yaxis()
        plt.tick_params(axis='x', top=True, labeltop=True, bottom=False, labelbottom=False)

        for i in range(self.filas):
            for j in range(self.columnas):

                if self.agente == [i, j]:
                    plt.plot(j, i, "go", markersize=25)

                elif [i,j] in self.camino:
                        plt.plot(j, i, "ys", markersize=25)
                elif self.tablero[i][j].getTipo() == "pasillo":
                    plt.plot(j, i, "ks", markersize=25)


                else:

                    if self.coordsObj == [i, j]:
                        plt.plot(j, i, "bs", markersize=25)

                    else:
                        plt.plot(j, i, "rs", markersize=25)

                    plt.text(j, i, self.tablero[i][j].getAlias(), fontsize=12, ha="center", va="center")

        plt.show()

