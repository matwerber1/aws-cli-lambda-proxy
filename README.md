# AWS CLI Lambda Proxy

This project creates an [AWS Lambda layer](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html) which contains the [AWS CLI](https://aws.amazon.com/cli/) and an [AWS Lambda function](https://aws.amazon.com/lambda/) that uses that layer to execute whatever CLI command it get's passed in its invocation parameters. 

## Background

The idea is that I want to create a "serverless AWS CLI" that I can embed into web apps. My vision is a static S3 website in which a user logs into a Cognito User Pool that is linked to a Cognito Identity Pool that allows the user to invoke this Lambda function. The web UI would have a text box skinned to look like a terminal and, when the user entered an AWS CLI command, it would then invoke the Lambda function with the same command as an input, receive results, and display them to the user. 

## Credits

The key steps needed to create a Lambda Layer containing the AWS CLI and the proxy function were adapted from:

* https://alestic.com/2016/11/aws-lambda-awscli/
* https://bezdelev.com/hacking/aws-cli-inside-lambda-layer-aws-s3-sync/

## Security

Right now, the Lambda function will be able to invoke whatever CLI commands that are supported by the function's IAM role. In the future, I would like to adapt the function to instead also expect the invoke to provide temporary STS credentials (e.g. from the caller's identity pool) and assume that role so that it only executes commands within the context of the user. Either that, or build some sort of custom authorization scheme.

## Status

I have a Lambda function successfully running a test AWS CLI command. 

More work is needed to adapt the function to run whatever command it is passed in its invocation parameters, rather than a hard-coded parameter I sent it. 

## Deployment

This project was built on MacOS using [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv). Not sure, but its possible the commands in `create-lambda-layer.sh` may need to be tweaked if you're using a different OS or using pyenv and virtualenv separately instead of the combined pyenv-virtualenv project. This project also requires the [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html).

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