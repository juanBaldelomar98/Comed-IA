"""Script that handles the visualization tools of the audio"""
import numpy as np
import io
from scipy.io import wavfile
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from algorithms.laughs.predictor import generate_laugh_predictions

plt.rcParams["figure.figsize"] = [14.90, 3.40]
plt.rcParams["figure.autolayout"] = True


def get_audio(file: str):
    rate, song = wavfile.read(file)
    if len(song.shape)>1:
        song = song[:, 0]

    return song

def get_silences():
    """Provides the intervals of relevant silences"""
    return np.array([])


def loudness_graphic():
    """Shows how loud the audio is"""
    return np.array([])


def generate_graphics(audio_path: str) -> io.BytesIO:
    """Merges all important graphics"""
    song = get_audio(audio_path)
    # laugh_graphic = generate_laugh_predictions(audio_path)
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.plot(song, color="red", alpha=0.3)
    # axis.plot(laugh_graphic[:, 0], laugh_graphic[:, 1], color="green", linewidth=2)
    axis.axes.yaxis.set_ticklabels([])
    axis.axes.xaxis.set_ticklabels([])
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return output
