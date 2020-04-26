# AWS CLI Lambda Proxy

This project creates an AWS Lambda layer which contains the AWS CLI and an AWS Lambda function that uses that layer to execute whatever CLI command it get's passed in its invocation parameters. 

## Status

Right now, I have a Lambda function successfully running a test AWS CLI command. 

More work is needed to adapt the function to run whatever command it is passed in its invocation parameters, rather than a hard-coded parameter I sent it. 

## Deployment

This project was built on MacOS using pyenv-virtualenv. Not sure, but its possible the commands in `create-lambda-layer.sh` may need to be tweaked if you're 

1. Clone the repository

2. Install pyenv-virtualenv (on Mac, `brew install pyenv-virtualenv`)

3. Install Python 3.7.0 (`pyenv install 3.7.0`)

4. Switch to Python 3.7.0 (`pyenv global 3.7.0`)

4. Execute the `create-lambda-layer.sh` script to install necessary AWS CLI dependencies to the `lambda/aws-cli-layer` directory:

  ```sh
  ./create-lambda-layer.sh
  ```

5. Run `sam build`

6. Run `sam deploy`