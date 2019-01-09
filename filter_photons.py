import click
import os
import numpy as np
import pandas as pd
from tqdm import trange
from find_peaks import find_peaks

raw_data_dir = '/data/user/dima/I3/flashers/oux/'
data_dir = '/data/user/aharnisch/flasher_data/all_cuts/'
photon_dir = '/data/user/aharnisch/iceopt_photons/all_cuts/'

# delta t from peak for time cuts in ns
dt_min = 500.
dt_max = 1000.


@click.command()
@click.argument('dom_id')
def main(dom_id):
    dom_id = int(dom_id)
    dom = dom_id % 60 + 1
    string = dom_id//60 + 1
    print("Working on {}_{}.".format(string, dom))

    # load data hits and get list of all DOMs without charge
    print("Getting excluded DOMs from data...")
    fname = data_dir + '{}_{}.hits'.format(string, dom)
    if not os.path.isfile(fname):
        return
    hits = np.loadtxt(fname)
    excluded = np.where(hits == 0)[0]
    if len(excluded) == 0:
        return

    # load peaks to filter time
    fname = raw_data_dir + 'oux.{}_{}'.format(string, dom)
    if not os.path.isfile(fname):
        print("No data found for {}_{}!".format(string, dom))
        return
    peaks = find_peaks(np.loadtxt(fname))

    # load photons and remove all photons that hit a dom without charge on data
    # and all photons that are outside of the time cut window
    fname = photon_dir + '{}_{}.photons'.format(string, dom)
    if not os.path.isfile(fname):
        raise IOError("Photons file does not exist yet!")

    print("Loading photons...")
    df = pd.read_csv(fname, header=None).fillna(0.)
    print("Filtering photons...")
    photons = df.values
    # init mask
    mask = photons[:, 0] == -1
    for dom in trange(5160, leave=False):
        dom_mask = photons[:, 0] == dom
        if dom in excluded:
            mask = np.logical_or(mask, dom_mask)
        else:
            t_mask = np.logical_or(photons[:, 1] < peaks[dom] - dt_min,
                                   photons[:, 1] > peaks[dom] + dt_max)
            mask = np.logical_or(mask, np.logical_and(dom_mask, t_mask))
    photons = photons[~mask]

    print("Done. {} photons left.".format(len(photons)))
    print("Writing to file...")
    savetxt_sparse_compact(fname, photons)
    print("Done.")


def savetxt_sparse_compact(fname, x, fmt="%g", delimiter=','):
    with open(fname, 'w') as fh:
        for row in x:
            line = delimiter.join("" if value == 0 else fmt % value for value
                                  in row)
            fh.write(line + '\n')


if __name__ == "__main__":
    main()
