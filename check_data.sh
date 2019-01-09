#!/bin/bash

photon_dir=/data/user/aharnisch/iceopt_photons/all_cuts

string=$1
for dom in {1..60}
do
    echo $string\_$dom: $(cat $photon_dir/$string\_$dom.photons | wc -l)
done
