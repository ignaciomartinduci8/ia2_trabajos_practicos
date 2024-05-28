import numpy as np
import matplotlib.pyplot as plt
from keras.datasets import mnist
from sklearn.preprocessing import StandardScaler, MaxAbsScaler, MinMaxScaler
from sklearn import joblib
import os
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# Cargar el dataset MNIST
(X_train, y_train), (X_test, y_test) = mnist.load_data()

# Conocer forma de conjuntos de datos
print("1: Conocer forma de los conjuntos de datos.")
print("Shape del conjunto de ejemplos: "+str(X_train.shape))
print("Shape del conjunto de etiquetas de ejemplo: "+str(y_train.shape))
print("Shape del conjunto de test: "+str(X_test.shape))
print("Shape del conjunto de etiquetas de test: "+str(y_test.shape))

# Mostrar 15 ejemplos aleatorios
r, c = 3, 5
fig = plt.figure(figsize=(2*c, 2*r))
for _r in range(r):
    for _c in range(c):
        ix = np.random.randint(0, len(X_train))
        img = X_train[ix]
        plt.subplot(r, c, _r*c + _c + 1)
        plt.imshow(img, cmap='gray')
        plt.axis("off")
        plt.title(y_train[ix])
plt.tight_layout()
plt.show()

# Aplicar reshape
X_train = X_train.reshape(X_train.shape[0],-1);
X_test = X_test.reshape(X_test.shape[0], -1);
print("2: Aplicar reshape al conjunto de ejemplos y test.")
print("Shape del conjunto de ejemplos: "+str(X_train.shape))
print("Shape del conjunto de etiquetas de ejemplo: "+str(y_train.shape))
print("Shape del conjunto de test: "+str(X_test.shape))
print("Shape del conjunto de etiquetas de test: "+str(y_test.shape))


# NOTA: AL APLICAR UN SCALER ESTE SE ENTRENA. EN EL CASO DE LLEVAR EL CODGIO A
# PRODUCCION ES IMPORTANTE GUARDARLO E IMPORTARLO PARA EVITAR ESTA SOBRECARGA
# ESTE SCALER ES DETERMINISITCO, SIEMPRE QUE NO SE CAMBIEN LOS DATOS DE ENTRADA
# ESTE NO CAMBIARÁ

# CONSULTAR: QUÉ PASA SI UN DATO ESTÁ POR FUERA DEL RANGO ADOPTADO DE LOS SCALERS
# ES DECIR, SI ES MÁS BLANCO O MÁS NEGRO QUE LO QUE SE TUVO EN LO DATOS

# INVESTIGAR SCALERS
# INVESTIGAR ALGORITMOS DE CLASIFICACION MULTICLASE
#

# Teoría de normalización
print("*")
print("*")
print("*")
print("3: Scalers a usar para normalizar. Ver listado en https://scikit-learn.org/stable/modules/classes.html#module-sklearn.preprocessing")
print("- StandardScaler -> Remueve el valor medio (lo establece a cero) y escala para obtener una varianza unitaria")
print("- MaxAbsScaler -> Normaliza con respecto al máximo valor absoluto, establece este en 1.")
print("- MinMaxScaler[arg1, arg2] -> Escala los datos a un valor máximo y mínimo dados por 'arg1' y 'arg2', por defecto son 0 y 1")
print("NOTA: Dado que la generación del scaler es acorde a la totalidad del conjunto de datos, es necesario almacenarlo en la etapa de entrenamiento para usarlo en validación, test y deployment.")

# Aplicación de normalización a conjunto ejemplos y test
scaler_std = StandardScaler()
scaler_maxAbs = MaxAbsScaler()
scaler_minMax = MinMaxScaler()

if os.path.exists("scaler_std.pkl"):
  scaler_Std = joblib.load("scaler_std.pkl")
  X_train_scaled_std = scaler.tr

else:
  X_train_scaled_std = scaler_std.fit_transform(X_train)



X_train_scaled_maxAbs = scaler_maxAbs.fit_transform(X_train)
X_train_scaled_minMax = scaler_minMax.fit_transform(X_train)

X_test_scaled_std = scaler_std.fit_transform(X_test)
X_test_scaled_maxAbs = scaler_maxAbs.fit_transform(X_test)
X_test_scaled_minMax = scaler_minMax.fit_transform(X_test)

X_train_example_index = np.random.randint(0, len(X_train_scaled_std[0]))

print("*")
print("*")
print("*")
print("4: Aplicar la normalización mediante diferentes scalers.")

fig = plt.figure(figsize=(2,2))
plt.title("StandardScaler")
plt.imshow(X_train_scaled_std[X_train_example_index].reshape(28, 28), cmap='gray')
plt.axis('off')
plt.show()

fig = plt.figure(figsize=(2,2))
plt.title("MaxAbsScaler")
plt.imshow(X_train_scaled_maxAbs[X_train_example_index].reshape(28, 28), cmap='gray')
plt.axis('off')
plt.show()

fig = plt.figure(figsize=(2,2))
plt.title("MinMaxScaler")
plt.imshow(X_train_scaled_minMax[X_train_example_index].reshape(28, 28), cmap='gray')
plt.axis('off')
plt.show()

print("*")
print("*")
print("*")
print("*")

# SKLEARN PREPROCESSING -> STANDARD SCALER
# SKLEARN.SVM -> SVC (clasificación) SVR (regresión)
# SKLEARN.METRICS -> ACCUARCY_SCORE

# Entrenar un Support Vector Classifier
svc = SVC(kernel='rbf', C=1.0)
svc.fit(X_train_scaled_std, y_train)

# Realizar predicciones en el conjunto de prueba
y_pred = svc.predict(X_test_scaled_std)

# Calcular la precisión del modelo
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)