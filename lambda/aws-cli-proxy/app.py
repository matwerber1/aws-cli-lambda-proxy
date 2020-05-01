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

# At the moment, the Lambda will execute the passed command with whatever role
# is attached to the Lambda function. The Cognito app is passiing the user's
# identity pool temp STS credentials, I just don't know how to assume them
# for the CLI. If we were doing everything in boto3, that would be easy...

def lambda_handler(event, context):

    print("Received event: \n" + json.dumps(event, indent=2))

    access_key = event['credentials']['accessKeyId']
    secret_key = event['credentials']['secretAccessKey']
    session_token = event['credentials']['sessionToken']
    
    #run_command('export AWS_ACCESS_KEY_ID={}'.format(access_key))
    #run_command('export AWS_SECRET_ACCESS_KEY_ID={}'.format(secret_key))
    #run_command('export AWS_SESSION_TOKEN={}'.format(session_token))

    commandToRun = event['commandToRun']
    commandArray = commandToRun.split(" ", 1)
 
    commandResult = None

    if (commandArray[0] == 'aws'):
        commandResult = run_command('/opt/aws {}'.format(commandArray[1]))
        #final_command = '(AWS_ACCESS_KEY_ID={} && AWS_SECRET_ACCESS_KEY_ID={} && AWS_SESSION_TOKEN={} && /opt/aws {})'.format(access_key,secret_key,session_token,commandArray[1])
        #commandResult = run_command(final_command)
    else:
        commandResult = "Exception: not a valid AWS CLI command."
        logger.error(commandResult)
    
    response = {
        "commandResult": commandResult
    }
    
    return response