import pandas as pd
import os
import numpy as np
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

#Cojemos la ruta del archivo
ruta = os.path.dirname(os.path.abspath(__file__))
#Contruimos la ruta del archivo
ruta_archivo = os.path.join(ruta, 'brazo_Andrea_filtrado_normalizado.csv')
# Cargar el archivo CSV en un DataFrame de pandas
df = pd.read_csv(ruta_archivo, delimiter=',')


#Eventos (contracción - relajación), nos vamos a basar en un umbral de amplitud. 
#Si la amplitud supera un umbral, se considera que el músculo está activado
#Si la amplitud es menor al umbral, se considera que el músculo está relajado
#Calculamos el umbral con la mediana
umbral = df['A1_filtrado'].median()
print('Umbral:', umbral)

# Identificar los cambios significativos en la señal
cambios = (df['A1_filtrado'] > umbral).astype(int).diff().fillna(0)
grupos = cambios.abs().cumsum()

# Agregar la información de los grupos al DataFrame
df['Grupo'] = grupos

# Calcular la duración de cada grupo
duraciones_grupo = df.groupby('Grupo').size()

# Identificar el estado (contraído o relajado) de cada grupo
estados_grupo = df.groupby('Grupo')['A1_filtrado'].mean() > umbral
estados_grupo = estados_grupo.replace({True: 'Contraido', False: 'Relajado'})

# Agregar la información de los estados al DataFrame
df['Estado'] = grupos.map(estados_grupo)

# Mostrar el resultado
print(df.head())

df.to_csv(os.path.join(ruta, 'brazo_Andrea_con_eventos.csv'), index=False)


#Frecuencia (fatiga muscular)
#Frecuencia, número de repeticiones de un fenómeno periódico en una unidad de tiempo.
# Calcular la frecuencia dominante para cada grupo
grupo_contraido = df[df['Estado'] == 'Contraido']
grupo_relajado = df[df['Estado'] == 'Relajado']

frecuencia_dominante_contraido = grupo_contraido['A1_filtrado'].values  # Reemplaza 'A1' con la columna que contiene tus datos de frecuencia
frecuencia_dominante_relajado = grupo_relajado['A1_filtrado'].values  # Reemplaza 'A1' con la columna que contiene tus datos de frecuencia

# Visualizar las distribuciones de frecuencias dominantes para cada grupo
plt.hist(frecuencia_dominante_contraido, alpha=0.5, label='Contraido', color='blue')
plt.hist(frecuencia_dominante_relajado, alpha=0.5, label='Relajado', color='green')
plt.xlabel('Frecuencia Dominante')
plt.ylabel('Frecuencia')
plt.title('Distribución de Frecuencias Dominantes por Grupo')
plt.legend(loc='upper right')
plt.show()


#Patrones de activación muscular
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
plt.title('Media de la señal filtrada para cada grupo y estado')
plt.legend()
plt.grid(True)
plt.show()

''' En la gráfica podemos observar que según avanzan los grupos (y por tanto el tiempo), la media (los puntos) de la señal es más alta, indicando que el músculo está más activado. 
Sin embargo, a su vez, la media de la relajación disminuye, indicando que el músculo se relaja más al estar más cansado.

Además, la desviación típica, que son las barras, cada vez es mayor, indicando que la señal es más variable, lo que indica que el músculo está más fatigado.'''

#Distancia entre picos
# Filtrar por el estado "Contraido" y obtener el valor máximo de "A1_filtrado" para cada grupo
maximos_contraido = df[df['Estado'] == 'Contraido'].groupby('Grupo')['A1_filtrado'].max().reset_index()

# Agregar la columna "Estado" con el valor "Contraido" para cada grupo
maximos_contraido['Estado'] = 'Contraido'

# Mostrar el grupo, el estado y el valor máximo de A1_filtrado para cada grupo y estado
print(maximos_contraido)
'''#calculamos la diferencia de los valores dos a dos
diferencias_contraidos_max = maximos_contraidos.diff().dropna()
diferencias_contraido_min = minimos_contraidos.diff().dropna()
# Crear una lista de los grupos entre los cuales se calculan las diferencias
grupos = list(zip(maximos_contraidos.index[:-1], maximos_contraidos.index[1:]))

# Crear un DataFrame con las diferencias y los pares de grupos
df_diferencias = pd.DataFrame({
    'Grupo1': [gr[0] for gr in grupos],
    'Grupo2': [gr[1] for gr in grupos],
    'Diferencia_max': diferencias_contraidos_max.values,
    'Diferencia_min': diferencias_contraido_min.values
})

# Fusionar los datos de diferencias con el DataFrame original
df = pd.merge(df, df_diferencias, left_index=True, right_index=True)

# Guardar el DataFrame modificado de vuelta al archivo CSV
df.to_csv('tu_archivo.csv', index=False)'''