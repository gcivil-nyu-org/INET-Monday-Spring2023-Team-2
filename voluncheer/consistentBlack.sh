python3 -m black -t py38 .
flake8 --filename=*.py --exclude=test_*,*_initial.py --max-line-length 100 --ignore=F401 --exclude=voluncheer/lib,voluncheer/bin/