#!/bin/bash

# first argument is the process id, the second a constant offset to allow for
# easier generation of partial data sets
((dom_id = $1 + $2))

# define the paths here
PPC=/data/user/aharnisch/modded-PPC/no_abs/ice/ppc
photon_dir=/data/user/aharnisch/iceopt_photons/
data_dir=/data/user/aharnisch/flasher_data_charge_only
generator_dir=/data/user/aharnisch/iceopt-generator

# load python
eval $(/cvmfs/icecube.opensciencegrid.org/py2-v3.0.1/setup.sh)

# the number of photons to emmit in the simulation
n_photons=100000000
# the number of desired hits in the final output file
n_hits=700000
# maximum number of photons in file to prevent running out of memory
((max_len = 4*$n_hits))

(( dom = $dom_id%60+1))
(( string = $dom_id/60+1))
cd "$(dirname $PPC)"
while true
do
    $PPC $string $dom $n_photons >> $photon_dir/$string\_$dom.photons
    if [ $(cat $photon_dir/$string\_$dom.photons | wc -l) -gt $max_len ]
    then
        sed -i $((max_len + 1))',$ d' $photon_dir/$string\_$dom.photons
    fi
    echo Total hits before filtering: $(cat $photon_dir/$string\_$dom.photons | wc -l)
    # python $generator_dir/filter_photons.py $dom_id
    echo Total hits so far: $(cat $photon_dir/$string\_$dom.photons | wc -l)
    [ $(cat $photon_dir/$string\_$dom.photons | wc -l) -lt $n_hits ] || break
done
if [ $(cat $photon_dir/$string\_$dom.photons | wc -l) -gt $n_hits ]
then
    sed -i $((n_hits + 1))',$ d' $photon_dir/$string\_$dom.photons
fi
# python $generator_dir/log_version.py photons
echo $dom_id >> $generator_dir/logs/done
