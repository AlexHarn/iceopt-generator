# ---------------------------------- Paths ------------------------------------
RAW_DATA_DIR = '/data/user/dima/I3/flashers/oux/'
DATA_DIR = '/data/user/aharnisch/flasher_data_charge_only/'
PHOTON_DIR = '/data/user/aharnisch/iceopt_photons/'
FAKE_DATA_DIR = \
    '/data/user/aharnisch/fake_flasher_data/'
PPC_DIR = '/data/user/aharnisch/modded-PPC/real/ice/'

# ----------------------------------- Cuts ------------------------------------
# If true, exclude all DOMs in photons and on fake data, that do not see charge
# on real data and also don't generate fake data for emitter DOMs for which we
# hav no real data
EXCLUDE_DOMS = True
# If true, apply the charge cuts to real data, with excluded DOMs this
# automaticially propagates to fake data and photons
Q_CUTS = True
# values for charge cut in PE
Q_MIN = .1
Q_SAT = 500.
# If true, apply the time cuts to real data, fake data, and photons
T_CUTS = True
# minimal and maximal time in ns, that define the time cut window around the
# waveform peak
DT_MIN = 500.
DT_MAX = 1000.

# ---------------------------------- Other ------------------------------------
# If True, the total charge on fake data will be rescaled to equal the total
# charge on real data
RESCALE_FAKE_DATA = True
