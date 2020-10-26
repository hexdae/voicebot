from pydub import AudioSegment
import urllib.request
import os
import io
import numpy as np


def from_url(url, fmt):
    """ Create audio segment from url """
    with urllib.request.urlopen(url) as audio_stream:
        audio = io.BytesIO(audio_stream.read())
        return AudioSegment.from_file(audio, format=fmt)


def stretch(snd_array, factor, window_size, h):
    """ Stretches/shortens a sound, by some factor. """
    phase = np.zeros(window_size)
    hanning_window = np.hanning(window_size)
    result = np.zeros(int(len(snd_array) / factor + window_size))

    for i in np.arange(0, len(snd_array) - (window_size + h), h * factor):
        i = int(i)
        # Two potentially overlapping subarrays
        a1 = snd_array[i: i + window_size]
        a2 = snd_array[i + h: i + window_size + h]

        # The spectra of these arrays
        s1 = np.fft.fft(hanning_window * a1)
        s2 = np.fft.fft(hanning_window * a2)

        # Rephase all frequencies and compute the inverse fft
        s1[s1 == 0] = 1e-12;
        phase = (phase + np.angle(s2 / s1)) % (2 * np.pi)
        a2_rephased = np.fft.ifft(np.abs(s2) * np.exp(1j * phase))

        i2 = int(i / factor)
        result[i2: i2 + window_size] += hanning_window * a2_rephased.real

    # normalize (16bit)
    result = ((2**(16-3)) * result / result.max())
    return result.astype(np.int16)


def phase_vocoder(sound, speed=1.0):
    """ Modify the speed of an AudioSegment without changing the pitch """
    samples = np.array(sound.get_array_of_samples(), dtype = np.int16)
    modified_samples = stretch(samples, speed, 2**10, 2**6)
    faster = sound._spawn(modified_samples)
    return faster


def speed_change(sound, speed=1.0):
    """ Modify the speed of an AudioSegment """
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