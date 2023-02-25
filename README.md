# Team Project repo

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
