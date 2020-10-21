## Voicebot

Voice bot is a chabot designed to handle voice notes on messaging apps.
You can forward a voice note to voicebot and it will respond sending a
sped up version of it, saving precious minutes.

## Development

### Environment
In order to develop Voice bot you will need to provide your own Twilio
credentials (SID and TOKEN). This can be done by placing a `.env` file
in the repo root directory with the following contents:
```bash
TWILIO_SID="<YOUR TWILIO SID>"
TWILIO_TOKEN="<YOUR TWILIO TOKEN>"
SERVER_IP="<YOUR IP ADDRESS>"
SERVER_PORT="8080"
```
You can find your Twilio SID and TOKEN in the [Twilio Console](https://www.twilio.com/console).

### Local setup
After setting up the `.env` file, you can start the chatbot, running at `http://localhost:8080`, with the following command:
```
$> sudo docker-compose up

Building chatbot_bot_1 ... done
...
Starting chatbot_bot_1 ... done
Attaching to chatbot_bot_1
bot_1  |  * Serving Flask app "bot" (lazy loading)
bot_1  |  * Environment: production
bot_1  |    WARNING: This is a development server. Do not use it in a production deployment.
bot_1  |    Use a production WSGI server instead.
bot_1  |  * Debug mode: off
bot_1  |  * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
```

To expose your local server to a public url you can download [ngrok](https://ngrok.com/download) and run it with:
```
$> ngrok http 8080

ngrok by @inconshreveable
(Ctrl+C to quit)

Session Status                online
Session Expires               7 hours, 59 minutes
Version                       2.3.35
Region                        United States (us)
Web Interface                 http://127.0.0.1:4040
Forwarding                    http://<your_unique_id>.ngrok.io -> http://localhost:8080
Forwarding                    https://<your_unique_id>.ngrok.io -> http://localhost:8080


Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

Now you can copy the server's address to the Twilio dashboard.

On the dashboard navigate to
```
All products and services
    -> Programmable messaging
        -> Whatsapp Sanbox Settings
```

and paste your server's public url (`http://<your_unique_id>.ngrok.io/bot`) to the text box.

Now your should see your local server respond to HTTP POST requests any time you send a whastapp message.

### Deployment
Voice bot can be run in the background with `docker-compose up -d`