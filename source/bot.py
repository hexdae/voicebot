from flask import Flask, send_file
from flask import request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import audio
import requests

app = Flask(__name__)
SERVER = "http://42f3bb7713e8.ngrok.io"


@app.route("/files/<path:path>", methods=["GET"])
def get_file(path):
    """Download a file."""
    file_dir = "/home/pi/Sandbox/Twilio/chatbot/"
    return send_file(f"{file_dir}/files/{path}", mimetype="audio/amr")


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
        media_type = req.get('MediaContentType0', '')
        media_content = media_type.split('/')[0]
        media_format = media_type.split('/')[1]

        if media_content == "audio":
            addr = req.get('MediaUrl0', '')
            sender = req.get('To', '')
            recipient = req.get('From', '')
            file = audio.from_url(requests.get(addr).url, media_content, media_format)
            send_mms(sender, recipient, SERVER + "/" + file)
            msg.body("Here is your sped up message")
            responded = True

    if responded != True:
        msg.body("I can't reply to this type of message, sorry")

    return str(resp)


def send_mms(sender, recipient, url):
    account_sid = 'AC7cf95694a62b120b52a37adf5c564807'
    auth_token = '26fa3beb80851e7182aa2f99c3c27a87'
    client = Client(account_sid, auth_token)
    return client.messages.create(
        body='',
        from_=sender,
        to=recipient,
        media_url=[url]
    )


if __name__ == '__main__':
    app.run()
