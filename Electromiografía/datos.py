'''
MUSCULAR
- eventos (contraccion-relajacion)
- amplitud señal: nivel activación muscular
- frecuencia (fatiga muscular)
- patrones activación muscular
- distancia entre picos
'''
import pandas as pd
from sklearn.preprocessing import StandardScaler
from scipy.signal import medfilt
import os

#obtenemos la ruta del archivo
ruta = os.path.dirname(os.path.abspath(__file__))

#Contruimos la ruta del archivo
ruta_archivo = os.path.join(ruta, 'Andrea_Brazo_excel.csv')

# Cargar el archivo CSV en un DataFrame de pandas
df = pd.read_csv(ruta_archivo, encoding='utf-8', delimiter=';')
print(df.columns)


columnas_eliminar =['A2', 'A3', 'A4', 'A5', 'A6']
df = df.drop(columnas_eliminar)
df.head()
'''
# Aplicar filtro de mediana para el filtrado de ruido
df['emg_filtrado'] = medfilt(df['emg'], kernel_size=3)

# Normalizar los datos utilizando normalización z-score
scaler = StandardScaler()
df['emg_normalizado'] = scaler.fit_transform(df[['emg_filtrado']])

# Guardar los datos filtrados y normalizados en un nuevo archivo CSV
df.to_csv('datos_emg_filtrados_normalizados.csv', index=False)'''