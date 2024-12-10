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
          Service = [
            "eks.amazonaws.com",
            "ec2.amazonaws.com"
          ]
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

resource "aws_iam_role_policy_attachment" "ecr_read_only_policy_attachment_service" {
  role       = aws_iam_role.eks_service_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

# IAM Role for EKS Worker Nodes
resource "aws_iam_role" "eks_node_role" {
  name = "eks-node-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "ec2.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

# Attach Required Policies to Node Role
resource "aws_iam_role_policy_attachment" "eks_worker_node_policy" {
  role       = aws_iam_role.eks_node_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
}

resource "aws_iam_role_policy_attachment" "eks_cni_policy" {
  role       = aws_iam_role.eks_node_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
}

resource "aws_iam_role_policy_attachment" "ecr_read_only_policy_attachment" {
  role       = aws_iam_role.eks_node_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}


# VPC Creation for EKS Cluster
resource "aws_vpc" "my_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
}

# Public Subnet for EKS Cluster
resource "aws_subnet" "public_subnet_a" {
  vpc_id                  = aws_vpc.my_vpc.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "ap-southeast-2a"  # Adjust based on your region
}
resource "aws_subnet" "public_subnet_b" {
  vpc_id                  = aws_vpc.my_vpc.id
  cidr_block              = "10.0.2.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "ap-southeast-2b"  # Second AZ
}
# EKS Cluster creation
resource "aws_eks_cluster" "my_eks_cluster" {
  name     = "my-cluster"
  role_arn = aws_iam_role.eks_service_role.arn

  vpc_config {
    subnet_ids = [aws_subnet.public_subnet_a.id, aws_subnet.public_subnet_b.id]
  }

  tags = {
    Name = "my-eks-cluster"
  }
}

resource "aws_eks_node_group" "my_node_group" {
  cluster_name    = aws_eks_cluster.my_eks_cluster.name
  node_group_name = "my-node-group"
  node_role_arn   = aws_iam_role.eks_node_role.arn
  subnet_ids      = [aws_subnet.public_subnet_a.id, aws_subnet.public_subnet_b.id]

  scaling_config {
    desired_size = 2
    max_size     = 3
    min_size     = 2
  }
}

# Fetching the EKS Cluster and Authentication info for Kubernetes provider
data "aws_eks_cluster" "my_eks_cluster" {
  name = aws_eks_cluster.my_eks_cluster.name
  depends_on = [
    aws_eks_cluster.my_eks_cluster
  ]
}

data "aws_eks_cluster_auth" "my_eks_cluster_auth" {
  name = aws_eks_cluster.my_eks_cluster.name
  depends_on = [
    aws_eks_cluster.my_eks_cluster
  ]
}

# resource "kubernetes_manifest" "backend_deployment" {
#   manifest   = yamldecode(file("k8s_aws/backend-deployment.yaml"))
#   depends_on = [aws_eks_cluster.my_eks_cluster, aws_eks_node_group.my_node_group]
# }

# resource "kubernetes_manifest" "backend_service" {
#   manifest   = yamldecode(file("k8s_aws/backend-service.yaml"))
#   depends_on = [aws_eks_cluster.my_eks_cluster, aws_eks_node_group.my_node_group]
# }

# resource "kubernetes_manifest" "celery_deployment" {
#   manifest   = yamldecode(file("k8s_aws/celery-deployment.yaml"))
#   depends_on = [aws_eks_cluster.my_eks_cluster, aws_eks_node_group.my_node_group]
# }

# resource "kubernetes_manifest" "celery_scaler_role" {
#   manifest   = yamldecode(file("k8s_aws/celery-scaler-role.yaml"))
#   depends_on = [aws_eks_cluster.my_eks_cluster, aws_eks_node_group.my_node_group]
# }

# resource "kubernetes_manifest" "celery_scaler_rolebinding" {
#   manifest   = yamldecode(file("k8s_aws/celery-scaler-rolebinding.yaml"))
#   depends_on = [aws_eks_cluster.my_eks_cluster, aws_eks_node_group.my_node_group]
# }

# resource "kubernetes_manifest" "redis_deployment" {
#   manifest   = yamldecode(file("k8s_aws/redis-deployment.yaml"))
#   depends_on = [aws_eks_cluster.my_eks_cluster, aws_eks_node_group.my_node_group]
# }

# resource "kubernetes_manifest" "redis_service" {
#   manifest   = yamldecode(file("k8s_aws/redis-service.yaml"))
#   depends_on = [aws_eks_cluster.my_eks_cluster, aws_eks_node_group.my_node_group]
# }

# resource "kubernetes_manifest" "scale_celery_up_cronjob" {
#   manifest   = yamldecode(file("k8s_aws/scale-celery-up-cronjob.yaml"))
#   depends_on = [aws_eks_cluster.my_eks_cluster, aws_eks_node_group.my_node_group]
# }
