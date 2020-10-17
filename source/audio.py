from pydub import AudioSegment
import urllib.request
import os
import io


def from_url(url, fmt):
    with urllib.request.urlopen(url) as audio_stream:
        audio = io.BytesIO(audio_stream.read())
        return AudioSegment.from_file(audio, format=fmt)


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


def save(sound, path):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    if os.path.exists(path):
        os.remove(path)
    fmt = path.split('.')[-1]
    sound.export(path, fmt)




