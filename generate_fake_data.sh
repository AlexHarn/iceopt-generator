#!/bin/bash

# first argument is the process id, the second a constant offset to allow for
# easier generation of partial data sets
((dom_id = $1 + $2))

generator_dir=/data/user/aharnisch/iceopt-generator

# load python
eval $(/cvmfs/icecube.opensciencegrid.org/py2-v3.0.1/setup.sh)

python $generator_dir/generate_fake_data.py $dom_id
python $generator_dir/log_version.py fake_data
echo $dom_id >> $generator_dir/logs/done.fake_data
