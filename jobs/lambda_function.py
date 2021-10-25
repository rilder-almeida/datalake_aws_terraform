import boto3
from datetime import datetime

sageclient = boto3.client("sagemaker")
sagemaker_role = "arn:aws:iam::051624633563:role/service-role/IGTISagemakerRole"


def handler(event, context):

    process_job_arn = sageclient.create_processing_job(
        ProcessingJobName=f"censo-extraction-{datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}",
        ProcessingOutputConfig={
            "Outputs": [
                {
                    "OutputName": "censoecolar",
                    "S3Output": {
                        "S3Uri": "s3://datalake-iac-mod1-prod-051624633563/raw-data/censo/year=2020/",
                        "LocalPath": "/opt/ml/processing/output/censoescolar",
                        "S3UploadMode": "EndOfJob",
                    },
                }
            ]
        },
        ProcessingResources={
            "ClusterConfig": {
                "InstanceCount": 1,
                "InstanceType": "ml.m5.xlarge",
                "VolumeSizeInGB": 50,
            }
        },
        AppSpecification={
            "ImageUri": "051624633563.dkr.ecr.us-east-1.amazonaws.com/igti-ecr-censo-image:latest"
        },
        RoleArn=sagemaker_role,
    )

    return {
        "statusCode": 200,
        "body": f"Started job {process_job_arn['ProcessingJobName']}",
    }
