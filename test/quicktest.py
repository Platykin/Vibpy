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


# latin1 encoding
data = pd.read_csv("C:/dev/Vibpy/test/testess.txt", sep='\\s+', encoding= 'utf-16-le', on_bad_lines= 'skip')

data.to_csv('teste.csv', index= None)

print(data)
