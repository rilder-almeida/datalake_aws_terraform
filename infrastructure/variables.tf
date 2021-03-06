variable "environment" {
  default = "prod"
}

variable "account_id" {
  default = "051624633563" # set manually
}

variable "region" {
  default = "us-east-1" # set manually
}
variable "lambda_function_name" {
  default = "UnzipCensoJob"
}

variable "base_bucket_name" {
  default = "datalake-iac-mod1" # set manually
}