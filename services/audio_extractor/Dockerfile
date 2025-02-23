FROM python:3.11-slim

RUN apt update && apt upgrade -y
RUN apt install ffmpeg -y

RUN mkdir /audio_extractor
WORKDIR /audio_extractor
COPY . /audio_extractor

RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]