# aws settings

provider "aws" {
  region = var.region
}

# Unify tfstate

terraform {
  backend "s3" {
    bucket = "terraform-state-051624633563" # set manually
    key    = "state/mod1/terraform.tfstate"
    region = "us-east-1"
  }
}