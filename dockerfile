# Usar a imagem oficial do Python 3.11
FROM python:3.11

# Definir o diretório de trabalho
WORKDIR /app

# Copiar o arquivo de requisitos para o contêiner
COPY requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o conteúdo do projeto para o contêiner
COPY . .

# Expor a porta 5000
EXPOSE 5000

# Definir o comando de execução
CMD ["python", "main.py"]
