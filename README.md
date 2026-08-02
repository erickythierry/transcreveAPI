[🇧🇷 Português](Readme.md) · [🇺🇸 English](README.en.md)

# API de Transcrição de Áudio para Texto

API simples em Python/Flask que usa a biblioteca [SpeechRecognition](https://github.com/Uberi/speech_recognition) para transcrever arquivos de áudio em texto.

> **Atenção:** este projeto é apenas um *wrapper*. Ele usa a API pública gratuita de reconhecimento de fala do Google através da lib SpeechRecognition. Não há garantia de disponibilidade, cota ou SLA — não use em produção crítica.

Formatos aceitos: **WAV**, **OGG** e **MP3**. Idioma da transcrição: **pt-BR**.

## Endpoints

| Método | Rota          | Descrição                                          |
| ------ | ------------- | -------------------------------------------------- |
| `GET`  | `/`           | Página de ajuda com o uso do endpoint               |
| `GET`  | `/health`     | Healthcheck (sempre `200 ok`, sem filtro de IP)     |
| `POST` | `/transcrever`| Recebe o áudio em `multipart/form-data` e transcreve |

### `POST /transcrever`

Envie o arquivo no campo de formulário `audio`. O `Content-Type` do arquivo precisa ser um destes:
`audio/wav`, `audio/wave`, `audio/x-wav`, `audio/ogg`, `audio/mp3`, `audio/mpeg`.

**Respostas**

| Status | Corpo                                                | Quando                                    |
| ------ | ---------------------------------------------------- | ----------------------------------------- |
| `200`  | texto puro com a transcrição                          | sucesso                                   |
| `400`  | `Nenhum arquivo de áudio enviado`                     | campo `audio` ausente                     |
| `400`  | `{"erro": "Apenas arquivos WAV, OGG e MP3 são permitidos"}` | tipo de arquivo não suportado      |
| `400`  | `Não foi possível reconhecer o áudio`                 | áudio sem fala reconhecível               |
| `403`  | `Acesso não autorizado`                               | IP fora de `ALLOWED_IPS`                  |
| `500`  | mensagem de erro                                      | falha no serviço do Google ou erro interno |

## Configuração

| Variável      | Padrão              | Descrição                                                                 |
| ------------- | ------------------- | ------------------------------------------------------------------------- |
| `ALLOWED_IPS` | *(vazio)*           | Lista de IPs separados por vírgula com permissão de acesso. Vazio = libera qualquer IP. Lê o header `X-Forwarded-For` antes do IP de origem. |
| `WORKERS`     | `4`                 | Workers do gunicorn (só no Docker)                                        |
| `LOGLEVEL`    | `info`              | Nível de log do gunicorn (só no Docker)                                   |
| `TZ`          | `America/Sao_Paulo` | Fuso horário do container                                                 |

## Executando

### Docker (recomendado)

```bash
docker build -t transcreve-api:latest .
docker run -p 5000:5000 transcreve-api:latest
```

O container sobe anexado ao console atual e escuta na porta `5000`. Para encerrar, use `ctrl+c`.

### Docker Compose

```bash
docker compose up --build
```

Antes, ajuste `ALLOWED_IPS` no `docker-compose.yaml` (ou remova a variável para liberar qualquer IP).

### Local

Requisitos: **Python 3.10+** (testado até 3.12) e **FFmpeg** instalado no sistema.

```bash
# Ubuntu / Debian / Zorin
sudo apt install ffmpeg

python3 -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Rodar em desenvolvimento:

```bash
flask --app main run --host 0.0.0.0 --port 5000
```

Ou com gunicorn, como em produção:

```bash
gunicorn --bind 0.0.0.0:5000 main:app --workers 4
```

> Python 3.13+ não é suportado: o módulo `audioop`, usado por SpeechRecognition e pydub, saiu da biblioteca padrão nessa versão.

## Exemplos de uso

### curl

```bash
curl -X POST -F 'audio=@/caminho/para/audio.wav' http://localhost:5000/transcrever
```

### Node.js (axios)

```js
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

const data = new FormData();
data.append('audio', fs.createReadStream('/caminho/para/audio.wav'));

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

with open('/caminho/para/audio.wav', 'rb') as f:
    r = requests.post(
        'http://localhost:5000/transcrever',
        files={'audio': ('audio.wav', f, 'audio/wav')},
    )

print(r.status_code, r.text)
```

## Dependências

```
Flask==3.1.3
SpeechRecognition==3.17.0
Werkzeug==3.1.8
pydub==0.25.1
gunicorn==26.0.0
```

## Contribuindo

Sinta-se à vontade para copiar ou contribuir com a API criando pull requests.
