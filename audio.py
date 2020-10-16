from pydub import AudioSegment
import urllib.request
import shutil

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


def from_url(url):
    with urllib.request.urlopen(url) as response, open("files/download.amr", 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    sound = AudioSegment.from_file("files/download.amr", format="amr")
    fast_sound = speed_change(sound, 1.5)
    fast_sound.export("files/sound.mp3", format="mp3")



