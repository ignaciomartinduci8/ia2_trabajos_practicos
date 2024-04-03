import math

from Casillero import Casillero
import random
import matplotlib.pyplot as plt
from Aestrella import Aestrella
import time
import copy
import json
import numpy as np
import math

RED = "\033[1;31m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"


class Tablero:

    def __init__(self):


        self.filas = 21
        self.columnas = 13
        self.orderLimit = 1
        self.pedidoLimit = 16

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

        c = 0

        # Algoritmo de generación de tablero

        for i in range(self.filas):
            fila = []
            for j in range(self.columnas):

                if i == 0 and j == 0:

                    fila.append(Casillero("pasillo", "HOME", i, j))
                    continue

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
        frecuencias = {}

        counter = 0

        for line in datos.split("\n"):

            if "Order" in line and int(line.replace("Order ", "")) > self.orderLimit:
                break

            if "Order" in line:

                counter = 0
                numero_orden = int(line.replace("Order ", ""))
                pedidos = []

            elif line == "\n" or line == "" or line == " " or line == " \n":
                allPedidos.append({"orden": numero_orden, "pedidos": pedidos})

            elif counter >= self.pedidoLimit:
                continue

            elif "P" in line:

                counter += 1

                pedidos.append(int(line.replace("P", "")))

                if int(line.replace("P", "")) in frecuencias:
                    frecuencias[int(line.replace("P", ""))] += 1
                else:
                    frecuencias[int(line.replace("P", ""))] = 1

        frecuencias = {k: v for k, v in sorted(frecuencias.items(), key=lambda item: item[1], reverse=True)}

        with open("./data/pedidos.json", "w") as file:
            json.dump(allPedidos, file)

        with open("./data/frecuencias.json", "w") as file:
            json.dump(frecuencias, file)

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

    def reordenarPedido(self, printMessage=True):

        self.coordsObj = []

        if printMessage:
            self.plotearTablero()

        T0 = 50 # No mejoró por subirla de 50
        Tf = 0.1 # No mejoró por disminuir de 0.1
        alpha = 0.75 # 0.75 es la mejor relacion costo-tiempo
        T = T0
        L = 5 # 10 es la mejor relación costo-tiempo. Probar L=10 o L=5 da costos mayores, L=20 es muy costoso en tiempo

        start_time = time.time()

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

        end_time = time.time()

        if printMessage:

            print(f"=====================================================")
            print(f"{GREEN}Pedido exitosamente optimizado luego de {RESET}{counter}{GREEN} iteraciones.{RESET}")
            print(f"{GREEN}Plan: {RESET}{self.pedido}")
            print(f"{GREEN}Costo del plan: {RESET}{costo_actual}")
            print(f"{GREEN}Tiempo de ejecución: {RESET}{end_time - start_time}")
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

        return costo_actual

    def reordenarTablero(self):

        N = 6
        gens = 29 # +1
        start = time.time()

        genoma = []

        for fila in self.tablero:
            for casillero in fila:

                if casillero.getTipo() == "estante":
                    genoma.append(casillero.getAlias())

        print(f"{GREEN}Genoma original: {RESET}{genoma}")

        genotipos = []

        for i in range(N):

            gen = copy.deepcopy(genoma)
            random.shuffle(gen)
            genotipos.append(gen)

        print(f"{GREEN}Poblacion original generada:{RESET}")

        for gen in genotipos:
            print(gen)

        fitness_vec = self.fitness(genotipos)

        print(f"{GREEN}Fitness de la población original generada:{RESET} {fitness_vec}")

        nuevos_genotipos = [[] for i in range(N)]

        for i in range(gens):

            print(f"{GREEN}Iteración {RESET}{i+1}")

            actual = time.time()

            genotipos = [x for _, x in sorted(zip(fitness_vec, genotipos), key=lambda pair: pair[0])]

            elite_size = math.ceil(0.3333 * N)

            for j in range(elite_size):  # un 33.333% de la población se considera "ELITE"

                nuevos_genotipos[j] = copy.deepcopy(genotipos[j])

            for j in range(0, N-elite_size):

                hijo1, hijo2 = self.PMX(genotipos[j], genotipos[j+1])

                hijo1 = self.intercambio(hijo1)
                hijo2 = self.intercambio(hijo2)
                hijo1 = self.insercion(hijo1)
                hijo2 = self.insercion(hijo2)


                nuevos_genotipos[j+elite_size-1] = hijo1
                nuevos_genotipos[j+elite_size] = hijo2

            genotipos = copy.deepcopy(nuevos_genotipos)

            fitness_vec = self.fitness(genotipos)

            print(f"{GREEN}Fitness de la población generada en la iteración {i}:{RESET} {fitness_vec}")

        print(f"=====================================================")
        print(f"{GREEN}Optimización finalizada{RESET}")
        print(f"{GREEN}Tiempo de ejecución: {RESET}{time.time() - start}")
        print(f"{GREEN}Genotipo final: {RESET}{genotipos[0]}")

        self.reasignarEstantes(genotipos[0])

        self.plotearTablero()

    def PMX(self, padre1, padre2):

        print(f"{GREEN}Padre 1: {RESET}{padre1}")
        print(f"{GREEN}Padre 2: {RESET}{padre2}")

        corte1 = random.randint(0, len(padre1) - 1)
        corte2 = random.randint(corte1, len(padre1) - 1)

        if corte1 == corte2:
            corte2 += 1

        if corte2 < corte1:
            corte1, corte2 = corte2, corte1

        size = len(padre1)

        hijo1 = [None for _ in range(size)]
        hijo2 = [None for _ in range(size)]

        hijo1[corte1:corte2] = padre2[corte1:corte2]
        hijo2[corte1:corte2] = padre1[corte1:corte2]

        padre1_cross = copy.deepcopy(padre1)
        padre2_cross = copy.deepcopy(padre2)
        padre1_cross[corte1:corte2] = padre2[corte1:corte2]
        padre2_cross[corte1:corte2] = padre1[corte1:corte2]

        for i in range(size):

            if i in range(corte1, corte2):
                continue

            if padre1[i] not in hijo1:

                hijo1[i] = padre1[i]

                continue

            val = padre1[i]

            while True:

                idx = hijo1.index(val)

                val = padre2_cross[idx]

                if val in hijo1:
                    continue

                hijo1[i] = val
                break

        for i in range(size):

            if i in range(corte1, corte2):
                continue

            if padre2[i] not in hijo2:

                hijo2[i] = padre2[i]

                continue

            val = padre2[i]

            while True:

                idx = hijo2.index(val)

                val = padre1_cross[idx]

                if val in hijo2:
                    continue

                hijo2[i] = val
                break

        print(f"{GREEN}Hijo 1: {RESET}{hijo1}")
        print(f"{GREEN}Hijo 2: {RESET}{hijo2}")

        return hijo1, hijo2

    def intercambio(self, hijo):

        idx1 = random.randint(0, len(hijo) - 1)
        idx2 = random.randint(0, len(hijo) - 1)

        hijo[idx1], hijo[idx2] = hijo[idx2], hijo[idx1]

        return hijo

    def insercion(self, hijo):

        idx1 = random.randint(0, len(hijo) - 1)
        idx2 = random.randint(0, len(hijo) - 1)

        if idx1 == idx2:
            return hijo

        if idx1 > idx2:
            idx1, idx2 = idx2, idx1

        subsec = hijo[idx1:idx2+1]

        newsec = [subsec[0], subsec[-1], *subsec[1:-1]]

        hijo = [*hijo[:idx1], *newsec, *hijo[idx2+1:]]

        return hijo

    def fitness(self, genotipos):

        fitness_vec = []

        for genotipo in genotipos:

            print(f"{GREEN}--> Evaluando genotipo: {RESET}{genotipo}")

            self.reasignarEstantes(genotipo)

            costo_dist = 0

            with open("./data/pedidos.json", "r") as file:
                datos = json.load(file)

            for orden in datos:

                self.pedido = orden["pedidos"]

                costo_dist += self.reordenarPedido(printMessage=False)

            fitness_vec.append(costo_dist)
            print(f"{GREEN}--> Costo del genotipo: {RESET}{costo_dist}")

        fit_max = max(fitness_vec)
        fit_sum = sum(fitness_vec)

        for i in range(len(fitness_vec)):

            fitness_vec[i] = 1 - (fitness_vec[i] / fit_max)

        return fitness_vec

    def reasignarEstantes(self, genotipo):

        data = copy.deepcopy(genotipo)

        for i in range(self.filas):
            for j in range(self.columnas):
                if self.tablero[i][j].getTipo() == "estante":
                    self.tablero[i][j].setAlias(data.pop(0))

    def costoPlan(self):

        costo = 0

        actual = self.agente
        objetivo_actual = None

        caminos = []

        for i in range(self.filas):
            for j in range(self.columnas):
                if self.tablero[i][j].getAlias() == self.pedido[0]:
                    objetivo_actual = [i, j]

        if not objetivo_actual:
            print(f"{RED}A* - 1 - Error en la asignación de objetivos{RESET}")
            return
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

            if not objetivo_actual:
                print(f"{RED}A* - 2 - Error en la asignación de objetivos{RESET}")
                return
            a_estrella = Aestrella(actual, objetivo_actual, self.tablero)
            costo += a_estrella.getCosto()
            caminos.append(a_estrella.getCamino())

        #print(f"{GREEN}--> Plan a evaluar: {RESET}{self.pedido}")
        #print(f"{GREEN}--> Calculo del costo del plan: {RESET}{costo}")

        actual = caminos[-1][-1]
        objetivo_actual = [0, 0]

        if not objetivo_actual:
            print(f"{RED}A* - 3 - Error en la asignación de objetivos{RESET}")
            return
        a_estrella = Aestrella(actual, objetivo_actual, self.tablero)

        costo += a_estrella.getCosto()
        caminos.append(a_estrella.getCamino())

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

