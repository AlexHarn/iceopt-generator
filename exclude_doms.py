import click
import os
import numpy as np
import pandas as pd
from tqdm import tqdm

data_dir = '/data/user/aharnisch/flasher_data_charge_only/'
photon_dir = '/data/user/aharnisch/iceopt_photons/'


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

    # load photons and remove all photons that hit a dom without charge on data
    fname = photon_dir + '{}_{}.photons'.format(string, dom)
    if not os.path.isfile(fname):
        raise IOError("Photons file does not exist yet!")

    print("Loading photons...")
    df = pd.read_csv(fname, header=None).fillna(0.)
    print("Excluding DOMs...")
    photons = df.values
    mask = photons[:, 0] == excluded[0]
    if len(excluded) > 1:
        for dom in tqdm(excluded[1:], leave=False):
            mask = np.logical_or(mask, photons[:, 0] == dom)
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
