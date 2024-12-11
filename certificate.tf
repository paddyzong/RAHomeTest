resource "aws_acm_certificate" "ra_certificate" {
  domain_name       = "*.rahometest.click"         # Replace with your domain
  validation_method = "DNS"                 # Can be "DNS" or "EMAIL"

  tags = {
    Environment = "Production"
    Name        = "ra-certificate"
  }
}

resource "aws_route53_record" "ra_record" {
  for_each = {
    for dvo in aws_acm_certificate.ra_certificate.domain_validation_options : dvo.domain_name => {
      name  = dvo.resource_record_name
      type  = dvo.resource_record_type
      value = dvo.resource_record_value
    }
  }

  zone_id = "Z0787172Q9SOK5I6GQH9"  # Replace with your Route 53 Hosted Zone ID
  name    = each.value.name
  type    = each.value.type
  records = [each.value.value]
  ttl     = 900
}

resource "aws_acm_certificate_validation" "ra_validation" {
  certificate_arn         = aws_acm_certificate.ra_certificate.arn
  validation_record_fqdns = [for record in aws_route53_record.ra_record : record.fqdn]
}

# ACM Certificate in us-east-1
resource "aws_acm_certificate" "frontend_cert_us_east_1" {
  provider                  = aws.us_east_1
  domain_name               = "*.rahometest.click"         # Replace with your domain
  validation_method         = "DNS"

  tags = {
    Environment = "Production"
    Name        = "FrontendCertificateUS_EAST_1"
  }
}

resource "aws_acm_certificate_validation" "frontend_cert_validation_us_east_1" {
  provider                  = aws.us_east_1
  certificate_arn           = aws_acm_certificate.frontend_cert_us_east_1.arn
  validation_record_fqdns   = [for record in aws_route53_record.ra_record : record.fqdn]
}
