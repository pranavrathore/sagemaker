#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import boto3

client = boto3.client('sagemaker')

response = client.create_notebook_instance(
    NotebookInstanceName='chacha-chaudhary',
    InstanceType='ml.t2.medium',
    SubnetId='subnet-a28e3e9c',
    SecurityGroupIds=[
        'sg-c7058083',
    ],
    RoleArn='arn:aws:iam::460207325220:role/service-role/AmazonSageMaker-ExecutionRole-20190224T165979',
    Tags=[
        {
            'Key': 'Name',
            'Value': 'tinkle'
        },
    ],
    DirectInternetAccess='Enabled',
    VolumeSizeInGB=5
    
    
)
