[🇧🇷 Português](Readme.md) · [🇺🇸 English](README.en.md)

# Audio-to-Text Transcription API

A small Python/Flask API that uses the [SpeechRecognition](https://github.com/Uberi/speech_recognition) library to transcribe audio files into text.

> **Heads up:** this project is just a *wrapper*. It relies on Google's free public speech recognition API through the SpeechRecognition library. There is no availability, quota or SLA guarantee — don't use it for critical production workloads.

Supported formats: **WAV**, **OGG** and **MP3**. Transcription language: **pt-BR** (Brazilian Portuguese).

## Endpoints

| Method | Route          | Description                                            |
| ------ | -------------- | ------------------------------------------------------ |
| `GET`  | `/`            | Help page describing the endpoint usage                |
| `GET`  | `/health`      | Healthcheck (always `200 ok`, no IP filtering)         |
| `POST` | `/transcrever` | Accepts audio as `multipart/form-data` and transcribes |

### `POST /transcrever`

Send the file in the `audio` form field. The file's `Content-Type` must be one of:
`audio/wav`, `audio/wave`, `audio/x-wav`, `audio/ogg`, `audio/mp3`, `audio/mpeg`.

**Responses**

| Status | Body                                                          | When                                     |
| ------ | ------------------------------------------------------------- | ---------------------------------------- |
| `200`  | plain text with the transcription                             | success                                  |
| `400`  | `Nenhum arquivo de áudio enviado`                             | `audio` field missing                    |
| `400`  | `{"erro": "Apenas arquivos WAV, OGG e MP3 são permitidos"}`   | unsupported file type                    |
| `400`  | `Não foi possível reconhecer o áudio`                         | no recognizable speech in the audio      |
| `403`  | `Acesso não autorizado`                                       | IP not listed in `ALLOWED_IPS`           |
| `500`  | error message                                                 | Google service failure or internal error |

> Response messages are in Portuguese, matching the original API.

## Configuration

| Variable      | Default             | Description                                                                 |
| ------------- | ------------------- | --------------------------------------------------------------------------- |
| `ALLOWED_IPS` | *(empty)*           | Comma-separated list of IPs allowed to call the API. Empty means any IP is allowed. Reads the `X-Forwarded-For` header before the source IP. |
| `WORKERS`     | `4`                 | Number of gunicorn workers (Docker only)                                    |
| `LOGLEVEL`    | `info`              | Gunicorn log level (Docker only)                                            |
| `TZ`          | `America/Sao_Paulo` | Container timezone                                                          |

## Running

### Docker (recommended)

```bash
docker build -t transcreve-api:latest .
docker run -p 5000:5000 transcreve-api:latest
```

The container attaches to the current console and listens on port `5000`. Press `ctrl+c` to stop it.

### Docker Compose

```bash
docker compose up --build
```

Adjust `ALLOWED_IPS` in `docker-compose.yaml` beforehand (or drop the variable to allow any IP).

### Local

Requirements: **Python 3.10+** (tested up to 3.12) and **FFmpeg** installed on the system.

```bash
# Ubuntu / Debian
sudo apt install ffmpeg

python3 -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Run in development:

```bash
flask --app main run --host 0.0.0.0 --port 5000
```

Or with gunicorn, like in production:

```bash
gunicorn --bind 0.0.0.0:5000 main:app --workers 4
```

> Python 3.13+ is not supported: the `audioop` module, used by SpeechRecognition and pydub, was removed from the standard library in that version.

## Usage examples

### curl

```bash
curl -X POST -F 'audio=@/path/to/audio.wav' http://localhost:5000/transcrever
```

### Node.js (axios)

```js
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

const data = new FormData();
data.append('audio', fs.createReadStream('/path/to/audio.wav'));

axios.post('http://localhost:5000/transcrever', data, {
    headers: data.getHeaders(),
    maxBodyLength: Infinity,
})
    .then(res => console.log(res.data))
    .catch(err => console.error(err.message));
```

### Python (requests)

```python
import requests

with open('/path/to/audio.wav', 'rb') as f:
    r = requests.post(
        'http://localhost:5000/transcrever',
        files={'audio': ('audio.wav', f, 'audio/wav')},
    )

print(r.status_code, r.text)
```

## Dependencies

```
Flask==3.1.3
SpeechRecognition==3.17.0
Werkzeug==3.1.8
pydub==0.25.1
gunicorn==26.0.0
```

## Contributing

Feel free to fork the project or contribute by opening pull requests.
