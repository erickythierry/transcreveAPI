# API de Transcrição de Áudio para Texto

Uma API simples criada com Python Flask e a biblioteca SpeechRecognition para transcrever arquivos de áudio em texto.

**ATENÇÃO: Esse projeto é apenas um "wrapper" que utiliza a lib SpeechRecognition e se comunica com a api pública do Google pra fazer as transcrições gratuitamente.**

## Deploy

### Requisitos para executar localmente

Antes de usar a API, certifique-se de ter instalado as dependências do projeto usando o seguinte comando:

```pip install -r requirements.txt```

**Também instale o FFMPEG!**

abra o `main.py` e descomente esse trecho abaixo no fim do arquivo:
```python
#if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
```

execute no terminal (ou cmd):
```bash
python main.py #para windows
```
ou
```bash
python3 main.py #para linux
```

### Requisitos para executar via Docker
execute o comando abaixo na raiz do projeto para fazer build da imagem Docker:
```bash
docker build -t transcreve-api:latest .
```

Depois, execute esse comando pra iniciar o container:
```bash
docker run -p 5000:5000 transcreve-api:latest
```
Assim o container irá iniciar anexado ao console atual, e ouvirá na porta `5000`

para encerrar o container, use `ctrl+c` no console atual


## Endpoint

A API possui um único endpoint em `/transcrever`, que pode ser usado para enviar arquivos de áudio para transcrição.

Para enviar um arquivo de áudio para transcrição, faça uma solicitação HTTP POST para o endpoint `/transcrever` com o arquivo de áudio como dados do formulário multipart.

Por exemplo, usando o comando `curl` no terminal:

```
curl -X POST -F 'audio=@/path/to/audio.wav' http://localhost:5000/transcrever
```


ou usando NodeJS Axios:
```js
var axios = require('axios');
var FormData = require('form-data');
var fs = require('fs');
var data = new FormData();
data.append('audio', fs.createReadStream('@/path/to/audio.wav'));

var config = {
    method: 'post',
    maxBodyLength: Infinity,
    url: 'http://localhost:5000/transcrever',
    headers: { 
        ...data.getHeaders()
    },
    data : data
};

axios(config)
    .then(function (response) {
        console.log(JSON.stringify(response.data));
    })
    .catch(function (error) {
        console.log(error);
    });
```


Isso enviará um arquivo de áudio `audio.wav` localizado em `/path/to/` para o endpoint `/transcrever` da API. Se o arquivo for um arquivo WAV válido, a API transcreverá o áudio em texto e retornará a transcrição como uma resposta HTTP 200 OK. Se o arquivo enviado não for um arquivo válido, a API retornará um JSON com uma mensagem de erro indicando que apenas arquivos WAV, OGG e MP3 são permitidos.

## Contribuindo

Sinta-se à vontade para copiar ou contribuir com a API criando pull requests.
