import time

from Fuzzifier import Fuzzifier
from Motor import Motor
import json
import random
import matplotlib.pyplot as plt

class Controller:

    def __init__(self):

        self.fuzzifier = Fuzzifier()
        self.motor = Motor()
        self.horasDia = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        self.horasNoche = [0, 1, 2, 3, 4, 5, 6, 7, 21, 22, 23]
        self.Ve = 25# random.randint(-5,    35)  # Temperatura externa
        self.V = random.randint(-5, 35)  # Temperatura interna
        self.Vo = 25  # Temperatura deseada
        self.R = 10000  # Resistencia térmica de la casa PROBAR CAMBIO
        self.Rv = 0.05 * self.R  # Resistencia térmica de la ventana, por defecot a medio abrir.
        self.apertura = 0.5
        self.historial_apertura = []
        self.historial_V = []
        self.C = 24 * 3600 / 5 / (self.R + self.Rv)  # Capacidad térmica de la casa
        self.pronostico = []  # Pronóstico de la temperatura
        self.prom = None  # Temperatura promedio del día
        self.Z = 0
        self.Z_cal = 0
        self.Z_enf = 0

        self.D_Hora = None  # Variable difusa de la hora
        self.D_Tpronostico = None  # Variable difusa de la temperatura pronosticada promedio
        self.D_Z = None  # Variable difusa de la variable Z
        self.D_Z_cal = None  # Variable difusa de la variable Z calentamiento
        self.D_Z_enf = None  # Variable difusa de la variable Z enfriamiento

        self.D_Rv = None  # Variable difusa de la resistencia térmica de la ventana


        print(f"> Parámetros de control automático: R = {self.R} C = {self.C}")
        print(f"> Constante de tiempo Tao = {self.R * self.C} segundos.")

        pass

    def evaluateCase(self, dia):

        if dia == "frio":
            nom_dia = "frio"
        elif dia == "templado":
            nom_dia = "templado"
        elif dia == "caliente":
            nom_dia = "caliente"
        elif dia == "calienteFrio":
            nom_dia = "calienteNocheFrioDia"
        elif dia == "frioCaliente":
            nom_dia = "frioNocheCalienteDia"
        else:
            print(f"> Error, el día ingresado no es válido.")
            return

        print(f"> Condiciones: {nom_dia}.")

        with open("./data/cases.json", "r") as file:
            data = json.load(file)

        for case in data:

            if case["name"] == nom_dia:
                self.pronostico = case["temps"]
                print(f"> Pronóstico de temperaturas: {self.pronostico}")
                self.getDesiredTemp()

        self.plotTemp(title=f"Pronóstico de temperaturas para un dia de tipo {nom_dia}.")

        counter = 0
        self.historial_apertura = []
        self.historial_V = []

        for temp_hora in self.pronostico:

            self.Ve = temp_hora

            self.calculateZs()

            # aca va el fuzzifier motor y defuzzifier

            self.D_Hora = self.fuzzifier.f_hora(counter)
            self.D_Tpronostico = self.fuzzifier.f_Tpron(self.prom)
            self.D_Z = self.fuzzifier.f_Z(self.Z)
            self.D_Z_enf = self.fuzzifier.f_Z(self.Z_enf)
            self.D_Z_cal = self.fuzzifier.f_Z(self.Z_cal)

            self.D_Rv = self.motor.inference(self.D_Hora[0], self.D_Hora[1], self.D_Z[0], self.D_Z[1], self.D_Z[2], self.D_Z_cal[0], self.D_Z_cal[1], self.D_Z_cal[2], self.D_Z_enf[0], self.D_Z_enf[1], self.D_Z_enf[2], self.D_Tpronostico[0], self.D_Tpronostico[1])

            self.apertura = self.fuzzifier.def_ven(self.D_Rv[0], self.D_Rv[1], self.D_Rv[2])
            self.historial_apertura.append(self.apertura)
            self.Rv = ((100 - self.apertura) / .01) * self.R # PROBAR CAMBIO

            ##

            # 5T = 5RC = 24*3600

            self.C = 24*3600 / (1 * 5 * (self.R + self.Rv))

            self.historial_V.append(self.V)

            if 0 <= counter <= 8:

                if self.prom < 21:
                    self.Vo = 50

                elif self.prom > 28:
                    self.Vo = 5

            elif 8 < counter < 20:
                self.Vo = 25

            else:
                self.Vo = 25

            self.Rv= 0

            #self.V = self.V + self.Z / (self.C*(self.R+self.Rv)*(self.V-25))

            self.V = self.V + (self.Ve - self.V) / (self.C * (self.Rv + self.R))

            print("----------------------------------")
            print(f"> Temperatura interna: {self.V}")
            print(f"> Apertura de la ventana: {self.apertura}")
            #print(f"> Resistencia térmica de la ventana: {self.Rv}")

            counter += 1

        plt.plot(range(0, 24), self.historial_apertura)
        plt.plot(range(0, 24), self.pronostico)
        plt.plot(range(0, 24), [self.Vo] * 24)
        plt.plot(range(0, 24), self.historial_V)
        plt.legend(["Apertura de la ventana", "Pronóstico", "Temperatura deseada", "Temperatura interna"])
        plt.xlabel("Hora")
        plt.ylabel("Temperatura y Apertura")
        plt.title(f"Apertura de la ventana para un día de tipo {nom_dia}")
        plt.grid()
        plt.show()

    def control(self):



        pass

    def getDesiredTemp(self):

            sum = 0
            counter = 0

            for i in range(len(self.pronostico)):

                if i in self.horasDia:
                    counter += 1
                    sum += self.pronostico[i]

            self.prom = sum / counter

            if 21 < self.prom < 27:
                self.Vo = 25
            elif self.prom < 22:
                self.Vo = 50
            else:
                self.Vo = 5

            print(f"> Temperatura promedio 8 - 20 hs: {self.prom}")
            print(f"> Temperatura objetivo del sistema de control: {self.Vo}")

    def calculateZs(self):

        print(self.V, self.Ve)

        self.Z = (self.V - 25) * (self.Ve - self.V)
        self.Z_cal = (self.V - 50) * (self.Ve - self.V)
        self.Z_enf = (self.V - 5) * (self.Ve - self.V)

    def plotTemp(self, title=None):

        plt.plot(range(0, 24),self.pronostico)
        plt.plot(range(0, 24), [self.Vo] * 24)
        plt.plot(range(0, 24), [self.prom] * 24)
        plt.xlabel("Hora")
        plt.ylabel("Temperatura")
        plt.title(f"{title}")
        plt.legend(["Pronóstico", "Temperatura deseada", "Temperatura promedio"])
        plt.grid()
        plt.show()

        pass








