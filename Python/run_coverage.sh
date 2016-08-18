old_path=$(PWD)
old_pythonpath=$PYTHONPATH
. ./venv/bin/activate
export PYTHONPATH=$PYTHONPATH:$PWD
cd manager
coverage run --omit=../venv/*,../lib/* unit_tests.py
coverage report
cd "$old_path"
export PYTHONPATH=$old_pythonpath
