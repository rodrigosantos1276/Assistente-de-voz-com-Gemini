from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import whisper
import google.generativeai as genai
from gtts import gTTS
import os
import tempfile
import traceback

app = Flask(__name__)
CORS(app)

whisper_model = None

def get_whisper_model():
    global whisper_model
    if whisper_model is None:
        print("Carregando modelo Whisper...")
        whisper_model = whisper.load_model("small")
        print("Modelo Whisper carregado!")
    return whisper_model

@app.route('/transcribe', methods=['POST'])
def transcribe():
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'Nenhum arquivo de áudio enviado'}), 400

        audio_file = request.files['audio']
        language = request.form.get('language', 'pt')
        gemini_api_key = request.form.get('api_key', '')

        if not gemini_api_key:
            return jsonify({'error': 'Chave de API do Gemini não fornecida'}), 400

        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_audio:
            audio_file.save(tmp_audio.name)
            tmp_audio_path = tmp_audio.name

        try:
            model = get_whisper_model()
            result = model.transcribe(tmp_audio_path, fp16=False, language=language)
            transcription = result["text"].strip()

            genai.configure(api_key=gemini_api_key)
            gemini = genai.GenerativeModel(model_name='gemini-flash-latest')
            response = gemini.generate_content(transcription)
            gemini_response = response.text

            tts = gTTS(text=gemini_response, lang=language, slow=False)
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp_tts:
                tts.save(tmp_tts.name)
                tts_path = tmp_tts.name

            with open(tts_path, 'rb') as f:
                audio_data = f.read()

            import base64
            audio_b64 = base64.b64encode(audio_data).decode('utf-8')

            return jsonify({
                'transcription': transcription,
                'response': gemini_response,
                'audio': audio_b64
            })

        finally:
            if os.path.exists(tmp_audio_path):
                os.unlink(tmp_audio_path)
            if 'tts_path' in locals() and os.path.exists(tts_path):
                os.unlink(tts_path)

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
