import requests
import json
import os

# --- Configurações para o Teste ---
# URL da sua API local
API_URL = "http://127.0.0.1:5000/predict"

# Caminho para a imagem que você quer testar
# ATENÇÃO: SUBSTITUA 'caminhao.png' PELO NOME/CAMINHO DA SUA IMAGEM DE TESTE REAL.
# A imagem deve estar na mesma pasta do 'test_api.py' ou você deve fornecer o caminho completo.
IMAGE_PATH = "caminhao.jpg" # <--- MUDE ISTO!

def test_prediction():
    # Verifica se o arquivo de imagem existe
    if not os.path.exists(IMAGE_PATH):
        print(f"Erro: Imagem não encontrada em '{IMAGE_PATH}'")
        print("Por favor, certifique-se de que o caminho para a imagem está correto.")
        print("A imagem deve estar na mesma pasta do test_api.py ou você deve fornecer o caminho completo.")
        return

    print(f"Enviando imagem '{IMAGE_PATH}' para a API em '{API_URL}'...")
    try:
        # Abre o arquivo de imagem em modo binário para enviar via POST
        with open(IMAGE_PATH, 'rb') as f:
            # 'image/png' ou 'image/jpeg' - Mude o mimetype conforme o tipo da sua imagem
            # O primeiro elemento da tupla é o nome do arquivo que será enviado (o nome pode ser qualquer coisa)
            # O segundo elemento é o conteúdo binário do arquivo
            # O terceiro elemento é o tipo MIME do arquivo
            files = {'file': (os.path.basename(IMAGE_PATH), f.read(), 'image/jpg')} # Mude 'image/png' se for .jpg, etc.
            
            # Envia a requisição POST para a API com o arquivo
            response = requests.post(API_URL, files=files)

        # Verifica o status da resposta da API
        if response.status_code == 200:
            # Se a resposta for bem-sucedida (código 200), parseia o JSON
            result = response.json()
            print("\n--- Predição Recebida com Sucesso ---")
            print(json.dumps(result, indent=4, ensure_ascii=False)) # Imprime o JSON formatado
        else:
            # Se houver um erro, imprime o código de status e a mensagem de erro
            print(f"\nErro na predição: Código de Status {response.status_code}")
            print(f"Mensagem de erro da API: {response.text}")

    except requests.exceptions.ConnectionError:
        print("\nErro de Conexão: Não foi possível conectar à API.")
        print("Certifique-se de que a API (app.py) está rodando e acessível em http://127.0.0.1:5000.")
    except Exception as e:
        print(f"\nOcorreu um erro inesperado durante o teste: {e}")

if __name__ == "__main__":
    test_prediction()