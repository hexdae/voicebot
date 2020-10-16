FROM python:3.7
COPY . /app
WORKDIR /app
RUN sudo apt-get ffmpeg
CMD ["source chatbot-venv/bin/activate && python bot.py"]