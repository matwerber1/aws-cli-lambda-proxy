from __future__ import print_function
import subprocess
import os
import logging
import traceback
import json

print('Loading function')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def run_command(command, credentials):
    
    my_env = os.environ.copy()
    my_env["AWS_ACCESS_KEY_ID"] = credentials['accessKeyId']
    my_env["AWS_SECRET_ACCESS_KEY"] = credentials['secretAccessKey']
    my_env["AWS_SESSION_TOKEN"] = credentials['sessionToken']
    my_env["AWS_REGION"] = 'us-west-2'

    command_list = command.split(' ')
    response = None
    try:
        logger.info("Running shell command: \"{}\"".format(command))
        result = subprocess.run(command_list, env=my_env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT);
        response = result.stdout.decode('UTF-8')
        logger.info("Command output:\n------------------\n{}\n------------------".format(response))
    except Exception as e:
        stacktrace = traceback.format_exc()
        response = "Command exception: {}\n--------------\n{}".format(e, stacktrace)
        logger.error(response)
    return response

def lambda_handler(event, context):

    # DO NOT PRINT EVENT, SINCE IT CONTAINS (TEMPORARY) COGNITO ACCESS KEYS FOR THE CALLING USER
    # It would not be secure to have these stored in logs...
    # Only used this for debugging...
    # print("Received event: \n" + json.dumps(event, indent=2))

    credentials = event['credentials'];
    commandToRun = event['commandToRun']
    commandArray = commandToRun.split(" ", 1)
    commandResult = None

    if (commandArray[0] == 'aws'):
        commandResult = run_command('/opt/aws {}'.format(commandArray[1]), credentials)
    else:
        commandResult = "Exception: not a valid AWS CLI command."
        logger.error(commandResult)
    
    response = {
        "commandResult": commandResult
    }
    
    return response