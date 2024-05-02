import json
import random
import matplotlib.pyplot as plt

class DataGen:

    def __init__(self, year):
        self.year = int(year)
        self.checkExistence()

    def checkExistence(self):
        with open("data/yearData.json", "r") as file:
            data = json.load(file)

        if self.year < 1991 or self.year > 2023:
            print(f"El año {self.year} no es válido.")
            return

        for elemento in data:
            if elemento["year"] == self.year:
                print(f"El año {self.year} ya existe en la base de datos.")
                return

        self.genYear()

    def genYear(self):

        with open("data/bsas_st_temp.txt", "r") as file:
            data = file.readlines()

        data_clean = [[] for i in range(len(data))]

        for i in range(len(data)):
            data[i] = data[i].split()

        idx = (self.year - 1991)*3

        for i in range(len(data)):

            for j in range(len(data[i])):

                if j < idx or j > idx + 2:
                    continue

                else:

                    if i < 2 or i > 9:
                        data_clean[i].append(round(float(data[i][j].replace(',', '.')), 2) + 10)  # exageracion
                    elif 4 < i < 8:
                        data_clean[i].append(round(float(data[i][j].replace(',', '.')), 2) - 10)  # exageracion

                    else:
                        data_clean[i].append(round(float(data[i][j].replace(',', '.')), 2))

        data_hourly = [None for _ in range(12*30*24)]

        for i in range(12):
            for j in range(30):

                min_distorted = data_clean[i][2] + random.choice([-6, 6])
                max_distorted = data_clean[i][1] + random.choice([-6, 6])
                mean_distorted = data_clean[i][0] + random.choice([-6, 6])

                for k in range(24):

                    index = i*30*24 + j*24 + k

                    data_hourly[index] = random.uniform(min_distorted, max_distorted)

        data_json = {
            "year": self.year
        }

        for i in range(12*30):
            data_daily = []
            for j in range(24):
                data_daily.append(data_hourly[i*24 + j])

            data_json[f"day_{i+1}"] = data_daily

        with open("data/yearData.json", "r") as file:
            data_actual_json = json.load(file)

        with open("data/yearData.json", "w") as file:
            data_final = data_actual_json.append(data_json)
            json.dump(data_actual_json, file)

        print(f"Año {self.year} generado con éxito.")

        daily_mins = []
        daily_maxs = []
        daily_means = []

        days = []

        for i in range(12*30):
            days.append(i+1)

        for i in range(12):
            for j in range(30):

                daily_sum = 0
                daily_min = 100
                daily_max = -100

                for k in range(24):

                    index = i*30*24 + j*24 + k

                    daily_sum += data_hourly[index]

                    if data_hourly[index] < daily_min:
                        daily_min = data_hourly[index]

                    if data_hourly[index] > daily_max:
                        daily_max = data_hourly[index]

                daily_mins.append(daily_min)
                daily_maxs.append(daily_max)
                daily_means.append(daily_sum / 24)

        daily_mins_smooth = daily_mins[::20]
        daily_maxs_smooth = daily_maxs[::20]
        daily_means_smooth = daily_means[::20]
        days_smooth = days[::20]

        print(len(daily_mins_smooth))

        plt.plot(days_smooth, daily_mins_smooth, label="Mínimas")
        plt.plot(days_smooth, daily_maxs_smooth, label="Máximas")
        plt.plot(days_smooth, daily_means_smooth, label="Promedios")
        plt.legend()
        plt.grid()
        plt.xlabel("Días")
        plt.ylabel("Temperatura")
        plt.title(f"Temperaturas del año {self.year}")
        plt.show()



