import numpy as np
import matplotlib.pyplot as plt
import io

def _plot(figure_number=0,
          title=None,
          xlabel=None,
          ylabel=None,
          x=None,
          filetype="png",
          *ys):


    plt.figure(figure_number)

    if len(ys) != 0:
        raise ValueError("no input")

    for y in ys:
        if x is not None:
            plt.plot(x, y)
        else:
            plt.plot(y)

    if title: plt.title(title)
    if xlabel: plt.xlabel(xlabel)
    if ylabel: plt.ylabel(ylabel)

    bytes_image = io.BytesIO()
    plt.savefig(bytes_image, format=filetype)
    bytes_image.seek(0)

    return bytes_image
