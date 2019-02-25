import click
import os
import numpy as np
import pandas as pd
import settings
from tqdm import trange
from find_peaks import find_peaks


@click.command()
@click.argument('dom_id')
def main(dom_id):
    dom_id = int(dom_id)
    dom = dom_id % 60 + 1
    string = dom_id//60 + 1
    print("Working on {}_{}.".format(string, dom))

    # load data hits and get list of all DOMs without charge
    print("Getting excluded DOMs from data...")
    fname = settings.DATA_DIR + '{}_{}.hits'.format(string, dom)
    if not os.path.isfile(fname):
        return
    hits = np.loadtxt(fname)
    excluded = np.where(hits == 0)[0]
    if len(excluded) == 0:
        return

    # load peaks to filter time
    fname = settings.RAW_DATA_DIR + 'oux.{}_{}'.format(string, dom)
    if not os.path.isfile(fname):
        print("No data found for {}_{}!".format(string, dom))
        if settings.EXCLUDE_DOMS:
            return
    else:
        if settings.T_CUTS:
            peaks = find_peaks(np.loadtxt(fname))

    # load photons and remove all photons that hit a dom without charge on data
    # and all photons that are outside of the time cut window
    fname = settings.PHOTON_DIR + '{}_{}.photons'.format(string, dom)
    if not os.path.isfile(fname):
        raise IOError("Photons file does not exist yet!")

    print("Loading photons...")
    df = pd.read_csv(fname, header=None).fillna(0.)
    print("Filtering photons...")
    photons = df.values
    # init mask with False entries
    mask = photons[:, 0] == -1
    for dom in trange(5160, leave=False):
        dom_mask = photons[:, 0] == dom
        if dom in excluded:
            if settings.EXCLUDE_DOMS:
                mask = np.logical_or(mask, dom_mask)
        else:
            if settings.T_CUTS:
                t_mask = np.logical_or(photons[:, 1] < peaks[dom] -
                                       settings.DT_MIN,
                                       photons[:, 1] > peaks[dom] +
                                       settings.DT_MAX)
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
