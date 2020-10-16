FROM python:3.7
COPY . /app
WORKDIR /app
CMD ["source chatbot-venv/bin/activate && python bot.py"]