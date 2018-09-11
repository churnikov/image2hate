"""Sticker hate.

Usage: image2hate.py [--front=EMOJI] [--back=EMOJI] [--width=WIDTH] <impath>

Arguments:
    <impath>              Path to hated image

Options:
  -h --help             Show this screen.
  --version             Show version.
  --front=EMOJI         Set front emoji [default: 😡]
  --back=EMOJI          Set background emoji [default: 🖤]
  --width=WIDTH         Set with of resulting "image" [default: 20]
"""
from docopt import docopt
from PIL import Image
import numpy as np
from scipy.ndimage.filters import median_filter


def fit_image(img: np.ndarray, size: int) -> np.ndarray:
    small_im = img
    filter_sz: int = 1
    while small_im.shape[1] > size:
        small_im = median_filter(small_im, size = (filter_sz, filter_sz)
                                )[::filter_sz, ::filter_sz]
        filter_sz += 1
    return small_im


def load_image(path: str) -> np.ndarray:
    img = Image.open(path)
    gray_img = np.mean(img, axis=2)
    return gray_img


def array2text(array: np.ndarray, front_fill: str, back_fill: str) -> str:
    emoim = ''
    for row in array > np.mean(array):
        line = ''.join([front_fill if val else back_fill for val in row])
        emoim += line + '\n'
    return emoim


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Polina 😡')

    im_path = arguments['<impath>']
    front_emoji = arguments['--front']
    back_emoji = arguments['--back']
    size_shrink = int(arguments['--width'])

    img: np.ndarray = load_image(im_path)

    gray_img = fit_image(img, size_shrink)
    hate = array2text(gray_img, front_emoji, back_emoji)
    print(hate)
