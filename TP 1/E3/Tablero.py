from Casillero import Casillero
import random
import matplotlib.pyplot as plt
from Aestrella import Aestrella
import time
import copy
import json
import numpy as np

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
        self.pedido = []

        self.tablero = []
        self.generarTablero()
        self.crearAgente()
        self.regenerarPedido()
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
            fila = 0

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

        self.plotearTablero()
        print(f"{GREEN}Imprimiendo camino (presionar enter para mostrar siguiente){RESET}")
        self.agente = self.camino[-1]
        self.camino = []
        input()
        self.plotearTablero()


        print(f"{GREEN}Recorrido finalizado{RESET}")

    def regenerarPedido(self):

        numero_orden = None
        datos = None

        with open("./data/pedidos.txt", "r") as file:
            datos = file.read()

        allPedidos = []
        pedidos = []

        counter = 0

        for line in datos.split("\n"):

            if "Order" in line:

                counter = 0
                numero_orden = int(line.replace("Order ", ""))
                pedidos = []

            elif counter >= 16:

                allPedidos.append({"orden": numero_orden, "pedidos": pedidos})

            elif "P" in line:

                counter += 1

                pedidos.append(int(line.replace("P", "")))

            elif line == "\n" or line == "" or line == " " or line == " \n":
                allPedidos.append({"orden": numero_orden, "pedidos": pedidos})

        with open("./data/pedidos.json", "w") as file:
            json.dump(allPedidos, file)

    def tomarPedido(self, pedido):

        try:
            pedido = int(pedido)

        except ValueError:
            print(f"{RED}El pedido debe ser un número entero{RESET}")
            return

        with open("./data/pedidos.json", "r") as file:
            datos = json.load(file)

        ok = 0

        for orden in datos:
            if orden["orden"] == pedido:
                ok = 1

        if not ok:
            print(f"{RED}El pedido no existe{RESET}")
            return

        self.pedido = datos[int(pedido) - 1]["pedidos"]

        self.reordenarPedido()

        pass

    def reordenarPedido(self):

        self.coordsObj = []
        self.plotearTablero()

        T0 = 50 # No mejoró por subirla
        Tf = 0.1 # No mejoró por disminuir
        alpha = 0.95 # 0.9 es la mejor relacion costo-tiempo
        T = T0
        L = 50 # 15 es la mejor relación costo-tiempo. Probar L=10 o L=5 da costos mayores, L=20 es muy costoso en tiempo

        costo_actual, caminos = self.costoPlan()

        mejor_orden = copy.deepcopy(self.pedido)
        mejores_caminos = copy.deepcopy(caminos)

        counter = 0

        while Tf <= T:

            for i in range(1, L):

                counter += 1

                random.shuffle(self.pedido)

                costo_nuevo, caminos = self.costoPlan()

                delta = costo_nuevo - costo_actual

                if delta < 0:

                    mejor_orden = copy.deepcopy(self.pedido)
                    mejores_caminos = copy.deepcopy(caminos)
                    costo_actual = costo_nuevo

                elif random.random() <= np.exp(-delta/T):

                    mejor_orden = copy.deepcopy(self.pedido)
                    mejores_caminos = copy.deepcopy(caminos)
                    costo_actual = costo_nuevo

            T = alpha * T

        self.pedido = copy.deepcopy(mejor_orden)

        print(f"=====================================================")
        print(f"{GREEN}Pedido exitosamente optimizado luego de {RESET}{counter}{GREEN} iteraciones.{RESET}")
        print(f"{GREEN}Plan: {RESET}{self.pedido}")
        print(f"{GREEN}Costo del plan: {RESET}{costo_actual}")
        print(f"{GREEN}Imprimiendo caminos...{RESET}")

        for i in range(len(caminos)):

            self.camino = mejores_caminos[i]
            self.plotearTablero()
            input("(Enter)")
            self.agente = self.camino[-1]
            self.camino = []
            self.plotearTablero()

        self.camino = []
        self.plotearTablero()

    def reordenarTablero(self):



        pass

    def calcularFrecuencias(self):

        pass

    def costoPlan(self):

        costo = 0

        actual = self.agente
        objetivo_actual = None

        caminos = []

        for i in range(self.filas):
            for j in range(self.columnas):
                if self.tablero[i][j].getAlias() == self.pedido[0]:
                    objetivo_actual = [i, j]

        a_estrella = Aestrella(actual, objetivo_actual, self.tablero)
        costo += a_estrella.getCosto()
        caminos.append(a_estrella.getCamino())

        for i in range(len(self.pedido)):

            if i == 0:
                continue

            actual = caminos[-1][-1]
            objetivo_actual = None

            for j in range(self.filas):
                for k in range(self.columnas):
                    if self.tablero[j][k].getAlias() == self.pedido[i]:
                        objetivo_actual = [j, k]

            a_estrella = Aestrella(actual, objetivo_actual, self.tablero)
            costo += a_estrella.getCosto()
            caminos.append(a_estrella.getCamino())

        #print(f"{GREEN}--> Plan a evaluar: {RESET}{self.pedido}")
        #print(f"{GREEN}--> Calculo del costo del plan: {RESET}{costo}")

        return [costo, caminos]

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

