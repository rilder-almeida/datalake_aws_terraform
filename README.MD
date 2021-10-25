# AWS Datalake with Terraform and Github Actions
> Project model for AWS Data Lake implementing by Terraform infrastructure and automated CI/CD with Github Actions.

## For what purpose?

This project was born from the need to ingest batch data from a third-party website to the cloud and provide them with a suitable format to be consulted, in an optimized and automated way.

## What was the context-situation?

You are a data engineer at a large educational institution. The manager of his area started a new data intelligence project with the objective of understanding the performance of high school students from all over Brazil in the National High School Exam (ENEM). Thus, you will be responsible for building a Data Lake with data from ENEM 2019, processing it using appropriate tools and making the data available for consultation by business users and BI analysts. To perform this activity, the use of AWS services is recommended. However, if you prefer, you can build your lake and its data processing structure in any cloud provider you prefer.

## Cloud Well-Architecture designed for case

![](https://github.com/rilder-almeida/datalake_aws_terraform/raw/master/design_datalake.jpg)

## How it works?
To provide all the necessary infrastructure in an automated way, Github Actions and Terraform were used. This required two git workflows, deploy and test, each working on its own branch. After preparing the environment and security for the keys used by aws cli, a bash script will package python's lambda function (explained shortly) and finally terraform will be called to deploy the pre-configured services to the cloud.

Terraform, in turn, will provide all functions and policies for services like lambda, sagemaker, s3, glue job, glue triggers and glue crawler. As well, it will determine the flow between services and stages so that the objective is successfully achieved.

## Step-by-Step
### Ingestion

There are 2 ways to ingest required data:
- Directly from the web source: In this case, the data will be compressed, zipped, so it was necessary to prepare services so that in addition to downloading the file, it will also be possible to decompress and load it into the bucket. This step is performed manually through a bash script __(1)__, loading a docker image from a python environment into the ECR and calling the Lambda function to create an instance of Sagemaker processing job __(3)__, which in turn will use the image to download the file, unzipping and loading to the S3.

- Loading locally to bucket __(2)__: In this way, data files are already in csv and unzipped format. A python script is called manually to load all files from the raw data folder directly to S3.

### Processing

At the processing stage, thinking about optimization, the Glue service __(4)__ was used. Which will work in the following way:

- A Glue Trigger was deployed so that once a day, the raw data can be processed, and converted from csv format to parquet, through a Glue Job. It is interesting to note that other ETL jobs can be performed to that data is properly prepared for analysis.

- Immediately after the data was converted, another Glue Trigger will run to call a Glue Crawler that will be responsible for allocating the parquet files in a glue database catalog.

### Provisioning

Once the data is provisioned in a database catalog, they can be read in the Athena Database __(5)__ service, which through the metadata is capable to structuring them in tables separated by ingested file, so that it will possible to consult them in an analytically efficient way. Also will allow to save these queries in an automated way again in S3 in a gold zone.

## Meta

Rilder Almeida – [LinkedIn](https://www.linkedin.com/in/rilder-almeida)

rilder.almeida@gmail.com

[Other Projets](https://github.com/rilder-almeida)
