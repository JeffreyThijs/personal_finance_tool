import numpy as np
import matplotlib.pyplot as plt
import io


def _plot(*args, **kwargs):

    x = kwargs['x'] if 'x' in kwargs else None
    title = kwargs['title'] if 'title' in kwargs else None
    xlabel = kwargs['xlabel'] if 'xlabel' in kwargs else None
    ylabel = kwargs['ylabel'] if 'ylabel' in kwargs else None
    figure_number = kwargs['figure_number'] if 'figure_number' in kwargs else 0
    filetype = kwargs['filetype'] if 'filetype' in kwargs else "png"
    figsize = kwargs['figsize'] if 'figsize' in kwargs else [12.8, 9.6]
    dpi = kwargs['dpi'] if 'dpi' in kwargs else 400

    plt.figure(figure_number, figsize=figsize, dpi=dpi)

    if len(args) == 0:
        raise ValueError("no input")

    for y in args:
        if x is not None:
            plt.plot(x, y)
        else:
            plt.plot(y)

    if title:
        plt.title(title)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)

    bytes_image = io.BytesIO()
    plt.savefig(bytes_image, format=filetype)
    bytes_image.seek(0)

    return bytes_image


def test_plot():

    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    y1 = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    y2 = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    y3 = [4, 8, 12, 16, 20, 16, 12, 8, 4, 0]

    return _plot(y1, y2, y3,
                 x=x,
                 title='test',
                 xlabel='time',
                 ylabel='value',
                 figure_number=0,
                 filetype='png')
