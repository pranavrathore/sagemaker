#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import boto3
from time import gmtime, strftime

region_name = 'us-east-1'

job_name = 'kmeans-lowlevel-' + strftime("%Y-%m-%d-%H-%M-%S", gmtime())
print("Training job", job_name)

image = '382416733822.dkr.ecr.us-east-1.amazonaws.com/kmeans:latest'
bucket = 'sagemaker-us-east-1-460207325220'

output_location = 's3://sagemaker-us-east-1-460207325220/kmeans_lowlevel_example/output'
print('training artifacts will be uploaded to: {}'.format(output_location))

role = 'arn:aws:iam::460207325220:role/service-role/AmazonSageMaker-ExecutionRole-20190224T165979'

data_location = 's3://sagemaker-us-east-1-460207325220/kmeans_lowlevel_example/data'

create_training_params = \
{
    "AlgorithmSpecification": {
        "TrainingImage": image,
        "TrainingInputMode": "File"
    },
    "RoleArn": role,
    "OutputDataConfig": {
        "S3OutputPath": output_location
    },
    "ResourceConfig": {
        "InstanceCount": 1,
        "InstanceType": "ml.m4.xlarge",
        "VolumeSizeInGB": 10
    },
    "TrainingJobName": job_name,
    "HyperParameters": {
        "k": "10",
        "feature_dim": "784",
        "mini_batch_size": "500",
        "force_dense": "True"
    },
    "StoppingCondition": {
        "MaxRuntimeInSeconds": 60 * 60
    },
    "InputDataConfig": [
        {
            "ChannelName": "train",
            "DataSource": {
                "S3DataSource": {
                    "S3DataType": "S3Prefix",
                    "S3Uri": data_location,
                    "S3DataDistributionType": "FullyReplicated"
                }
            },
            "CompressionType": "None",
            "RecordWrapperType": "None",
            "InputMode": "Pipe"
        }
    ]
}

sagemaker = boto3.client('sagemaker')

sagemaker.create_training_job(**create_training_params)

status = sagemaker.describe_training_job(TrainingJobName=job_name)['TrainingJobStatus']
print(status)

try:
    sagemaker.get_waiter('training_job_completed_or_stopped').wait(TrainingJobName=job_name)
finally:
    status = sagemaker.describe_training_job(TrainingJobName=job_name)['TrainingJobStatus']
    print("Training job ended with status: " + status)
    if status == 'Failed':
        message = sagemaker.describe_training_job(TrainingJobName=job_name)['FailureReason']
        print('Training failed with the following error: {}'.format(message))
        raise Exception('Training job failed')

