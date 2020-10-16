FROM python:3.7
WORKDIR /app
RUN apt-get ffmpeg
CMD ["source chatbot-venv/bin/activate && python bot.py"]