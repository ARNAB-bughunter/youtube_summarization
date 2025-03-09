FROM python:3.11-slim

RUN apt update && apt upgrade -y


RUN mkdir /api_gateway
WORKDIR /api_gateway
COPY . /api_gateway

RUN pip3 install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]