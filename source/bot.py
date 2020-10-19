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


@app.route("/files/<path:path>", methods=["GET"])
def get_file(path):
    """Download a file."""
    return send_file(files.pop(path), mimetype="audio/amr")


@app.route('/bot', methods=['POST'])
def bot():
    req = request.values

    num_media = int(req.get('NumMedia', ''))
    incoming_msg = req.get('Body', '')

    resp = MessagingResponse()
    msg = resp.message()
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
            path = f"{recipient}/{hash(sound)}.mp3"
            files[path] = BytesIO()
            audio.speed_change(sound, 1.5).export(files[path])

            url = f"http://{SERVER_IP}:{SERVER_PORT}/files/{path}"
            send_mms(sender, recipient, url)
            msg.body("Here is your sped up message")
            responded = True

    if not responded:
        msg.body("I can't reply to this type of message, sorry!")

    return str(resp)


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
