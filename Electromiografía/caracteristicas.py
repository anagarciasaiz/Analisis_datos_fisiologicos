import pandas as pd
import os

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

#Creamos una nueva columna para los eventos
df['Evento'] = 'Relajado'
df.loc[df['A1_filtrado'] > umbral, 'Evento'] = 'Contraido'
print(df.head())

#pasamos a csv
df.to_csv(os.path.join(ruta, 'brazo_Andrea_con_eventos.csv'), index=False)

#Amplitud señal: nivel de activación muscular
#La amplitud de la señal nos indica el nivel de activación muscular.

# Calcular la duración de cada estado
eventos = df['Evento'].tolist()
duraciones = []
estado_actual = eventos[0]
duracion_actual = 1

for evento in eventos[1:]:
    if evento == estado_actual:
        duracion_actual += 1
    else:
        duraciones.append((estado_actual, duracion_actual))
        estado_actual = evento
        duracion_actual = 1

duraciones.append((estado_actual, duracion_actual))

print("Duración de cada estado:")
for estado, duracion in duraciones:
    print(f"Estado: {estado}, Duración: {duracion} muestras")

# Calcular la frecuencia de cambios entre estados
cambios = sum(1 for i in range(1, len(eventos)) if eventos[i] != eventos[i-1])
frecuencia_cambios = cambios / len(eventos)
print(f"Frecuencia de cambios entre estados: {frecuencia_cambios}")

#Frecuencia (fatiga muscular)
#La frecuencia de la señal nos indica la fatiga muscular.


#Patrones de activación muscular
#Los patrones de activación muscular nos indican cómo se activa el músculo.


#Distancia entre picos


