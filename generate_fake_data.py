import click
import os
import numpy as np
import pandas as pd
import subprocess
from tqdm import tqdm
from find_peaks import find_peaks

raw_data_dir = '/data/user/dima/I3/flashers/oux/'
data_dir = '/data/user/aharnisch/flasher_data/all_cuts/'

fake_data_dir = '/data/user/aharnisch/fake_flasher_data/spice_3.2.2/all_cuts/'
path_to_ppc = '/data/user/aharnisch/modded-PPC/real/ice/ppc'

# delta t from peak for time cuts in ns
dt_min = 500.
dt_max = 1000.


@click.command()
@click.argument('dom_id')
def main(dom_id):
    dom_id = int(dom_id)
    flasher_dom = dom_id % 60 + 1
    flasher_string = dom_id//60 + 1
    print("Working on {}_{}.".format(flasher_string, flasher_dom))

    # Initialize the hit list
    # The number of DOMs is 86*60 = 5160
    hits = np.zeros(5160)

    # load total data hits and get list of all DOMs without charge
    print("Getting total hits and excluded DOMs from data...")
    fname = data_dir + '{}_{}.hits'.format(flasher_string, flasher_dom)
    if not os.path.isfile(fname):
        print("No data found for {}_{}!".format(flasher_string, flasher_dom))
        return
    data_hits = np.loadtxt(fname)
    excluded = np.where(data_hits == 0)[0]
    total_hits = np.sum(data_hits)

    # load peaks to filter time
    fname = raw_data_dir + 'oux.{}_{}'.format(flasher_string, flasher_dom)
    if not os.path.isfile(fname):
        print("No data found for {}_{}!".format(flasher_string, flasher_dom))
        return
    peaks = find_peaks(np.loadtxt(fname))

    # accumulate hits until we match total data hits after cuts
    while np.sum(hits) < total_hits:
        photons = simulate_flash(flasher_string, flasher_dom)
        doms = np.setdiff1d(np.arange(5160), excluded, assume_unique=True)
        for dom in tqdm(doms):
            dom_mask = photons[:, 0] == dom
            t_mask = np.logical_or(photons[:, 1] > peaks[dom] - dt_min,
                                   photons[:, 1] < peaks[dom] + dt_max)
            mask = np.logical_and(dom_mask, t_mask)
            # accumulate the hits
            hits[dom] += mask.sum()
        print("{}/{} hits".format(np.sum(hits), total_hits))

    # rescale to exact total hits
    hits *= total_hits/np.sum(hits)

    # write to file
    fname = np.savetxt(fake_data_dir + '{}_{}.hits'.format(flasher_string,
                                                           flasher_dom), hits)
    print("Done.")


def simulate_flash(string, dom, n_photons=1000000000):
    """
    Simulates a single flash of DOM 'dom' on string 'string' with
    'n_photons' photons being emitted by the flasher board with absorption
    enabled to generate fake data.

    Parameters
    ----------
    string : integer
        The id of the string the DOM to flash belongs to. Can be any
        integer between 1 and 86.
    dom : integer
        The id of the DOM to flash on the given string. Can be any integer
        between 1 and 60.
    n_photons : integer
        The amount of photons to be emitted by the flasher board.

    Returns
    -------
    A numpy array containing the PPC output.
    """
    assert round(string) == string and string >= 1 and string <= 86
    assert round(dom) == dom and dom >= 1 and dom <= 60

    p = subprocess.Popen([path_to_ppc, str(string), str(dom),
                          str(n_photons)],
                         stdout=subprocess.PIPE,
                         cwd=os.path.dirname(path_to_ppc))
    out, err = p.communicate()
    df = pd.read_csv(pd.compat.StringIO(out.decode()), header=None)
    return df.values


if __name__ == "__main__":
    main()
