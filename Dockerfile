FROM python:3.11-slim
RUN apt update && apt install -y ffmpeg
WORKDIR /app
COPY . /app
RUN pip install python-telegram-bot==20.7
CMD ["python", "main.py"]
