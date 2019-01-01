#!/bin/bash

PPC=/data/user/aharnisch/modded-PPC/no_abs/ice/ppc
photon_dir=/data/user/aharnisch/iceopt_photons
data_dir=/data/user/aharnisch/flasher_data_charge_only
generator_dir=/data/user/aharnisch/iceopt-generator

# load python
eval $(/cvmfs/icecube.opensciencegrid.org/py2-v3.0.1/setup.sh)

# the number of photons to emmit in the simulation
n_photons=20000000
# the number of desired hits in the final output file
n_hits=700000

(( dom = $1%60+1))
(( string = $1/60+1))
cd "$(dirname $PPC)"
$PPC $string $dom $n_photons > $photon_dir/$string\_$dom.photons
python $generator_dir/exclude_doms.py $1
while [ $(cat $photon_dir/$string\_$dom.photons | wc -l) -lt $n_hits ]
do
    echo Total hits so far: $(cat $photon_dir/$string\_$dom.photons | wc -l)
    $PPC $string $dom $n_photons >> $photon_dir/$string\_$dom.photons
    python $generator_dir/exclude_doms.py $1
done
sed -i $((n_hits + 1))',$ d' $photon_dir/$string\_$dom.photons
echo $1 >> $generator_dir/logs/done
