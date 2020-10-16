FROM python:3.7
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["source chatbot-venv/bin/activate && python bot.py"]