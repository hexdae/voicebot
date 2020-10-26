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
        phase = (phase + np.angle(s2 / (s1 + 0.00001))) % (2 * np.pi)
        a2_rephased = np.fft.ifft(np.abs(s2) * np.exp(1j * phase))

        i2 = int(i / factor)
        result[i2: i2 + window_size] += hanning_window * a2_rephased.real

    # normalize (16bit)
    result = ((2**(16-3)) * result / result.max())

    return result.astype('int16')


def speed_change(sound, speed=1.0):
    """ Modify the speed of an AudioSegment without changing the pitch """
    raw = np.array(sound.get_array_of_samples(), dtype = np.int16)
    stretched = stretch(raw, speed, 2**10, 2**8)
    return sound._spawn(stretched)


def save(sound, path):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    if os.path.exists(path):
        os.remove(path)
    fmt = path.split('.')[-1]
    sound.export(path, fmt)