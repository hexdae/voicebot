FROM python:3.7
WORKDIR /app
RUN apt-get update && apt-get install -y ffmpeg

ENV VIRTUAL_ENV=/chatbot-venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN mkdir -p files

# Copy the application
COPY .env .
COPY source source

# Expose the port
EXPOSE 8080

# RUn the application
CMD ["python", "source/bot.py"]