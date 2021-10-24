resource "aws_s3_bucket" "datalake" {
  bucket = "${var.base_bucket_name}-${var.environment}-${var.account_id}"
  acl    = "private"

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }


  tags = {
    name        = "${var.base_bucket_name}"
    environment = "${var.environment}"
  }
}


# uploading python jobs

resource "aws_s3_bucket_object" "spark_jobs" {
  for_each = fileset("../jobs/", "*")
  bucket   = aws_s3_bucket.datalake.id
  key      = "emr-code/pyspark/${each.value}"
  source   = "../jobs/${each.value}"
  etag     = filemd5("../jobs/${each.value}")
}