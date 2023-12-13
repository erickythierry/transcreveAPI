from flask import Flask, request
import speech_recognition as sr

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return '<center><h1>[POST] /transcrever with "audio" form file (only wav)</h1></center>'

@app.route('/transcrever', methods=['POST'])
def transcrever():
    if 'audio' not in request.files:
        return 'Nenhum arquivo de áudio enviado', 400

    audio_file = request.files['audio']
    if not audio_file:
        return 'Arquivo de áudio inválido', 400
    
    # verifique se o arquivo é um arquivo WAV
    if audio_file.content_type not in ['audio/wav', 'audio/wave', 'audio/x-wav']:
        return {'erro': 'Apenas arquivos WAV são permitidos'}, 400

    # inicializa o reconhecedor de fala
    recognizer = sr.Recognizer()
    
    # abre o arquivo de áudio com o SpeechRecognition
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
    
    try:
        # utiliza a função recognize_google para transcrever o áudio em texto
        transcribed_text = recognizer.recognize_google(audio_data, language='pt-BR')
        return transcribed_text, 200
    except sr.UnknownValueError:
        return 'Não foi possível reconhecer o áudio', 400
    except sr.RequestError:
        return 'Erro ao se comunicar com o serviço de reconhecimento de fala', 500

if __name__ == '__main__':
    app.run(debug=True)
