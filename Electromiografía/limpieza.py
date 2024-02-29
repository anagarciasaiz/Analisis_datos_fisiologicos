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


def limpiar_csv(csv, columnas_eliminar):
    

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

def ruido_normalizacion(df, columna, nombre):
    # Aplicar filtro de mediana para el filtrado de ruido
    df[columna + '_filtrado'] = medfilt(df[columna], kernel_size=3)

    # Normalizar los datos utilizando normalización z-score
    scaler = StandardScaler()
    df[columna + '_normalizado'] = scaler.fit_transform(df[[columna + '_filtrado']])
    df.to_csv(os.path.join(ruta, nombre), index=False)
    return df

#obtenemos la ruta del archivo
ruta = os.path.dirname(os.path.abspath(__file__))

# Cargar los datos de los archivos CSV y los limpiamos
df_andrea_brazo = limpiar_csv('Andrea_Brazo_excel.csv', ['A2', 'A3', 'A4', 'A5', 'A6'])
print('ANDREA BRAZO')
print(df_andrea_brazo.head())

df_ana_brazo = limpiar_csv('brazo_Ana_excel.csv', None)
print('ANA BRAZO')
print(df_ana_brazo.head())

# Aplicar filtro de mediana para el filtrado de ruido y normalizamos
df_andrea_brazo = ruido_normalizacion(df_andrea_brazo, 'A1', 'brazo_Andrea_filtrado_normalizado.csv')
print('ANDREA BRAZO FILTRADO Y NORMALIZADO')
print(df_andrea_brazo.head())

df_ana_brazo = ruido_normalizacion(df_ana_brazo, 'A1', 'brazo_Ana_filtrado_normalizado.csv')
print('ANA BRAZO FILTRADO Y NORMALIZADO')
print(df_ana_brazo.head())



