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

def extract_fft_components(filtered_fft):
    frequencies = []
    magnitudes = []
    
    for freq, complex_amp in filtered_fft:
        frequencies.append(freq)
        magnitude = np.sqrt(complex_amp.real**2 + complex_amp.imag**2)
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
# t = 60 * sampling_rate  # Número de amostras por intervalo
# res = 1 / sampling_rate  # Intervalo de tempo entre amostras
# fMin = 0.1
# fMax = 50


resultados = VibData(t=5000, res=0.1, fMin=0.1, fMax=15, data=data)

# print(resultados)

frequencias, magnitudes = extract_fft_components(resultados[0][3])

# for i in range(20):
#     print(frequencias[i], "\t", magnitudes[i])

fft_graph(frequencias, magnitudes)