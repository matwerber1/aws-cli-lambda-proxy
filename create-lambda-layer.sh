#!/bin/bash

# This script assumes you have pyenv-virtualenv installed on MacOS

# The script will fail if any of the commands fail
set -e

export PROJECT_DIR=$(pwd)

# Automatically detects python version (only works for python3.x)
export PYTHON_VERSION=`python3 -c 'import sys; version=sys.version_info[:3]; print("{0}.{1}".format(*version))'`

# Temporary directory for the virtual environment
export VIRTUAL_ENV_NAME="aws-cli-virtualenv"

# Temporary directory for AWS CLI and its dependencies
export LAMBDA_LAYER_DIR="lambda/aws-cli-layer"

# Creates a directory for virtual environment
mkdir -p ${LAMBDA_LAYER_DIR}

(
  # Needed for pyenv to work in a non-login shell
  eval "$(pyenv init -)"

  # Initializes a virtual environment in the virtual environment directory
  pyenv virtualenv ${VIRTUAL_ENV_NAME}

  pyenv activate ${VIRTUAL_ENV_NAME}

  # This will give you something such as: /Users/YOUR_USERNAME/.pyenv/versions/3.7.0
  export PYENV_ROOT=$(pyenv virtualenv-prefix)
  echo "Pyenv root is ${PYENV_ROOT}"

  # Installs AWS CLI and its dependencies
  pip install awscli

  export VIRTUAL_ENV_PATH=${PYENV_ROOT}/envs/${VIRTUAL_ENV_NAME}

  # Modifies the first line of aws file to #!/var/lang/bin/python (path to Python3 in Lambda)
  # if this command fails, you can manually edit the first line in the "aws" file in a text editor
  sed -i '' "1s/.*/\#\!\/var\/lang\/bin\/python/" $VIRTUAL_ENV_PATH/bin/aws

  # Deactivates the virtual env
  pyenv deactivate

  cp $VIRTUAL_ENV_PATH/bin/aws $PROJECT_DIR/$LAMBDA_LAYER_DIR
  cp -r $VIRTUAL_ENV_PATH/lib/python${PYTHON_VERSION}/site-packages/ $PROJECT_DIR/$LAMBDA_LAYER_DIR

)

pyenv virtualenv-delete -f ${VIRTUAL_ENV_NAME}