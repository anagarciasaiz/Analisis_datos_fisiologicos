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

'''#obtenemos la ruta del archivo
ruta = os.path.dirname(os.path.abspath(__file__))

#Contruimos la ruta del archivo
ruta_archivo = os.path.join(ruta, csv)

# Cargar el archivo CSV en un DataFrame de pandas
df = pd.read_csv(ruta_archivo, encoding='utf-8', delimiter=';')
df.columns = df.columns.str.strip()
print('COLUMNAS-------------')
print(df.columns)

df.columns = ['nSeq', 'I1', 'I2', 'O1', 'O2','A1', 'A2', 'A3', 'A4', 'A5', 'A6']
columnas_eliminar =['A2', 'A3', 'A4', 'A5', 'A6']
df = df.drop(columnas_eliminar, axis = 1)
print(df.head())

# Aplicar filtro de mediana para el filtrado de ruido
df['A1_filtrado'] = medfilt(df['A1'], kernel_size=3)

# Normalizar los datos utilizando normalización z-score
scaler = StandardScaler()
df['A1_normalizado'] = scaler.fit_transform(df[['A1_filtrado']])

# Guardar los datos filtrados y normalizados en un nuevo archivo CSV
df.to_csv('datos_emg_filtrados_normalizados.csv', index=False)'''

def limpiar_csv(csv, columnas_eliminar):
    #obtenemos la ruta del archivo
    ruta = os.path.dirname(os.path.abspath(__file__))

    #Contruimos la ruta del archivo
    ruta_archivo = os.path.join(ruta, csv)

    # Cargar el archivo CSV en un DataFrame de pandas
    df = pd.read_csv(ruta_archivo, encoding='utf-8', delimiter=';')
    df.columns = df.columns.str.strip()
    if columnas_eliminar is not None:
        df = df.drop(columnas_eliminar, axis = 1)
    else:
        pass
    
    return df

df_andrea_brazo = limpiar_csv('Andrea_Brazo_excel.csv', ['A2', 'A3', 'A4', 'A5', 'A6'])
print('ANDREA BRAZO')
print(df_andrea_brazo.head())

df_ana_brazo = limpiar_csv('brazo_Ana_excel.csv', None)
print('ANA BRAZO')
print(df_ana_brazo.head())