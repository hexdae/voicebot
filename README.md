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
SERVER_PORT="<YOUR PORT>"
```

### Deployment
Voice bot can be started with `docker-compose up -d`