#!/bin/sh

source activate tensorflow_p36

python3 download_essentials.py

python3 downloadfroms3.py

export PYTHONPATH='$PYTHONPATH:/home/ubuntu/models/research:/home/ubuntu/models/research/slim'
python3 setup.py

python3 errorfix.py

echo 'export PYTHONPATH=$PYTHONPATH:/home/ubuntu/models/research:/home/ubuntu/models/research/slim'

#python3 ./utils/jupytersetup.py

