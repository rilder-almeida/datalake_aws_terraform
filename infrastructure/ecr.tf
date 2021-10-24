resource "aws_ecr_repository" "repo" {
  name = "igti-ecr-censo-image"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = false
  }
}