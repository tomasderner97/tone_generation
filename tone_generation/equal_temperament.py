import numpy as np
from functools import reduce

DEFAULT_RATE = 44100
REFERENCE_NUMBER = 0


def parse_tone_name(name):
    tone_names = {
        "c": -9,
        "c#": -8,
        "db": -8,
        "d": -7,
        "d#": -6,
        "eb": -6,
        "e": -5,
        "f": -4,
        "f#": -3,
        "gb": -3,
        "g": -2,
        "g#": -1,
        "ab": -1,
        "a": 0,
        "a#": 1,
        "bb": 1,
        "b": 2,
    }

    tone = tone_names[name[:-1].lower()]
    octave = int(name[-1:])

    return octave - 4 + tone + REFERENCE_NUMBER


def set_default_rate(rate: int):
    global DEFAULT_RATE

    DEFAULT_RATE = rate


def normalize_array(array):
    abs_max = max(abs(np.max(array)), abs(np.min(array)))
    if abs_max == 0:
        return array
    return array / abs_max


def play_array(signal_array, rate):
    import sounddevice

    normalized = normalize_array(signal_array)
    sounddevice.play(normalized, rate, blocking=True)


def play_array_in_notebook(signal_array, rate):
    from IPython.display import Audio

    normalized = normalize_array(signal_array)
    return Audio(normalized, rate=rate, autoplay=True, normalize=False)


def get_time_axis_array(length, rate):
    number_of_values = int(length * rate)
    return np.linspace(0, length, number_of_values, endpoint=False)


class Tone:
    RATIO = 2 ** (1 / 12)

    def __init__(self, number, amplitude=1, reference=440):
        self.number = number
        self.amplitude = amplitude
        self.reference = reference

        self.frequency = self.reference * self.RATIO ** (self.number - REFERENCE_NUMBER)

    def get_relative_tone(self, halfsteps_up):
        return Tone(self.number + halfsteps_up, self.reference)

    def get_signal_axis_array(self, time_array):
        return self.amplitude * np.sin(2 * np.pi * self.frequency * time_array)

    def get_arrays(self, length, rate=DEFAULT_RATE):
        time_array = get_time_axis_array(length, rate)
        signal_array = self.get_signal_axis_array(time_array)

        return time_array, signal_array

    def play(self, length=1, rate=DEFAULT_RATE):
        _, signal = self.get_arrays(length)
        play_array(signal, rate)

    def play_in_notebook(self, length=1, rate=DEFAULT_RATE):
        _, signal = self.get_arrays(length)
        return play_array_in_notebook(signal, rate)


class Chord:

    def __init__(self, *tones):
        if not tones:
            raise ValueError("Chord can not be empty.")

        self.tones = tones

    def get_arrays(self, length, rate=DEFAULT_RATE):
        time_array = get_time_axis_array(length, rate)
        signal_array = reduce(np.add, (tone.get_signal_axis_array(time_array) for tone in self.tones))

        return time_array, signal_array

    def play(self, length=1, rate=DEFAULT_RATE):
        _, signal = self.get_arrays(length, rate)
        play_array(signal, rate)

    def play_in_notebook(self, length=1, rate=DEFAULT_RATE):
        _, signal = self.get_arrays(length, rate)
        return play_array_in_notebook(signal, rate)
