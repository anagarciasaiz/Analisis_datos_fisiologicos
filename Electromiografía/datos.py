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

# Cargar el archivo CSV en un DataFrame de pandas
df = pd.read_csv('Andrea_Brazo_excl.csv')

# Aplicar filtro de mediana para el filtrado de ruido
df['emg_filtrado'] = medfilt(df['emg'], kernel_size=3)

# Normalizar los datos utilizando normalización z-score
scaler = StandardScaler()
df['emg_normalizado'] = scaler.fit_transform(df[['emg_filtrado']])

# Guardar los datos filtrados y normalizados en un nuevo archivo CSV
df.to_csv('datos_emg_filtrados_normalizados.csv', index=False)