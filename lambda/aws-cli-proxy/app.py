from __future__ import print_function
import subprocess
import logging
import traceback
import json

print('Loading function')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def run_command(command):
    command_list = command.split(' ')
    response = None
    try:
        logger.info("Running shell command: \"{}\"".format(command))
        result = subprocess.run(command_list, stdout=subprocess.PIPE, stderr=subprocess.STDOUT);
        response = result.stdout.decode('UTF-8')
        logger.info("Command output:\n------------------\n{}\n------------------".format(response))
    except Exception as e:
        stacktrace = traceback.format_exc()
        response = "Command exception: {}\n--------------\n{}".format(e, stacktrace)
        logger.error(response)
    return response

def lambda_handler(event, context):

    #
    # event: {
    #   commandToRun: "aws s3api get-bucket-acl --bucket werberm-example-bucket --output json"
    # }
    #

    print("Received event: \n" + json.dumps(event, indent=2))

    commandToRun = event['commandToRun']
    commandArray = commandToRun.split(" ", 1)
 
    commandResult = None

    if (commandArray[0] == 'aws'):
        commandResult = run_command('/opt/aws {}'.format(commandArray[1]))
        
    else:
        commandResult = "Exception: not a valid AWS CLI command."
        logger.error(response)
    
    response = {
        "commandResult": commandResult
    }
    
    return response