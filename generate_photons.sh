#!/bin/bash

PPC=/data/user/aharnisch/modded-PPC/no_abs/ice/ppc
photon_dir=/data/user/aharnisch/iceopt_photons
log_file=/data/user/aharnisch/generate_photons/logs/done

# load python
eval $(/cvmfs/icecube.opensciencegrid.org/py2-v3.0.1/setup.sh)

# the number of photons to emmit in the simulation
n_photons=20000000
# the number of desired hits in the final output file
n_hits=700000

(( dom = $1%60+1))
(( string = $1/60+1))
cd "$(dirname $PPC)"
$PPC $string $dom $n_photons > $string\_$dom.photons
while [ $(cat $string\_$dom.photons | wc -l) -lt $n_hits ]
do
    echo Total hits so far: $(cat $string\_$dom.photons | wc -l)
    $PPC $string $dom $n_photons >> $string\_$dom.photons
done
sed -i $((n_hits + 1))',$ d' $string\_$dom.photons
mv $string\_$dom.photons $photon_dir/$string\_$dom.photons
echo $1 >> $log_file
