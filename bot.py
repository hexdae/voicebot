from flask import Flask, send_file
from flask import request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import audio
import requests

app = Flask(__name__)
SERVER = "http://9a925d77961e.ngrok.io"


@app.route("/files/<path:path>", methods=["GET"])
def get_file(path):
    """Download a file."""
    return send_file("files/" + path, mimetype="audio/amr")


@app.route('/bot', methods=['POST'])
def bot():
    # add webhook logic here and return a response
    req = request.values

    num_media = int(req.get('NumMedia', ''))
    incoming_msg = req.get('Body', '')

    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    if num_media > 0:
        if req.get('MediaContentType0', '') == "audio/amr":
            addr = req.get('MediaUrl0', '')
            recipient = req.get('From', '')
            audio.from_url(requests.get(addr).url)
            return create_mms(recipient, SERVER + "/files/sound.mp3")

    if responded != True:
        msg.body("I can't reply to this message sorry")

    return str(resp)


def create_mms(recipient, url):

    account_sid = 'AC7cf95694a62b120b52a37adf5c564807'
    auth_token = '26fa3beb80851e7182aa2f99c3c27a87'
    client = Client(account_sid, auth_token)

    mms = client.messages \
        .create(
            body='Here is your sped up message',
            from_="+12195338335",
            to=recipient,
            media_url=[url]
        )
    return mms


if __name__ == '__main__':
    app.run(host='0.0.0.0')
