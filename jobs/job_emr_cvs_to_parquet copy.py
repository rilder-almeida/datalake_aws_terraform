import sys
import boto3
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext

## @params: ['JOB_NAME']
args = getResolvedOptions(sys.argv, ["JOB_NAME"])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)


# TABLE_NAMES = [
#     "docentes_co",
#     "docentes_nordeste",
#     "docentes_norte",
#     "docentes_sudeste",
#     "docentes_sul",
#     "escolas",
#     "gestor",
#     "matricula_co",
#     "matricula_nordeste",
#     "matricula_norte",
#     "matricula_sudeste",
#     "matricula_sul",
#     "turmas",
# ]

source_path = "s3://datalake-iac-mod1-prod-051624633563/raw-data/censo/year=2020/"
dest_path = "s3://datalake-iac-mod1-prod-051624633563/staging/censo/year=2020/"


def get_table_names():
    """Get file names from s3 source folder

    Returns:
        list: file list from s3 source folder
    """

    bucket = boto3.resource("s3").Bucket("datalake-iac-mod1-prod-051624633563")
    return [
        obj.split(source_path)[1] for obj in bucket.objects.filter(Prefix=source_path)
    ]


def read_table(table_name):
    """Read csv file to dataframe

    Args:
        table_name (str): target table name

    Returns:
        dataframe: read dataframe from csv file
    """
    return (
        spark.read.format("csv")
        .option("header", True)
        .option("inferSchema", True)
        .option("delimiter", "|")
        .load(source_path + table_name + ".CSV")
        .cache()
    )


def write_table(df, table_name):
    """Write table in parquet from dataframe

    Args:
        df (dataframe): target dataframe
        table_name (str): target table name
    """
    (
        df.write.mode("overwrite")
        .format("parquet")
        .partitionBy("NU_ANO_CENSO")
        .save("dest_path" + table_name)
    )


TABLE_NAMES = [table.split(".csv")[0] for table in get_table_names()]

for t in TABLE_NAMES:
    df = read_table(t)
    write_table(df, t)

# job.commit()
