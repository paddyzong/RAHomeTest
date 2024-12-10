# Provider configuration for Kubernetes
provider "kubernetes" {
  host                   = data.aws_eks_cluster.my_eks_cluster.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.my_eks_cluster.certificate_authority[0].data)
  token                  = data.aws_eks_cluster_auth.my_eks_cluster_auth.token
}

# IAM Role for EKS service
resource "aws_iam_role" "eks_service_role" {
  name = "eks-service-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Principal = {
          Service = "eks.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "eks_cluster_policy_attachment" {
  role       = aws_iam_role.eks_service_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
}

resource "aws_iam_role_policy_attachment" "eks_service_policy_attachment" {
  role       = aws_iam_role.eks_service_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSServicePolicy"
}

resource "aws_iam_role_policy_attachment" "ecr_read_only_policy_attachment" {
  role       = aws_iam_role.eks_service_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}


# VPC Creation for EKS Cluster
resource "aws_vpc" "my_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
}

# Public Subnet for EKS Cluster
resource "aws_subnet" "public_subnet" {
  vpc_id                  = aws_vpc.my_vpc.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "ap-southeast-2"  # Adjust based on your region
}

# EKS Cluster creation
resource "aws_eks_cluster" "my_eks_cluster" {
  name     = "my-cluster"
  role_arn = aws_iam_role.eks_service_role.arn

  vpc_config {
    subnet_ids = [aws_subnet.public_subnet.id]
  }

  tags = {
    Name = "my-eks-cluster"
  }
}

# Fetching the EKS Cluster and Authentication info for Kubernetes provider
data "aws_eks_cluster" "my_eks_cluster" {
  name = aws_eks_cluster.my_eks_cluster.name
}

data "aws_eks_cluster_auth" "my_eks_cluster_auth" {
  name = aws_eks_cluster.my_eks_cluster.name
}

resource "kubernetes_manifest" "backend_deployment" {
  manifest = yamldecode(file("k8s_aws/backend-deployment.yaml"))
}

resource "kubernetes_manifest" "backend_service" {
  manifest = yamldecode(file("k8s_aws/backend-service.yaml"))
}

resource "kubernetes_manifest" "celery_deployment" {
  manifest = yamldecode(file("k8s_aws/celery-deployment.yaml"))
}

resource "kubernetes_manifest" "celery_scaler_role" {
  manifest = yamldecode(file("k8s_aws/celery-scaler-role.yaml"))
}

resource "kubernetes_manifest" "celery_scaler_rolebinding" {
  manifest = yamldecode(file("k8s_aws/celery-scaler-rolebinding.yaml"))
}

resource "kubernetes_manifest" "redis_deployment" {
  manifest = yamldecode(file("k8s_aws/redis-deployment.yaml"))
}

resource "kubernetes_manifest" "redis_service" {
  manifest = yamldecode(file("k8s_aws/redis-service.yaml"))
}

resource "kubernetes_manifest" "scale_celery_up_cronjob" {
  manifest = yamldecode(file("k8s_aws/scale-celery-up-cronjob.yaml"))
}
