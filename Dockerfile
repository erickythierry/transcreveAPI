FROM python:3.11
WORKDIR /app
RUN apt update && apt install git flac ffmpeg -y
RUN git clone https://github.com/erickythierry/transcreveAPI .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "main.py"]
