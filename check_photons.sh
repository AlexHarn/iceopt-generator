#!/bin/bash

# load python
eval $(/cvmfs/icecube.opensciencegrid.org/py2-v3.0.1/setup.sh)

photon_dir=/data/user/aharnisch/iceopt_photons

string=$1
for dom in {1..60}
do
    ((dom_id = dom - 1 + ($1 - 1)*60))
    echo $string\_$dom: $(cat $photon_dir/$string\_$dom.photons | wc -l)
    python filter_photons.py $dom_id --check
done
