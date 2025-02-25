FROM python:3.11-slim

RUN apt update && apt upgrade -y
RUN apt install ffmpeg -y

RUN mkdir /speech_to_text
WORKDIR /speech_to_text
COPY . /speech_to_text

RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]