import os
import numpy as np
import multiprocessing
import settings
from tqdm import trange
from find_peaks import find_peaks
from log_version import log_version

flasher_dir = settings.RAW_DATA_DIR
data_dir = settings.DATA_DIR


def convert(string, dom):
    """
    Worker function to convert Dima's flasher histograms into charge only data
    for the Gradient Descent Method.

    Parameters
    ----------
    string : Integer
        The id of the string to which the emitter DOM belongs. Integer between
        1 and 86.
    dom : Integer
        The id of the emitter DOM on the given string. Integer between 1 and
        60.
    """
    # load the flasher histogram if we have edata for that emitter
    fname = flasher_dir + 'oux.{}_{}'.format(string, dom)
    if not os.path.isfile(fname):
        print("No data found for {}_{}!".format(string, dom))
        return

    # accumulate all the charge from all time bins
    # the format is string, dom, timebin, charge
    #               b[0],   b[1],b[2],    b[3]
    hits = np.zeros(shape=(5160,))
    bins = np.loadtxt(fname)

    # find the peaks
    peaks = find_peaks(bins)
    for b in bins:
        dom_id = 60*(int(b[0]) - 1) + int(b[1]) - 1
        if b[2] < peaks[dom_id] + settings.DT_MAX and b[2] > peaks[dom_id] - \
           settings.DT_MIN:
            hits[dom_id] += b[3]

    # apply charge cuts
    hits = np.where(hits > settings.Q_MIN, hits, np.zeros_like(hits))
    hits = np.where(hits < settings.Q_SAT, hits, np.zeros_like(hits))

    # save to file
    np.savetxt(data_dir + '{}_{}.hits'.format(string, dom), hits)


if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count() - 1)
    print("Starting jobs...")
    for string in trange(1, 87, leave=False):
        for dom in range(1, 61):
            pool.apply_async(convert, args=(string, dom))
    print("Waiting for jobs to finish...")
    pool.close()
    pool.join()
    log_version("real_data")
    print("Done.")
