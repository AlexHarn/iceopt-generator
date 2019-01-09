import numpy as np


def find_peaks(bins):
    """
    Finds the bins with highest charge for each DOM.

    Returns
    -------
    Array of shape (5160,) containing the time (middle of bin) of the charge
    peak for each DOM.
    """
    peaks = np.zeros(shape=(5160,))
    for dom_id in range(5160):
        dom_filtered = np.where(60*(bins[:, 0] - 1) + bins[:, 1] - 1 == dom_id,
                                bins[:, 3], np.zeros_like(bins[:, 3]))
        peaks[dom_id] = bins[np.argmax(dom_filtered), 2]

    return peaks
