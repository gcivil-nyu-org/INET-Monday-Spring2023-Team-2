# VolunCHEER

[![Python Version](https://img.shields.io/badge/python-3.7-brightgreen.svg)](https://python.org)
[![Django Version](https://img.shields.io/badge/django-3.2.8-brightgreen.svg)](https://djangoproject.com)

## Build and Test Status

### Main

![Main Status](https://github.com/gcivil-nyu-org/INET-Monday-Spring2023-Team-2/actions/workflows/presubmit.yml/badge.svg?branch=main)
![Coverage Status](https://coveralls.io/repos/github/gcivil-nyu-org/INET-Monday-Spring2023-Team-2/badge.svg?branch=main)

### Develop

![Develop Status](https://github.com/gcivil-nyu-org/INET-Monday-Spring2023-Team-2/actions/workflows/presubmit.yml/badge.svg?branch=develop)
![Coverage Status](https://coveralls.io/repos/github/gcivil-nyu-org/INET-Monday-Spring2023-Team-2/badge.svg?branch=develop)

## Development Environment

### Setup

To prepare an environment for development perform the following steps from the
root of the local Github repository:

1. Create a virtual environment:

   ```shell
   virtualenv ${NAME:?}
   ```

1. Activate the environment:

   ```shell
   source ${NAME:?}/bin/activate
   ```

1. Install PyPi dependencies:

   ```shell
   pip install -r voluncheer/requirements.txt
   ```

### Adding New Requirements

If there are new requirements you need to add run the following from the root
directory of the local GitHub repository:

```shell
pip freeze > voluncheer/requirements.txt
```
