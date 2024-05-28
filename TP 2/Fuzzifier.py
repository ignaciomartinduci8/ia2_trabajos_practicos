import matplotlib.pyplot as plt
import time
class Fuzzifier: # PROBAR CAMBIOS ACA MUCHO MUCHO

    def __init__(self):
        self.moduleSatZ = 700
        self.plot()

    def f_hora(self, hora):

        # Noche

        if 0 <= hora <= 6:
            noche = 1

        elif 6 < hora <= 10:
            noche = (10 - hora) / 4

        elif 18 <= hora < 22:
            noche = (hora - 18) / 4

        elif hora >= 22:
            noche = 1

        else:
            noche = 0

        # Dia

        if 6 <= hora <= 10:
            dia = (hora - 6) / 4

        elif 10 < hora < 18:
            dia = 1

        elif 18 <= hora <= 22:
            dia = (22 - hora) / 4

        else:
            dia = 0

        return [noche, dia]

    def f_Tpron(self, Tpron):

        # Frio

        if -20 <= Tpron <= 15:
            frio = 1

        elif 15 <= Tpron <= 30:
            frio = (30 - Tpron) / 15

        else:
            frio = 0

        # Caliente

        if 20 <= Tpron <= 35:
            caliente = (Tpron - 20) / 15

        elif 35 <= Tpron <= 50:
            caliente = 1

        else:
            caliente = 0

        return [frio, caliente]

    def f_Z(self, Z):

        if Z < -self.moduleSatZ:
            Z = -self.moduleSatZ
        elif Z > self.moduleSatZ:
            Z = self.moduleSatZ

        # Negativo

        if Z <= -20:
            negativo = 1

        elif -20 < Z <= 0:
            negativo = (0 - Z) / 20

        else:
            negativo = 0

        # Cero

        if -20 <= Z <= 0:
            cero = (Z + 20) / 20

        elif 0 < Z <= 20:
            cero = (20 - Z) / 20

        else:
            cero = 0

        # Positivo

        if 0 <= Z <= 20:
            positivo = Z / 20

        elif 20 < Z:
            positivo = 1

        else:
            positivo = 0

        return [negativo, cero, positivo]

    def def_ven(self, cerrar, centro, abrir, defusificacion = "MC"):

        porcentaje = [i for i in range(0, 101)]
        var_cerrar = []
        var_centro = []
        var_abrir = []

        for i in porcentaje:

            if i <= 20:
                var_cerrar.append(min(1, cerrar))

            elif 20 <= i <= 50:
                var_cerrar.append(min((20-i)/30, cerrar))

            else:
                var_cerrar.append(0)

            if 40 <= i <= 50:
                var_centro.append(min((i-40)/10, centro))

            elif 50 < i <= 60:
                var_centro.append(min((60-i)/10, centro))

            else:
                var_centro.append(0)

            if 50 <= i <= 80:
                var_abrir.append(min((i-50)/30, abrir))

            elif i > 80:
                var_abrir.append(min(1, abrir))

            else:
                var_abrir.append(0)

        contraer_variables = False

        if contraer_variables:

            var_cerrar = [value**2 for value in var_cerrar]
            var_centro = [value**2 for value in var_centro]
            var_abrir = [value**2 for value in var_abrir]

        #plt.plot(porcentaje, var_cerrar, label="Cerrar")
        #plt.plot(porcentaje, var_centro, label="Centro")
        #plt.plot(porcentaje, var_abrir, label="Abrir")
        #plt.legend()
        #plt.xlabel("Porcentaje")
        #plt.ylabel("Pertenencia")
        #plt.title("Funciones de pertenencia para la variable de control truncadas")
        #plt.grid()
        #plt.show()
        #input()

        var_union = []

        for i in range(0, 101):
            var_union.append(max(var_cerrar[i], var_centro[i], var_abrir[i]))

        #calcular el centroide de la union

        suma = 0

        for valor in var_union:
            suma += valor * var_union.index(valor)

        media_centros = suma / sum(var_union)

        maximo_mayor = 0

        v_0 = var_union[0]

        for valor in var_union:
            if valor >= v_0:
                v_0 = valor
                maximo_mayor = var_union.index(valor)

        if defusificacion == "MC":
            return media_centros
        if defusificacion == "MM":
            return maximo_mayor

    def plot(self):

        noche = []
        dia = []

        for i in range(24):
            noche_act, dia_act = self.f_hora(i)
            noche.append(noche_act)
            dia.append(dia_act)

        plt.plot(range(0, 24), noche, label="Noche")
        plt.plot(range(0, 24), dia, label="Dia")
        plt.legend()
        plt.xlabel("Hora")
        plt.ylabel("Pertenencia")
        plt.title("Funciones de pertenencia para la hora del dia")
        plt.grid()
        plt.show()

        frio = []
        caliente = []

        for i in range(-20, 51):
            frio_act, caliente_act = self.f_Tpron(i)
            frio.append(frio_act)
            caliente.append(caliente_act)

        plt.plot(range(-20, 51), frio, label="Frio")
        plt.plot(range(-20, 51), caliente, label="Caliente")
        plt.legend()
        plt.xlabel("Temperatura pronosticada")
        plt.ylabel("Pertenencia")
        plt.title("Funciones de pertenencia para la temperatura pronosticada")
        plt.grid()
        plt.show()

        negativo, cero, positivo = [], [], []

        for i in range(-self.moduleSatZ, self.moduleSatZ + 1):
            negativo_act, cero_act, positivo_act = self.f_Z(i)
            negativo.append(negativo_act)
            cero.append(cero_act)
            positivo.append(positivo_act)

        plt.plot(range(-self.moduleSatZ, self.moduleSatZ+1), negativo, label="Negativo")
        plt.plot(range(-self.moduleSatZ, self.moduleSatZ+1), cero, label="Cero")
        plt.plot(range(-self.moduleSatZ, self.moduleSatZ+1), positivo, label="Positivo")
        plt.legend()
        plt.xlabel("Z")
        plt.ylabel("Pertenencia")
        plt.title("Funciones de pertenencia para la variable Z")
        plt.grid()
        plt.show()






