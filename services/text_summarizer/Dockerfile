FROM python:3.11-slim


# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Set up application environment
RUN mkdir /text_summarizer
WORKDIR /text_summarizer
COPY . /text_summarizer

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Start script
RUN chmod +x start.sh

CMD ["./start.sh"]