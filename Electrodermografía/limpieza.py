import pandas as pd
import numpy as np
import os
from scipy.signal import medfilt
from sklearn.preprocessing import StandardScaler

directorio = os.path.dirname(__file__)

def filtrado_y_normal_edg(archivo, nuevonombre):
    """
    Función que recibe un archivo .csv, una columna y un tamaño de ventana para aplicar un filtrado de mediana y una normalización z-score.
    """
    # Cargar el archivo CSV en un DataFrame de pandas
    df_ruta =  os.path.join(os.path.dirname(__file__), archivo)
    df = pd.read_csv(df_ruta, delimiter=';')   

    # Filtrado de ruido de mediana 
    window_size = 3 #Tamaño de la ventana 
    df['A3_filtrado'] = medfilt(df['A3'], kernel_size=window_size)

    # Normalizar los datos utilizando normalización z-score
    scaler = StandardScaler()
    df['A3_normalizado'] = scaler.fit_transform(df[['A3_filtrado']])
    df.to_csv(os.path.join(directorio, nuevonombre), index=False)
    
    return df
filtrado_y_normal_edg('ANDREA_mano_reposo_excel.csv', 'ANDREA_mano_reposo_filtrado.csv')
filtrado_y_normal_edg('ANDREA_mano_postejercicio_excel.csv', 'ANDREA_mano_postejercicio_filtrado.csv')
filtrado_y_normal_edg('ANA_mano_reposo_excel.csv', 'ANA_mano_reposo_filtrado.csv')
filtrado_y_normal_edg('ANA_mano_postejercicio.csv', 'ANA_mano_postejercicio_filtrado.csv')




