#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import boto3

client  = boto3.client('sagemaker')

response = client.create_presigned_notebook_instance_url(
    NotebookInstanceName='chacha-chaudhary',
    SessionExpirationDurationInSeconds=1800
)

print(response)
