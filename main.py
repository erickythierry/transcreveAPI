from flask import Flask, request
import speech_recognition as sr
from pydub import AudioSegment
import io

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return '<center><h1>[POST] /transcrever with "audio" form file (wav, ogg, mp3)</h1></center>'

@app.route('/transcrever', methods=['POST'])
def transcrever():
    if 'audio' not in request.files:
        return 'Nenhum arquivo de áudio enviado', 400

    audio_file = request.files['audio']
    if not audio_file:
        return 'Arquivo de áudio inválido', 400

    # Verifique o tipo de conteúdo do arquivo de áudio
    content_type = audio_file.content_type
    if content_type not in ['audio/wav', 'audio/wave', 'audio/x-wav', 'audio/ogg', 'audio/mp3']:
        return {'erro': 'Apenas arquivos WAV, OGG e MP3 são permitidos'}, 400

    # Converta o arquivo para WAV se necessário
    if content_type in ['audio/ogg', 'audio/mp3']:
        audio = AudioSegment.from_file(io.BytesIO(audio_file.read()), format=content_type.split('/')[1])
        audio = audio.set_frame_rate(16000).set_channels(1)  # Ajuste a taxa de amostragem e canais conforme necessário
        wav_io = io.BytesIO()
        audio.export(wav_io, format='wav')
        wav_io.seek(0)
        audio_file = wav_io

    # Inicializa o reconhecedor de fala
    recognizer = sr.Recognizer()

    # Abre o arquivo de áudio com o SpeechRecognition
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
    
    try:
        # Utiliza a função recognize_google para transcrever o áudio em texto
        transcribed_text = recognizer.recognize_google(audio_data, language='pt-BR')
        return transcribed_text, 200
    except sr.UnknownValueError:
        return 'Não foi possível reconhecer o áudio', 400
    except sr.RequestError:
        return 'Erro ao se comunicar com o serviço de reconhecimento de fala', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
