from flask import Flask, send_file
from flask import request
from io import BytesIO
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import audio
import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__) + "/../", '.env')
load_dotenv(dotenv_path)

TWILIO_SID = os.environ.get("TWILIO_SID")
TWILIO_TOKEN = os.environ.get("TWILIO_TOKEN")
SERVER_IP = os.environ.get("SERVER_IP")
SERVER_PORT = os.environ.get("SERVER_PORT")

app = Flask(__name__)
files = {}


@app.route("/files/audio/<path:path>", methods=["GET"])
def get_audio_file(path):
    """Download a file."""
    _, extension = os.path.splitext(path)
    print(extension)
    return send_file(files.pop(path), mimetype=f"audio/mp4")


@app.route('/bot', methods=['POST'])
def bot():
    req = request.values

    num_media = int(req.get('NumMedia', ''))
    incoming_msg = req.get('Body', '')

    response = MessagingResponse()
    responded = False

    if num_media > 0:
        media_type = req.get('MediaContentType0', '')
        media_content = media_type.split('/')[0]
        media_format = media_type.split('/')[1]

        if media_content == "audio":
            addr = req.get('MediaUrl0', '')
            sender = req.get('To', '')
            recipient = req.get('From', '')
            sound = audio.from_url(requests.get(addr).url, media_format)

            sound_format = "mp4"
            path = f"{recipient}/{hash(sound)}.{sound_format}"
            files[path] = BytesIO()
            sound = audio.speed_change(sound, 1.5)
            sound.export(files[path], sound_format)

            msg = response.message("Here is your sped up message")
            msg.media(f"http://{SERVER_IP}:{SERVER_PORT}/files/audio/{path}")
            responded = True

    if not responded:
        msg = response.message("Sorry, I cannot respond to this type of message")

    return str(response)


def send_mms(sender, recipient, media_url):
    client = Client(TWILIO_SID, TWILIO_TOKEN)
    return client.messages.create(
        body='',
        from_=sender,
        to=recipient,
        media_url=[media_url]
    )


if __name__ == '__main__':
    app.run(host=('0.0.0.0'), port=SERVER_PORT)
