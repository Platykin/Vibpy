# encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
# for encoding in encodings:
#     try:
#         with open('C:/dev/Vibpy/test/testess.txt', 'r', encoding=encoding) as file:
#             content = file.read()
#             print(f'Encoding: {encoding}')
#             print(content[:1024])  # Exibir os primeiros 1024 caracteres para inspeção
#             break
#     except UnicodeDecodeError:
#         continue

import pandas as pd
import numpy as np
from scipy.fft import fft
from datetime import datetime
import matplotlib.pyplot as plt

# def safe_float_conversion(value):
#     try:
#         return float(value.replace(',', '.'))
#     except ValueError:
#         return np.nan

# data = pd.read_csv("C:/dev/Vibpy/test/testess.txt", sep='\\s+', encoding= 'utf-16-le',
#                     names= ['timestamp', 'acceleration'],  on_bad_lines= 'skip',
#                     converters={'timestamp': safe_float_conversion, 'acceleration': safe_float_conversion},
#                     decimal= ',')

# data.to_csv('teste2.csv', index= None)

# print(data)

def fft_graph(frequencys, magnitudes):
    plt.figure(figsize=(10, 6))
    plt.plot(frequencys, magnitudes)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.title('FFT of Acceleration Data')
    plt.grid(True)
    plt.show()

def safe_float_conversion(value):
    try:
        return float(value.replace(',', '.'))
    except ValueError:
        return np.nan

def read_data(file_path):
    if file_path.endswith('.csv'):
        data = data = pd.read_csv("C:/dev/Vibpy/test/testess.txt", sep='\\s+', encoding= 'utf-16-le',
                    names= ['timestamp', 'acceleration'],  on_bad_lines= 'skip',
                    converters={'timestamp': safe_float_conversion, 'acceleration': safe_float_conversion},
                    decimal= ',')
    elif file_path.endswith('.xls') or file_path.endswith('.xlsx'):
        data = pd.read_excel(file_path)
        data['acceleration'] = data['acceleration'].astype(float)
    else:
        raise ValueError("Unsupported file format")
    return data

def extract_fft_components(filtered_fft, nyquist_frequencie):
    frequencies = []
    magnitudes = []
    
    for freq, complex_amp in filtered_fft:
        if freq >= 0:
            frequencies.append(freq)
            magnitude = np.sqrt(complex_amp.real**2 + complex_amp.imag**2)
            if freq > 0 and freq < nyquist_frequencie:
                magnitude *= 2
            magnitudes.append(magnitude)
    
    return frequencies, magnitudes

def VibData(t, res, fMin, fMax, data):
    results = []

    num_intervals = len(data) // t
    
    for i in range(num_intervals):
        interval_data = data.iloc[i*t : (i+1)*t].dropna(subset=['acceleration'])
        aMax = interval_data['acceleration'].max()
        vRMS = np.sqrt(np.mean(interval_data['acceleration']**2))
        
        fft_vals = fft(interval_data['acceleration'].to_numpy())
        fft_freqs = np.fft.fftfreq(len(fft_vals), d=res)
        
        filtered_fft = [(freq, amp) for freq, amp in zip(fft_freqs, fft_vals) if fMin <= abs(freq) <= fMax]
        
        date = interval_data['timestamp'].iloc[0]
        results.append((date, aMax, vRMS, filtered_fft))
    
    return results

file_path = 'C:/dev/Vibpy/teste2.csv'
data = read_data(file_path)

# Still to add
# sampling_rate = 800  # Hz
# t = sampling_rate  # Número de amostras por intervalo
# ex: Caso tenhamos uma taxa de amostragem de 1000 Hz, se t = 1000, estaremos analisando 1000 amostras no intervalo de 1 segundo
# Mas poderíamos fazer também t = 500, que seriam 1000 amostras para cada 0,5 segundo
# Ou também t = 2000, que seriam 1000 amostras para cada 2 segundos 

#  ---------------------------------------------------------------------------------------------------------------------------------------------------
# | t Maior -> Melhor resolução de frequência, menor resolução temporal.                                                                              |
# | t Menor -> Melhor resolução temporal, menor resolução de frequência.                                                                              |
# |                                                                                                                                                   |
# | Sinal Estacionário: Se o sinal não muda muito ao longo do tempo, um t maior pode ser usado para obter uma melhor resolução de frequência.         |
# |       Análise de Vibração em Máquinas:                                                                                                            |
# |          Se você está analisando a vibração de uma máquina que opera de forma relativamente estável, você pode escolher um t maior para ter       |
# |        uma resolução de frequência mais precisa.                                                                                                  |
# |                                                                                                                                                   |
# |      Exemplo: t = 2000 para intervalos de 2 segundos (taxa de amostragem = 1000 Hz).                                                              |
# |                                                                                                                                                   |
# | Sinal Não Estacionário: Se o sinal muda rapidamente, um t menor é preferível para capturar essas mudanças com maior resolução temporal.           |
# |       Análise de Sinais Biológicos:                                                                                                               |
# |          Para sinais biológicos, como a atividade cerebral, onde as mudanças podem ser rápidas, um t menor pode ser mais apropriado.              |
# |                                                                                                                                                   |
# |          Exemplo: t = 500 para intervalos de 0,5 segundo (taxa de amostragem = 1000 Hz).                                                          |
#  ---------------------------------------------------------------------------------------------------------------------------------------------------

# res = 1 / sampling_rate  # Intervalo de tempo entre amostras, inverso da taxa de amostragem
# fMin = 0.1
# fMax = 50

sampling_rate = 800
num_samples_per_interval = 2 * sampling_rate
sampling_interval = 1/sampling_rate
nyquist_frequencie = sampling_rate/2



resultados = VibData(t=num_samples_per_interval, res=sampling_interval, fMin=0.1, fMax=15, data=data)

# print(resultados)

frequencias, magnitudes = extract_fft_components(resultados[0][3], nyquist_frequencie)

# for i in range(20):
#     print(frequencias[i], "\t", magnitudes[i])

fft_graph(frequencias, magnitudes)