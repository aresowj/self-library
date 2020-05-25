#!/bin/bash
source /home/kagami/python_env/jupyter/bin/activate
cd /home/kagami/jupyter
exec jupyter notebook --ip=0.0.0.0 &> /home/kagami/jupyter_run.log
