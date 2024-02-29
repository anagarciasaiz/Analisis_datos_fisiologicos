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
#El umbral se puede calcular como el 50% de la amplitud máxima
umbral = df['A1_filtrado'].max() * 0.5
print('Umbral:', umbral)

#Creamos una nueva columna para los eventos
df['Evento'] = 'Relajado'
df.loc[df['A1_filtrado'] > umbral, 'Evento'] = 'Contraido'
print(df.head())

#Amplitud señal: nivel de activación muscular
#La amplitud de la señal nos indica el nivel de activación muscular.
amplitud = df['A1_filtrado'].max() - df['A1_filtrado'].min()
print('Amplitud:', amplitud)


#Frecuencia (fatiga muscular)
#La frecuencia de la señal nos indica la fatiga muscular.


#Patrones de activación muscular
#Los patrones de activación muscular nos indican cómo se activa el músculo.


#Distancia entre picos


