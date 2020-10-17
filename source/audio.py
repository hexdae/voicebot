from pydub import AudioSegment
import urllib.request
import os
import io

def speed_change(sound, speed=1.0):
    # Manually override the frame_rate. This tells the computer how many
    # samples to play per second
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * speed)
    })
    # convert the sound with altered frame rate to a standard frame rate
    # so that regular playback programs will work right. They often only
    # know how to play audio at standard frame rate (like 44.1k)
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)


def from_url(url, content, fmt):
    file_out = "files/" + content + "." + 'mp3'
    if os.path.exists(file_out):
        os.remove(file_out)
    with urllib.request.urlopen(url) as audio_stream:
        audio = io.BytesIO(audio_stream.read())
        sound = AudioSegment.from_file(audio, format=fmt)
        speed_change(sound, 1.5).export(file_out, format="mp3")
    return file_out

if __name__=="__main__":
    from_url("http://42f3bb7713e8.ngrok.io/files/audio.amr", "audio", "amr")



