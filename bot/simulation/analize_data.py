import pandas as pd
import matplotlib.pyplot as plt
from sklearn.utils import resample
import pyperclip
from scipy.stats import lognorm
import numpy as np
# Cargar el archivo CSV
data = pd.read_csv('./datasets/heart_disease_health_indicators_BRFSS2015 (1).csv')

# Eliminar columnas innecesarias
columnas_eliminar = ['HeartDiseaseorAttack', 'CholCheck', 'Stroke', 'Fruits', 'Veggies', 'AnyHealthcare', 'NoDocbcCost', 'DiffWalk', 'Education', 'Income']
data = data.drop(columns=columnas_eliminar)
data['Age'] = data['Age'] * 4

# Mostrar los primeros 5 registros
print(data.head())

# Realizar muestreo aleatorio simple
muestra = data.sample(n=1000, replace=False)  # Seleccionar 100 filas al azar
 
print(muestra.describe()) # Mostrar estadísticas de la muestra

#Obtener la probabilidades de cada columna binaria de la muestra
print("Columna HighBP:")
print(muestra['HighBP'].value_counts(normalize=True))
print("Columna HighChol:")
print(muestra['HighChol'].value_counts(normalize=True))
print("Columna Smoker:")
print(muestra['Smoker'].value_counts(normalize=True))
print("Columna Diabetes:")
print(muestra['Diabetes'].value_counts(normalize=True))
print("Columna PhysActivity:")
print(muestra['PhysActivity'].value_counts(normalize=True))
print("Columna HvyAlcoholConsump:")
print(muestra['HvyAlcoholConsump'].value_counts(normalize=True))
print("Columna GenHlth:")
print(muestra['GenHlth'].value_counts(normalize=True))
print("Columna MentHlth:")
print(muestra['Sex'].value_counts(normalize=True))

#HIstograma para BMI, MentHlth, PhysHlth, Age
muestra['BMI'].plot.hist()
plt.show()
muestra['MentHlth'].plot.hist()
plt.show()
muestra['PhysHlth'].plot.hist()
plt.show()
muestra['Age'].plot.hist()
plt.show()

B = 300

# Para almacenar los resultados del bootstrap
bootstrap_samples = {}

# Columnas de interés
columns = ["BMI", "MentHlth", "PhysHlth", "Age"]

pyperclip.copy(muestra['Age'].to_string(index=False))

# Ajusta una distribución log-normal a los datos
shape, loc, scale = lognorm.fit(muestra['BMI'])

# Los parámetros mu y sigma son entonces:
mu = np.log(scale)
sigma = shape

# Estima lambda
lambda_param = 1 / np.mean(muestra['MentHlth'])


# Estima la media y la desviación estándar
mu2 = np.mean(muestra['Age'])
sigma2 = np.std(muestra['Age'])

print("mu: ", mu)
print("sigma: ", sigma)
print("lambda: ", lambda_param)
print("mu: ", mu2)
print("sigma: ", sigma2)
#BMI lognormal distribution

# Bootstrap sampling
#for column in columns:
#    bootstrap_samples[column] = []
#    for i in range(B):
#        bootstrap_sample = resample(data[column], replace=True)
#        bootstrap_samples[column].append(bootstrap_sample)

# Histogramas de los bootstrap samples
#for column in columns:
#    plt.figure()
#    plt.hist(bootstrap_samples[column], bins=30)
#    plt.title(column)
#    plt.show()