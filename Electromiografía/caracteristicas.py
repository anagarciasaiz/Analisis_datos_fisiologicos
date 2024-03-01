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


#Distancia entre picos, DARLE UNA VUELTA ESTÁ RARETE
max_pico_contraido = grupo_contraido['A1_filtrado'].max()
min_pico_contraido = grupo_contraido['A1_filtrado'].min()
distancia_picos_contraido = max_pico_contraido - min_pico_contraido

max_pico_relajado = grupo_relajado['A1_filtrado'].max()
min_pico_relajado = grupo_relajado['A1_filtrado'].min()
distancia_picos_relajado = max_pico_relajado - min_pico_relajado

print('Distancia entre picos (Contraido):', distancia_picos_contraido)
print('Distancia entre picos (Relajado):', distancia_picos_relajado)


