import pandas as pd
import os

#Cojemos la ruta del archivo
ruta = os.path.dirname(os.path.abspath(__file__))
#Contruimos la ruta del archivo
ruta_archivo = os.path.join(ruta, 'brazo_Andrea_filtrado_normalizado.csv')
# Cargar el archivo CSV en un DataFrame de pandas
df = pd.read_csv(ruta_archivo, delimiter=';')

#Eventos (contracción - relajación), nos vamos a basar en un umbral de amplitud. 
#Si la amplitud supera un umbral, se considera que el músculo está activado
#Si la amplitud es menor al umbral, se considera que el músculo está relajado
#El umbral se puede calcular como el 50% de la amplitud máxima
umbral = df['A1'].max() * 0.5
print('Umbral:', umbral)

#Creamos una nueva columna para los eventos
df['Evento'] = 'Relajado'
df.loc[df['A1'] > umbral, 'Evento'] = 'Contraido'
print(df.head())


