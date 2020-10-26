from pydub import AudioSegment
import audio

if __name__ == "__main__":
    # Development audio testing
    sound = AudioSegment.from_file("input/voicenote.m4a", "m4a")
    sound = audio.speed_change(sound, 1.5)
    audio.save(sound, "output/voicenote.mp3")