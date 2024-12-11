# resource "kubernetes_manifest" "backend_deployment" {
#   manifest   = yamldecode(file("k8s_aws/backend-deployment.yaml"))
#   depends_on = [aws_eks_cluster.my_eks_cluster, aws_eks_node_group.my_node_group]

#   field_manager {
#     name            = "terraform"
#     force_conflicts = true
#   }
# }

# resource "kubernetes_manifest" "backend_service" {
#   manifest   = yamldecode(file("k8s_aws/backend-service.yaml"))
#   depends_on = [aws_eks_cluster.my_eks_cluster, aws_eks_node_group.my_node_group]

#   field_manager {
#     name            = "terraform"
#     force_conflicts = true
#   }
# }

# resource "kubernetes_manifest" "celery_deployment" {
#   manifest   = yamldecode(file("k8s_aws/celery-deployment.yaml"))
#   depends_on = [aws_eks_cluster.my_eks_cluster, aws_eks_node_group.my_node_group]

#   field_manager {
#     name            = "terraform"
#     force_conflicts = true
#   }
# }

# resource "kubernetes_manifest" "celery_scaler_role" {
#   manifest   = yamldecode(file("k8s_aws/celery-scaler-role.yaml"))
#   depends_on = [aws_eks_cluster.my_eks_cluster, aws_eks_node_group.my_node_group]

#   field_manager {
#     name            = "terraform"
#     force_conflicts = true
#   }
# }

# resource "kubernetes_manifest" "celery_scaler_rolebinding" {
#   manifest   = yamldecode(file("k8s_aws/celery-scaler-rolebinding.yaml"))
#   depends_on = [aws_eks_cluster.my_eks_cluster, aws_eks_node_group.my_node_group]

#   field_manager {
#     name            = "terraform"
#     force_conflicts = true
#   }
# }

# resource "kubernetes_manifest" "redis_deployment" {
#   manifest   = yamldecode(file("k8s_aws/redis-deployment.yaml"))
#   depends_on = [aws_eks_cluster.my_eks_cluster, aws_eks_node_group.my_node_group]

#   field_manager {
#     name            = "terraform"
#     force_conflicts = true
#   }
# }

# resource "kubernetes_manifest" "redis_service" {
#   manifest   = yamldecode(file("k8s_aws/redis-service.yaml"))
#   depends_on = [aws_eks_cluster.my_eks_cluster, aws_eks_node_group.my_node_group]

#   field_manager {
#     name            = "terraform"
#     force_conflicts = true
#   }
# }

# resource "kubernetes_manifest" "scale_celery_up_cronjob" {
#   manifest   = yamldecode(file("k8s_aws/scale-celery-up-cronjob.yaml"))
#   depends_on = [aws_eks_cluster.my_eks_cluster, aws_eks_node_group.my_node_group]

#   field_manager {
#     name            = "terraform"
#     force_conflicts = true
#   }
# }
