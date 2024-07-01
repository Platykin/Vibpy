import re

def extract_text_from_binary(file_path):
    with open(file_path, 'rb') as file:
        binary_data = file.read()
    
    # Tentando encontrar partes textuais (XML) usando expressões regulares
    text_pattern = re.compile(b'<\?xml.*?>.*?</.*?>', re.DOTALL)
    matches = text_pattern.findall(binary_data)
    
    if matches:
        for match in matches:
            try:
                # Decodificar os dados textuais encontrados
                xml_text = match.decode('utf-8')
                print("Extracted XML:")
                print(xml_text)
            except UnicodeDecodeError:
                pass  # Ignorar partes que não puderem ser decodificadas
    
    return matches

# Exemplo de uso com o caminho do arquivo
file_path = r'C:\Users\igo_r\Downloads\Echoenergia-Dia_15-Hora_11-Minuto_27'
extracted_texts = extract_text_from_binary(file_path)