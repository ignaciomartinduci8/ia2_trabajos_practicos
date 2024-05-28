import copy
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
        self.Ve = 27 # random.randint(-5, 35)  # Temperatura externa
        self.V_media_centros = 27  # Temperatura interna
        self.V_maximo_mayor = 27  # Temperatura interna
        self.Vo = 25  # Temperatura deseada
        self.R = 10000  # Resistencia térmica de la casa PROBAR CAMBIO
        self.Rv_media_centros = 0.05 * self.R  # Resistencia térmica de la ventana, por defecot a medio abrir.
        self.Rv_maximo_mayor = 0.05 * self.R  # Resistencia térmica de la ventana, por defecot a medio abrir.
        self.apertura_media_centros = None
        self.apertura_maximo_mayor = None
        self.historial_apertura_media_centros = []
        self.historial_apertura_maximo_mayor = []
        self.historial_V_media_centros = []
        self.historial_V_maximo_mayor = []
        self.C_media_centros = 24 * 3600 / 5 / (self.R + self.Rv_media_centros)  # Capacidad térmica de la casa
        self.C_maximo_mayor = 24 * 3600 / 5 / (self.R + self.Rv_maximo_mayor)  # Capacidad térmica de la casa
        self.pronostico = []  # Pronóstico de la temperatura
        self.prom = None  # Temperatura promedio del día
        self.Z_media_centros = 0
        self.Z_cal_media_centros = 0
        self.Z_enf_media_centros = 0
        self.Z_maximo_mayor = 0
        self.Z_cal_maximo_mayor = 0
        self.Z_enf_maximo_mayor = 0

        self.D_Hora = None  # Variable difusa de la hora
        self.D_Tpronostico = None  # Variable difusa de la temperatura pronosticada promedio
        self.D_Z_media_centros = None  # Variable difusa de la variable Z
        self.D_Z_cal_media_centros = None  # Variable difusa de la variable Z calentamiento
        self.D_Z_enf_media_centros = None  # Variable difusa de la variable Z enfriamiento

        self.D_Z_maximo_mayor = None  # Variable difusa de la variable Z
        self.D_Z_cal_maximo_mayor = None  # Variable difusa de la variable Z calentamiento
        self.D_Z_enf_maximo_mayor = None  # Variable difusa de la variable Z enfriamiento

        self.D_res_media_centros = None  # Variable difusa de la resistencia térmica de la ventana
        self.D_res_maximo_mayor = None  # Variable difusa de la resistencia térmica de la ventana

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
        self.historial_apertura_media_centros = []
        self.historial_apertura_maximo_mayor = []
        self.historial_V_media_centros = []
        self.historial_V_maximo_mayor = []

        for temp_hora in self.pronostico:

            self.Ve = temp_hora

            self.calculateZs()

            # aca va el fuzzifier motor y defuzzifier

            self.D_Hora = self.fuzzifier.f_hora(counter)
            self.D_Tpronostico = self.fuzzifier.f_Tpron(self.prom)
            self.D_Z_media_centros = self.fuzzifier.f_Z(self.Z_media_centros)
            self.D_Z_enf_media_centros = self.fuzzifier.f_Z(self.Z_enf_media_centros)
            self.D_Z_cal_media_centros = self.fuzzifier.f_Z(self.Z_cal_media_centros)
            self.D_Z_maximo_mayor = self.fuzzifier.f_Z(self.Z_maximo_mayor)
            self.D_Z_enf_maximo_mayor = self.fuzzifier.f_Z(self.Z_enf_maximo_mayor)
            self.D_Z_cal_maximo_mayor = self.fuzzifier.f_Z(self.Z_cal_maximo_mayor)

            self.D_res_media_centros = self.motor.inference(self.D_Hora[0], self.D_Hora[1], self.D_Z_media_centros[0], self.D_Z_media_centros[1], self.D_Z_media_centros[2], self.D_Z_cal_media_centros[0], self.D_Z_cal_media_centros[1], self.D_Z_cal_media_centros[2], self.D_Z_enf_media_centros[0], self.D_Z_enf_media_centros[1], self.D_Z_enf_media_centros[2], self.D_Tpronostico[0], self.D_Tpronostico[1])
            self.D_res_maximo_mayor = self.motor.inference(self.D_Hora[0], self.D_Hora[1], self.D_Z_maximo_mayor[0], self.D_Z_maximo_mayor[1], self.D_Z_maximo_mayor[2], self.D_Z_cal_maximo_mayor[0], self.D_Z_cal_maximo_mayor[1], self.D_Z_cal_maximo_mayor[2], self.D_Z_enf_maximo_mayor[0], self.D_Z_enf_maximo_mayor[1], self.D_Z_enf_maximo_mayor[2], self.D_Tpronostico[0], self.D_Tpronostico[1])

            self.apertura_media_centros = self.fuzzifier.def_ven(self.D_res_media_centros[0], self.D_res_media_centros[1], self.D_res_media_centros[2], "MC")
            self.apertura_maximo_mayor = self.fuzzifier.def_ven(self.D_res_maximo_mayor[0], self.D_res_maximo_mayor[1], self.D_res_maximo_mayor[2], "MM")
            self.historial_apertura_media_centros.append(self.apertura_media_centros)
            self.historial_apertura_maximo_mayor.append(self.apertura_maximo_mayor)

            self.Rv_media_centros = ((100 - self.apertura_media_centros) / 100) * self.R * 0.1 # PROBAR CAMBIO
            self.Rv_maximo_mayor = ((100 - self.apertura_maximo_mayor) / 100) * self.R * 0.1 # PROBAR CAMBIO

            # 5T = 5RC = 24*3600

            self.C_media_centros = 24*3600 / (1 * 5 * (self.R + self.Rv_media_centros))
            self.C_maximo_mayor = 24*3600 / (1 * 5 * (self.R + self.Rv_maximo_mayor))

            self.historial_V_media_centros.append(self.V_media_centros)
            self.historial_V_maximo_mayor.append(self.V_maximo_mayor)

            if 0 <= counter <= 8:

                if self.prom < 21:
                    self.Vo = 50

                elif self.prom > 28:
                    self.Vo = 5

            elif 8 < counter < 20:
                self.Vo = 25

            else:
                self.Vo = 25

            #self.V = self.V + self.Z / (self.C*(self.R+self.Rv)*(self.V-25))

            self.V_media_centros = (self.V_media_centros + (self.Ve - self.V_media_centros) * 3600 /
                                    (self.C_media_centros * (self.Rv_media_centros + self.R)))
            self.V_maximo_mayor = (self.V_maximo_mayor + (self.Ve - self.V_maximo_mayor) * 3600 /
                                   (self.C_maximo_mayor * (self.Rv_maximo_mayor + self.R)))

            self.V_dot_media_centros = (self.Ve - self.V_media_centros) / (self.C_media_centros * (self.Rv_media_centros + self.R))

            self.V_media_centros = self.V_dot_media_centros * 3600 + self.V_media_centros

            print("----------------------------------")
            print(f"> Temperatura interna media_centros: {self.V_media_centros}")
            print(f"> Apertura de la ventana media_centros: {self.apertura_media_centros}")
            print(f"> Temperatura interna maximo_mayor: {self.V_maximo_mayor}")
            print(f"> Apertura de la ventana maximo_mayor: {self.apertura_maximo_mayor}")
            counter += 1

        plt.plot(range(0, 24), self.historial_apertura_media_centros)
        plt.plot(range(0, 24), self.pronostico)
        plt.plot(range(0, 24), [self.Vo] * 24)
        plt.plot(range(0, 24), self.historial_V_media_centros)
        plt.legend(["Apertura de la ventana", "Pronóstico", "Temperatura deseada", "Temperatura interna"])
        plt.xlabel("Hora")
        plt.ylim([-10, 102])
        plt.ylabel("Temperatura y Apertura")
        plt.title(f"Apertura de la ventana para un día de tipo {nom_dia} - MEDIA DE CENTROS")
        plt.grid()
        plt.show()

        plt.plot(range(0, 24), self.historial_apertura_maximo_mayor)
        plt.plot(range(0, 24), self.pronostico)
        plt.plot(range(0, 24), [self.Vo] * 24)
        plt.plot(range(0, 24), self.historial_V_maximo_mayor)
        plt.legend(["Apertura de la ventana", "Pronóstico", "Temperatura deseada", "Temperatura interna"])
        plt.xlabel("Hora")
        plt.ylim([-10, 102])
        plt.ylabel("Temperatura y Apertura")
        plt.title(f"Apertura de la ventana para un día de tipo {nom_dia} - MAXIMO MAYOR")
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

        self.Z_media_centros = (self.V_media_centros - 25) * (self.Ve - self.V_media_centros)
        self.Z_cal_media_centros = (self.V_media_centros - 50) * (self.Ve - self.V_media_centros)
        self.Z_enf_media_centros = (self.V_media_centros - 5) * (self.Ve - self.V_media_centros)

        self.Z_maximo_mayor = (self.V_maximo_mayor - 25) * (self.Ve - self.V_maximo_mayor)
        self.Z_cal_maximo_mayor = (self.V_maximo_mayor - 50) * (self.Ve - self.V_maximo_mayor)
        self.Z_enf_maximo_mayor = (self.V_maximo_mayor - 5) * (self.Ve - self.V_maximo_mayor)

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








