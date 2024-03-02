import pandas as pd
import os
import matplotlib.pyplot as plt

'''
MUSCULAR
- eventos (contraccion-relajacion)
- amplitud señal: nivel activación muscular
- frecuencia (fatiga muscular)
- patrones activación muscular
- distancia entre picos

Falta hacer función y ver que de lo de arriba #Me canse
'''

#Eventos (contracción - relajación), nos vamos a basar en un umbral de amplitud. 
#Si la amplitud supera un umbral, se considera que el músculo está activado
#Si la amplitud es menor al umbral, se considera que el músculo está relajado
#Calculamos el umbral con la mediana

def eventos(df, nombre):
    umbral = df['A1_filtrado'].median()

    # Identificar los cambios significativos en la señal
    cambios = (df['A1_filtrado'] > umbral).astype(int).diff().fillna(0)
    grupos = cambios.abs().cumsum()

    # Agregar la información de los grupos al DataFrame
    df['Grupo'] = grupos

    # Calcular la duración de cada grupo
    duraciones_grupo = df.groupby('Grupo').size()
    print(nombre + ' Duraciones de grupo')
    print(duraciones_grupo)
    
    # Identificar el estado (contraído o relajado) de cada grupo
    estados_grupo = df.groupby('Grupo')['A1_filtrado'].mean() > umbral
    estados_grupo = estados_grupo.replace({True: 'Contraido', False: 'Relajado'})

    # Agregar la información de los estados al DataFrame
    df['Estado'] = grupos.map(estados_grupo)

    # Guardar el DataFrame con la información de los eventos
    df.to_csv(os.path.join(ruta, nombre + '_eventos.csv'), index=False)
    
    return df



#Frecuencia (fatiga muscular)
def frecuencia(df, nombre):
    #Frecuencia, número de repeticiones de un fenómeno periódico en una unidad de tiempo.
    # Calcular la frecuencia dominante para cada grupo
    grupo_contraido = df[df['Estado'] == 'Contraido']
    grupo_relajado = df[df['Estado'] == 'Relajado']

    frecuencia_dominante_contraido = grupo_contraido['A1_filtrado'].values  
    frecuencia_dominante_relajado = grupo_relajado['A1_filtrado'].values  

    # Visualizar las distribuciones de frecuencias dominantes para cada grupo
    plt.hist(frecuencia_dominante_contraido, alpha=0.5, label='Contraido', color='blue')
    plt.hist(frecuencia_dominante_relajado, alpha=0.5, label='Relajado', color='green')
    plt.xlabel('Frecuencia Dominante')
    plt.ylabel('Frecuencia')
    plt.title('Distribución de Frecuencias Dominantes por Grupo ' + nombre)
    plt.legend(loc='upper right')
    plt.show()
    


#Patrones de activación muscular
def patrones_activacion(df, nombre):
    #Los patrones de activación muscular nos indican cómo se activa el músculo.
    # Para ver la activación muscular, voy a calcular estadística simples de cada grupo y estado, contraído y relajado, y las voy a graficar para compararlos
    estadisticas_grupo = df.groupby(['Grupo', 'Estado'])['A1_filtrado'].describe()
    print(estadisticas_grupo)
    plt.figure(figsize=(20, 20))
    
    for estado in df['Estado'].unique():
        datos_estado = estadisticas_grupo.loc[(slice(None), estado), :]
        plt.errorbar(datos_estado.index.get_level_values('Grupo'), datos_estado['mean'], yerr=datos_estado['std'], label=estado, fmt='-o')
        
    plt.xlabel('Grupo')
    plt.ylabel('Media de la señal filtrada')
    plt.title('Media de la señal filtrada para cada grupo y estado ' + nombre)
    plt.legend()
    plt.grid(True)
    plt.show()


