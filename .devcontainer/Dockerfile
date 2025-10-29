FROM python:3.10-slim
RUN apt-get update && apt-get install -y --no-install-recommends build-essential ffmpeg git && rm -rf /var/lib/apt/lists/*
WORKDIR /workspace
COPY . /workspace
CMD [ "bash", "-lc", "python app.py" ]
