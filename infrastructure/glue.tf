#############
## CRAWLER ##
#############

resource "aws_glue_catalog_database" "censo" {
  name = "censodb"
}

resource "aws_glue_crawler" "censo" {
  database_name = aws_glue_catalog_database.censo.name
  name          = "censo_s3_crawler"
  role          = aws_iam_role.glue_role.arn

  s3_target {
    path = "s3://${aws_s3_bucket.datalake.bucket}/staging/censo/year=2020/"
  }

  tags = {
    IES   = "IGTI",
    CURSO = "EDC"
  }
}

##########
## JOBS ##
##########

resource "aws_glue_job" "censo" {
  name     = "censo_job"
  role_arn = aws_iam_role.glue_role.arn

  command {
    script_location = "s3://${aws_s3_bucket.datalake.bucket}/emr-code/pyspark/job_emr_cvs_to_parquet.py"
  }

  execution_property {
    max_concurrent_runs = "1"
  }
}

#############
## TRIGGER ##
#############

resource "aws_glue_trigger" "censo" {
  name = "censo_trigger"
  type = "CONDITIONAL"

  actions {
    crawler_name = aws_glue_crawler.censo.name
  }

  predicate {
    conditions {
      job_name = aws_glue_job.censo.name
      state    = "SUCCEEDED"
    }
  }
}