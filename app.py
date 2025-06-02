import os
from flask import Flask, request, jsonify, render_template
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import cv2
import uuid # NOVO: Para gerar IDs únicos
import csv  # NOVO: Para gravar o log de feedback
import datetime # NOVO: Para timestamp

print("--- Script app.py iniciado ---")

app = Flask(__name__)

# --- Configurações do Modelo ---
MODEL_PATH = './models/cifar10_cnn_model_aprimorado.keras'
IMG_SIZE = (32, 32)
CLASS_NAMES = ['airplane', 'automobile', 'bird', 'cat', 'deer',
               'dog', 'frog', 'horse', 'ship', 'truck']

# --- NOVO: Pastas para arquivos temporários e de feedback ---
TEMP_UPLOAD_DIR = './temp_uploads'
FEEDBACK_DATA_DIR = './feedback_data'
FEEDBACK_LOG_FILE = os.path.join(FEEDBACK_DATA_DIR, 'feedback_log.csv')

# Garante que as pastas existam
os.makedirs(TEMP_UPLOAD_DIR, exist_ok=True)
os.makedirs(FEEDBACK_DATA_DIR, exist_ok=True)

# Garante que o arquivo de log CSV tenha cabeçalho se for novo
if not os.path.exists(FEEDBACK_LOG_FILE):
    with open(FEEDBACK_LOG_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'prediction_id', 'predicted_class', 'user_feedback_class', 'image_path'])

# Carregar o modelo
print(f"Carregando o modelo de: {MODEL_PATH}...")
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print("Modelo carregado com sucesso!")
except Exception as e:
    print(f"Erro ao carregar o modelo: {e}")
    model = None
    import sys
    sys.exit(1)

print("--- Modelo carregado com sucesso, registrando rotas ---")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    print("\n--- Requisição /predict recebida ---")
    if model is None:
        return jsonify({"error": "Modelo não carregado. Verifique os logs do servidor."}), 500

    if 'file' not in request.files:
        print("Erro: Nenhum arquivo na requisição 'file'.")
        return jsonify({"error": "Nenhum arquivo enviado. Por favor, envie um arquivo com a chave 'file'."}), 400

    file = request.files['file']
    if file.filename == '':
        print("Erro: Nome de arquivo inválido.")
        return jsonify({"error": "Nome de arquivo inválido."}), 400

    if not file:
        print("Erro: Arquivo vazio (objeto 'file' é None).")
        return jsonify({"error": "Arquivo vazio."}), 400

    print(f"Arquivo recebido: {file.filename}")
    print(f"Content-Type do arquivo: {file.content_type}")
    
    try:
        # Gerar um ID único para esta predição
        prediction_id = str(uuid.uuid4())
        original_filename = file.filename
        file_extension = os.path.splitext(original_filename)[1]
        temp_image_path = os.path.join(TEMP_UPLOAD_DIR, f"{prediction_id}{file_extension}")

        # Salvar a imagem temporariamente
        file.save(temp_image_path)
        print(f"Imagem salva temporariamente em: {temp_image_path}")

        # Re-abrir a imagem do caminho temporário para processamento com Pillow
        # (Isso evita problemas se file.read() já foi chamado uma vez)
        with open(temp_image_path, 'rb') as f:
            img_pil = Image.open(f).convert('RGB')
        
        print("Imagem aberta com Pillow com sucesso!")
        
        img_np = np.array(img_pil)
        img_resized = cv2.resize(img_np, IMG_SIZE, interpolation=cv2.INTER_AREA)
        
        img_normalized = img_resized / 255.0
        
        img_batch = np.expand_dims(img_normalized, axis=0)

        predictions = model.predict(img_batch)
        
        predicted_class_index = np.argmax(predictions[0])
        confidence = float(np.max(predictions[0]))
        
        predicted_class_name = CLASS_NAMES[predicted_class_index]

        response = {
            "prediction_id": prediction_id, # NOVO: Envia o ID da predição
            "prediction": predicted_class_name,
            "confidence": f"{confidence * 100:.2f}%",
            "all_probabilities": {name: f"{prob * 100:.2f}%" for name, prob in zip(CLASS_NAMES, predictions[0])}
        }
        return jsonify(response), 200

    except Exception as e:
        print(f"Erro interno ao processar a imagem no try/except: {str(e)}")
        # Se houver erro, tente remover o arquivo temporário
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)
        return jsonify({"error": f"Erro interno ao processar a imagem: {str(e)}"}), 500


# --- NOVA ROTA para receber feedback do usuário ---
@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.get_json() # Espera um JSON com o feedback

    prediction_id = data.get('prediction_id')
    predicted_class = data.get('predicted_class')
    user_feedback_class = data.get('user_feedback_class') # Será a classe correta, se houver
    image_temp_path = os.path.join(TEMP_UPLOAD_DIR, f"{prediction_id}{os.path.splitext(data.get('original_filename', ''))[1]}") # Precisa do filename original para extensão

    print(f"\n--- Feedback Recebido para ID: {prediction_id} ---")
    print(f"Predição Original: {predicted_class}")
    print(f"Feedback do Usuário: {user_feedback_class}")

    if not prediction_id or not predicted_class or not user_feedback_class:
        print("Erro: Dados de feedback incompletos.")
        return jsonify({"status": "error", "message": "Dados de feedback incompletos."}), 400

    # Verifica se a imagem temporária existe
    if os.path.exists(image_temp_path):
        # Move a imagem para a pasta de feedback_data
        final_image_path = os.path.join(FEEDBACK_DATA_DIR, os.path.basename(image_temp_path))
        os.rename(image_temp_path, final_image_path)
        print(f"Imagem movida para: {final_image_path}")

        # Registra o feedback no arquivo CSV
        with open(FEEDBACK_LOG_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.datetime.now().isoformat(),
                prediction_id,
                predicted_class,
                user_feedback_class,
                final_image_path
            ])
        print("Feedback registrado no CSV.")
    else:
        print(f"Aviso: Imagem temporária '{image_temp_path}' não encontrada para o feedback.")
        # Se a imagem não foi encontrada, ainda registramos o feedback textual
        with open(FEEDBACK_LOG_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.datetime.now().isoformat(),
                prediction_id,
                predicted_class,
                user_feedback_class,
                "NOT_FOUND_FOR_FEEDBACK" # Indica que a imagem original não foi salva/encontrada
            ])

    return jsonify({"status": "success", "message": "Feedback registrado com sucesso!"}), 200

if __name__ == '__main__':
    print("--- Chamando app.run() ---")
    app.run(debug=True, host='0.0.0.0', port=5000)