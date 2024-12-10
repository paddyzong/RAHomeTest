# main.tf

terraform {
  backend "remote" {
    organization = "youkobak"

    workspaces {
      name = "RAHomeTest"
    }
  }
}

provider "aws" {
  region = "ap-southeast-2"
}

# S3 Bucket
resource "aws_s3_bucket" "ra_frontend_bucket" {
  bucket = "rahometest-frontend-bucket"

  tags = {
    Name        = "FrontendBucket"
    Environment = "Production"
  }
}

resource "aws_s3_bucket_acl" "ra_frontend_bucket_acl" {
  bucket = aws_s3_bucket.ra_frontend_bucket.id
  acl    = "private"
}

# S3 Bucket Website Configuration
resource "aws_s3_bucket_website_configuration" "ra_frontend_website" {
  bucket = aws_s3_bucket.ra_frontend_bucket.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "error.html"
  }
}

# Origin Access Identity
resource "aws_cloudfront_origin_access_identity" "oai" {
  comment = "OAI for Frontend S3 Bucket"
}

# S3 Bucket Policy
resource "aws_s3_bucket_policy" "ra_frontend_bucket_policy" {
  bucket = aws_s3_bucket.ra_frontend_bucket.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = {
          AWS = aws_cloudfront_origin_access_identity.oai.iam_arn
        }
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.ra_frontend_bucket.arn}/*"
      }
    ]
  })
}

# CloudFront Distribution
resource "aws_cloudfront_distribution" "ra_frontend_distribution" {
  origin {
    domain_name = aws_s3_bucket.ra_frontend_bucket.bucket_regional_domain_name
    origin_id   = "S3-FrontendBucket"

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.oai.cloudfront_access_identity_path
    }
  }

  enabled             = true
  is_ipv6_enabled     = true
  comment             = "CloudFront Distribution for Frontend"
  default_root_object = "index.html"

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD", "OPTIONS"]
    target_origin_id = "S3-FrontendBucket"
    viewer_protocol_policy = "redirect-to-https"
    forwarded_values {
      query_string = false

      cookies {
        forward = "none"
      }
    }
  }

  price_class = "PriceClass_100"

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }
  viewer_certificate {
    cloudfront_default_certificate = true
  }
  tags = {
    Environment = "Production"
    Name        = "FrontendDistribution"
  }
}

