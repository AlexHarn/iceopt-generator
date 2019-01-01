import os
import numpy as np
from tqdm import trange
import multiprocessing

flasher_dir = '/data/user/dima/I3/flashers/oux/'
data_dir = '/data/user/aharnisch/flasher_data_charge_only/'


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
    # load the flasher histogram if we hav edata for that emitter
    fname = flasher_dir + 'oux.{}_{}'.format(string, dom)
    if not os.path.isfile(fname):
        return

    # accumulate all the charge from all tiem bins
    # the format is string, dom, timebin, charge
    #               b[0],   b[1],b[2],    b[3]
    # TODO: Include cuts in time and charge
    hits = np.zeros(shape=(5160,))
    bins = np.loadtxt(fname)
    for b in bins:
        hits[60*(int(b[0]) - 1) + int(b[1]) - 1] += b[3]

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
    print("Done.")
