import pandas as pd
import numpy as np
import os
from scipy.signal import medfilt
from sklearn.preprocessing import StandardScaler
from scipy.signal import find_peaks

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


# Ahora hacemos la extracción de características
def extraccion_caract(archivo, nuevonombre):
    # Cargar el archivo CSV en un DataFrame de pandas
    df_ruta =  os.path.join(os.path.dirname(__file__), archivo)
    df = pd.read_csv(df_ruta, delimiter=',')   
    print(df.head())
    
    # Identificamos los picos
    pico, _ = find_peaks(df['A3_filtrado'], distance=10) 
    # La _ es porque find_peaks devuelve dos valores, pero el segundo es un diccionario que no vamos a usar. Lo metemos en la variable _
    
    # Cálculo de intervalos entre picos
    picos_indices = pico.tolist()
    intervalos = np.diff(picos_indices) 
    
    # Otros parámetros relevantes
    amplitud_picos = df['A3_filtrado'].iloc[pico]
    
    # Dataframe con las cosas extraidas
    print(amplitud_picos)
    df_caract = pd.DataFrame({'amplitud_picos': amplitud_picos})
    
    # Lo guardo en un nuevo csv
    df_caract.to_csv(os.path.join(directorio, nuevonombre), index=False)
    
    return df_caract

extraccion_caract('ANDREA_mano_reposo_filtrado.csv', 'ANDREA_mano_reposo_caract.csv')
extraccion_caract('ANDREA_mano_postejercicio_filtrado.csv', 'ANDREA_mano_postejercicio_caract.csv')
extraccion_caract('ANA_mano_reposo_filtrado.csv', 'ANA_mano_reposo_caract.csv')
extraccion_caract('ANA_mano_postejercicio_filtrado.csv', 'ANA_mano_postejercicio_caract.csv')
