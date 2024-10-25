FROM python:3.11-alpine AS builder

WORKDIR /transcreve-api

RUN apk add --no-cache git ffmpeg build-base

COPY . .

RUN pip install --no-cache-dir -r requirements.txt --target=/transcreve-api/venv

FROM python:3.11-alpine

WORKDIR /transcreve-api

RUN apk add --no-cache \
    bash \
    dumb-init \
    tzdata \
    ffmpeg \
    flac \
    wget \
    ca-certificates

ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY --from=builder /transcreve-api /transcreve-api

ENV PYTHONPATH=/transcreve-api/venv
ENV PATH=/transcreve-api/venv/bin:$PATH

EXPOSE 5000

ENTRYPOINT ["dumb-init", "--"]

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app", "--workers", "4", "--log-level", "info"]
