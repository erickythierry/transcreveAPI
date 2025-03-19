# transcreveAPI/main.py
from flask import Flask, request
import speech_recognition as sr
from pydub import AudioSegment
from functools import wraps
import io
import logging
import os
from datetime import datetime

app = Flask(__name__)

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Pegar IPs permitidos da variável de ambiente e remover espaços em branco
raw_ips = os.getenv('ALLOWED_IPS', '').strip()
ALLOWED_IPS = {ip.strip() for ip in raw_ips.split(',') if ip.strip(
)} if raw_ips else None  # None significa "qualquer IP é permitido"

logging.info(f"IPs permitidos: {ALLOWED_IPS if ALLOWED_IPS else 'Todos'}")


def check_ip(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        request_ip = request.headers.get(
            'X-Forwarded-For', request.remote_addr)

        # Se ALLOWED_IPS for None, permite qualquer IP
        if ALLOWED_IPS is not None and request_ip not in ALLOWED_IPS:
            logging.warning(
                f"Tentativa de acesso não autorizada do IP: {request_ip}")
            return 'Acesso não autorizado', 403

        logging.info(f"Acesso autorizado do IP: {request_ip}")
        return f(*args, **kwargs)

    return decorated_function


@app.before_request
def log_request_info():
    logging.info(f"Request IP: {request.remote_addr}")
    logging.info(f"Headers: {dict(request.headers)}")


@app.route('/', methods=['GET'])
@check_ip
def home():
    return '<center><h1>[POST] /transcrever with "audio" form file (wav, ogg, mp3)</h1></center>'


@app.route('/transcrever', methods=['POST'])
@check_ip
def transcrever():
    request_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    request_ip = request.remote_addr

    logging.info(f"Requisição recebida do IP: {request_ip}")

    if 'audio' not in request.files:
        logging.error(
            f"{request_time} - Nenhum arquivo de áudio enviado - IP: {request_ip}")
        return 'Nenhum arquivo de áudio enviado', 400

    audio_file = request.files['audio']
    if not audio_file:
        logging.error(
            f"{request_time} - Arquivo de áudio inválido - IP: {request_ip}")
        return 'Arquivo de áudio inválido', 400

    content_type = audio_file.content_type
    if content_type not in ['audio/wav', 'audio/wave', 'audio/x-wav', 'audio/ogg', 'audio/mp3']:
        logging.error(
            f"{request_time} - Tipo de arquivo não suportado: {content_type} - IP: {request_ip}")
        return {'erro': 'Apenas arquivos WAV, OGG e MP3 são permitidos'}, 400

    try:
        if content_type in ['audio/ogg', 'audio/mp3']:
            audio = AudioSegment.from_file(io.BytesIO(
                audio_file.read()), format=content_type.split('/')[1])
            audio = audio.set_frame_rate(16000).set_channels(
                1)  # Ajuste a taxa de amostragem e canais
            wav_io = io.BytesIO()
            audio.export(wav_io, format='wav')
            wav_io.seek(0)
            audio_file = wav_io

        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)

        transcribed_text = recognizer.recognize_google(
            audio_data, language='pt-BR')

        logging.info(
            f"{request_time} - Transcrição bem-sucedida: {transcribed_text} - IP: {request_ip}")
        return transcribed_text, 200

    except sr.UnknownValueError:
        logging.error(
            f"{request_time} - Não foi possível reconhecer o áudio - IP: {request_ip}")
        return 'Não foi possível reconhecer o áudio', 400
    except sr.RequestError as e:
        logging.error(
            f"{request_time} - Erro ao se comunicar com o serviço de reconhecimento de fala: {e} - IP: {request_ip}")
        return 'Erro ao se comunicar com o serviço de reconhecimento de fala', 500
    except Exception as e:
        logging.error(
            f"{request_time} - Erro inesperado: {e} - IP: {request_ip}")
        return 'Erro interno no servidor', 500
