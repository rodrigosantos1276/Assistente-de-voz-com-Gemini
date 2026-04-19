# Assistente de Voz — Whisper + Gemini + gTTS

## Requisitos

- Python 3.9+
- ffmpeg instalado no sistema

## Instalação

```bash
pip install -r requirements.txt
```

### Instalar ffmpeg (necessário para o Whisper):

**Ubuntu/Debian:**
```bash
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Baixe em https://ffmpeg.org/download.html e adicione ao PATH.

## Como usar

### 1. Inicie o backend:
```bash
python app.py
```
O servidor sobe em http://localhost:5000

### 2. Abra o frontend:
Abra o arquivo `index.html` diretamente no navegador (duplo clique), ou sirva com:
```bash
python -m http.server 8080
```
E acesse http://localhost:8080

### 3. No navegador:
1. Insira sua **chave de API do Gemini** (obtenha em https://aistudio.google.com)
2. Clique em **Verificar** para confirmar conexão com o backend
3. Escolha o **idioma** e a **duração** da gravação
4. Clique no **microfone** e fale
5. Aguarde a transcrição, resposta e áudio gerados automaticamente

## Arquitetura

```
Navegador (index.html)
    │
    │  POST /transcribe  (audio + api_key + language)
    ▼
Backend Flask (app.py)
    ├── Whisper → transcrição do áudio
    ├── Gemini API → resposta ao texto
    └── gTTS → síntese de voz (MP3)
    │
    │  JSON { transcription, response, audio (base64) }
    ▼
Navegador → exibe resultados e reproduz áudio
```
