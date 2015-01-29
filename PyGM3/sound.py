__author__ = 'Salvakiya'
import pyglet


class _AudioController:
    Audio = []

    def __init__(self):
        pass


def load(filename):
    # audioID = next(sound.AudioCount)
    _AudioController.Audio.append(pyglet.media.load(filename, streaming=False))
    return len(_AudioController.Audio)-1


def play(name):
    _AudioController.Audio[name].play()


def unload():
    # unload all audio
    for i in range(len(_AudioController.Audio)):
        _AudioController.Audio.pop(0)