#Distancia entre picos
def diferencias_entre_picos(df, nombre):
    # Filtrar por el estado "Contraido" y obtener el valor máximo de "A1_filtrado" para cada grupo
    maximos_contraido = df[df['Estado'] == 'Contraido'].groupby('Grupo')['A1_filtrado'].max().reset_index()
    minimos_contraido = df[df['Estado'] == 'Contraido'].groupby('Grupo')['A1_filtrado'].min().reset_index()
    
    # Filtrar por el estado "Relajado" y obtener el valor mínimo de "A1_filtrado" para cada grupo
    minimos_relajados = df[df['Estado'] == 'Relajado'].groupby('Grupo')['A1_filtrado'].min().reset_index()
    maximos_relajados = df[df['Estado'] == 'Relajado'].groupby('Grupo')['A1_filtrado'].max().reset_index()
    
    # Calcular la diferencia de los valores dos a dos
    diferencias_contraidos_max = maximos_contraido.diff().dropna()  
    diferencias_contraido_min = minimos_contraido.diff().dropna()
    
    diferencias_relajados_max = maximos_relajados.diff().dropna()
    diferencias_relajados_min = minimos_relajados.diff().dropna()
    
    #Añadimos columna indicando los grupos que se comparan
    diferencias_contraidos_max['Grupo1_max'] = maximos_contraido['Grupo'].values[:-1]
    diferencias_contraidos_max['Grupo2_max'] = maximos_contraido['Grupo'].values[1:]
    diferencias_contraido_min['Grupo1_min'] = minimos_contraido['Grupo'].values[:-1]
    diferencias_contraido_min['Grupo2_min'] = minimos_contraido['Grupo'].values[1:]
    
    diferencias_relajados_max['Grupo1_max'] = maximos_relajados['Grupo'].values[:-1]
    diferencias_relajados_max['Grupo2_max'] = maximos_relajados['Grupo'].values[1:]
    diferencias_relajados_min['Grupo1_min'] = minimos_relajados['Grupo'].values[:-1]
    diferencias_relajados_min['Grupo2_min'] = minimos_relajados['Grupo'].values[1:]
    
    #Eliminamos la columna de grupo
    diferencias_contraidos_max = diferencias_contraidos_max.drop(columns='Grupo')
    diferencias_contraido_min = diferencias_contraido_min.drop(columns='Grupo')
    
    diferencias_relajados_max = diferencias_relajados_max.drop(columns='Grupo')
    diferencias_relajados_min = diferencias_relajados_min.drop(columns='Grupo')
    
    #unimos los dataframes de max y min
    diferencias_contraidos = pd.concat([diferencias_contraidos_max, diferencias_contraido_min], axis=1)
    diferencias_relajados = pd.concat([diferencias_relajados_max, diferencias_relajados_min], axis=1)
    
    #extraemos los datos a csv
    diferencias_contraidos.to_csv(os.path.join(ruta, nombre +'_dif_cont.csv'), index=False)
    diferencias_relajados.to_csv(os.path.join(ruta, nombre +'_dif_rel.csv'), index=False)
    
    return diferencias_contraidos, diferencias_relajados

#Cojemos la ruta del archivo
ruta = os.path.dirname(os.path.abspath(__file__))
#Contruimos la ruta del archivo
ruta_archivo_a = os.path.join(ruta, 'brazo_Andrea_filtrado_normalizado.csv')
ruta_archivo_b = os.path.join(ruta, 'brazo_Ana_filtrado_normalizado.csv')
# Cargar el archivo CSV en un DataFrame de pandas
df_andrea = pd.read_csv(ruta_archivo_a, delimiter=',')
df_ana = pd.read_csv(ruta_archivo_b, delimiter=',')

#Eventos (contracción - relajación)
eventos(df_andrea, 'Brazo_Andrea')
eventos(df_ana, 'Brazo_Ana')

#Frecuencia (fatiga muscular)
frecuencia(df_andrea, 'Brazo_Andrea')
frecuencia(df_ana, 'Brazo_Ana')

#Patrones de activación muscular
patrones_activacion(df_andrea, 'Brazo_Andrea')
patrones_activacion(df_ana, 'Brazo_Ana')

''' En la gráfica podemos observar que según avanzan los grupos (y por tanto el tiempo), la media (los puntos) de la señal es más alta, indicando que el músculo está más activado. 
Sin embargo, a su vez, la media de la relajación disminuye, indicando que el músculo se relaja más al estar más cansado.

Además, la desviación típica, que son las barras, cada vez es mayor, indicando que la señal es más variable, lo que indica que el músculo está más fatigado.'''


#Distancia entre picos
diferencias_entre_picos(df_andrea, 'Brazo_Andrea')
diferencias_entre_picos(df_ana, 'Brazo_Ana')
'''
A1_filtrado es la diferencia de los Grupo1 y Grupo2. El max y min de detrás de los grupos es 
para indicar si es la diferencia entre máximos o mínimos.

Contraido y relajado están separados en dos csv
'''
