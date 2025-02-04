import pandas as pd
import numpy as np
from scipy.fft import fft
from datetime import datetime

#transforms .txt into .csv. Watch out for the 

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

def VibData(t, trg, res, fMin, fMax, data):
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

resultados = VibData(t=60, trg=0.5, res=0.01, fMin=0.1, fMax=50, data=data)

converted_fft_df = pd.DataFrame(resultados)
converted_fft_df.to_csv("Resultados_FFT.csv", index=False)

resultado_FFT_csv = pd.read_csv("C:/dev/Vibpy/Resultados_FFT", sep=',', encoding= 'utf-16-le',
                    names= ['date', 'aMax', 'vRMS', 'filtered_fft'],  on_bad_lines= 'skip',
                    converters={'date': safe_float_conversion, 'aMax': safe_float_conversion, 'vRMS': safe_float_conversion, 'filtered_fft': safe_float_conversion},
                    decimal= '.')

print(resultado_FFT_csv)
