#!/bin/bash

generator_dir=/data/user/aharnisch/iceopt-generator

# load python
eval $(/cvmfs/icecube.opensciencegrid.org/py2-v3.0.1/setup.sh)

# iterate over string
#for dom in {0..59}
for dom in {0..5}
do
    ((dom_id = ($1-1)*60 + $dom))
    python $generator_dir/generate_fake_data.py $dom_id
done
python $generator_dir/log_version.py fake_data
