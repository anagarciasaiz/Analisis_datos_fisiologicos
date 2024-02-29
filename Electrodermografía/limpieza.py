import pandas as pd
import numpy as np
import os
from scipy.signal import medfilt

# cargamos el csv
ruta = os.path.dirname(os.path.abspath(__file__))
ruta_archivo = os.path.join(ruta, 'ANDREA_mano_reposo_excel.csv')

# Cargar el archivo CSV en un DataFrame de pandas
df_andmanorep = pd.read_csv(ruta_archivo, encoding='utf-8', delimiter=';')

# Filtrado de ruido de mediana 
window_size = 3 #Tamaño de la ventana 
df_andmanorep['A3_filtered'] = medfilt(df_andmanorep['A3'], kernel_size=window_size)

# Normalizar los datos utilizando normalización z-score
col_normalizar = df_andmanorep.columns.difference(['nSeq'])
df_andmanorep[col_normalizar] = (df_andmanorep[col_normalizar] - df_andmanorep[col_normalizar].mean()) / df_andmanorep[col_normalizar].std()

