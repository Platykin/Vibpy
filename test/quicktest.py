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

def safe_float_conversion(value):
    try:
        return float(value.replace(',', '.'))
    except ValueError:
        return np.nan

data = pd.read_csv("C:/dev/Vibpy/test/testess.txt", sep='\\s+', encoding= 'utf-16-le',
                    names= ['timestamp', 'acceleration'],  on_bad_lines= 'skip',
                    converters={'timestamp': safe_float_conversion, 'acceleration': safe_float_conversion},
                    decimal= ',')

data.to_csv('teste2.csv', index= None)

print(data)
