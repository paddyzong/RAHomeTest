resource "kubernetes_deployment" "backend" {
  depends_on = [aws_eks_cluster.my_eks_cluster, aws_eks_node_group.my_node_group]
  metadata {
    name      = "backend"
    namespace = "default"
    labels = {
      "io.kompose.service" = "backend"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        "io.kompose.service" = "backend"
      }
    }

    strategy {
      type = "Recreate"
    }

    template {
      metadata {
        labels = {
          "io.kompose.service" = "backend"
        }
      }

      spec {
        container {
          name  = "backend"
          image = "public.ecr.aws/y2c8v6k4/paddy/backend:latest"

          port {
            container_port = 8000
            protocol      = "TCP"
          }

          env {
            name  = "PYTHONUNBUFFERED"
            value = "1"
          }

          env {
            name  = "REDIS_HOST"
            value = "redis"
          }

          env {
            name  = "REDIS_PORT"
            value = "6379"
          }

          volume_mount {
            name       = "app-data"
            mount_path = "/app/media"
          }

          command = ["gunicorn"]
          args    = ["--bind", "0.0.0.0:8000", "--log-level", "debug", "RATypeInfer.wsgi"]
        }

        volume {
          name = "app-data"
          host_path {
            path = "/app/media"
            type = "DirectoryOrCreate"
          }
        }

        restart_policy = "Always"
      }
    }
  }
}

resource "kubernetes_service" "backend" {
  depends_on = [aws_eks_cluster.my_eks_cluster, aws_eks_node_group.my_node_group]

  metadata {
    name      = "backend"
    namespace = "default"
    
    labels = {
      "io.kompose.service" = "backend"
    }
    
    annotations = {
      "service.beta.kubernetes.io/aws-load-balancer-type"     = "alb"
      "service.beta.kubernetes.io/aws-load-balancer-ssl-cert" = aws_acm_certificate.ra_certificate.arn
      "service.beta.kubernetes.io/aws-load-balancer-ssl-ports" = "443"
    }
  }

  spec {
    type = "LoadBalancer"
    
    port {
      name        = "8000"
      port        = 8000
      target_port = 8000
    }
    
    port {
      name        = "https"
      port        = 443
      target_port = 8000
      protocol    = "TCP"
    }

    selector = {
      "io.kompose.service" = "backend"
    }
  }
}

resource "kubernetes_deployment" "celery" {
  depends_on = [aws_eks_cluster.my_eks_cluster, aws_eks_node_group.my_node_group]

  metadata {
    name      = "celery"
    namespace = "default"
    labels = {
      "io.kompose.service" = "celery"
    }
  }

  spec {
    replicas = 2

    selector {
      match_labels = {
        "io.kompose.service" = "celery"
      }
    }

    strategy {
      type = "Recreate"
    }

    template {
      metadata {
        labels = {
          "io.kompose.service" = "celery"
        }
      }

      spec {
        container {
          name  = "celery"
          image = "public.ecr.aws/y2c8v6k4/paddy/backend:latest"

          args = [
            "celery",
            "-A",
            "RATypeInfer",
            "worker",
            "--loglevel=info"
          ]

          env {
            name  = "PYTHONUNBUFFERED"
            value = "1"
          }

          env {
            name  = "REDIS_HOST"
            value = "redis"
          }

          env {
            name  = "REDIS_PORT"
            value = "6379"
          }

          volume_mount {
            name       = "app-data"
            mount_path = "/app/media"
          }
        }

        volume {
          name = "app-data"
          host_path {
            path = "/app/media"
            type = "DirectoryOrCreate"
          }
        }

        restart_policy = "Always"
      }
    }
  }
}

resource "kubernetes_role" "celery_scaler" {
  depends_on = [aws_eks_cluster.my_eks_cluster, aws_eks_node_group.my_node_group]

  metadata {
    name      = "celery-scaler"
    namespace = "default"
  }

  rule {
    api_groups = ["apps"]
    resources  = ["deployments"]
    verbs      = ["get", "list", "update", "patch"]
  }

  rule {
    api_groups = ["apps"]
    resources  = ["deployments/scale"]
    verbs      = ["get", "update", "patch"]
  }
}

resource "kubernetes_role_binding" "celery_scaler_binding" {
  depends_on = [aws_eks_cluster.my_eks_cluster, aws_eks_node_group.my_node_group]

  metadata {
    name      = "celery-scaler-binding"
    namespace = "default"
  }

  role_ref {
    api_group = "rbac.authorization.k8s.io"
    kind      = "Role"
    name      = "celery-scaler"
  }

  subject {
    kind      = "ServiceAccount"
    name      = "default"
    namespace = "default"
  }
}

resource "kubernetes_deployment" "redis" {
  depends_on = [aws_eks_cluster.my_eks_cluster, aws_eks_node_group.my_node_group]

  metadata {
    name      = "redis"
    namespace = "default"
    labels = {
      "io.kompose.service" = "redis"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        "io.kompose.service" = "redis"
      }
    }

    template {
      metadata {
        labels = {
          "io.kompose.service" = "redis"
        }
      }

      spec {
        container {
          name  = "redis-broker"
          image = "redis:latest"

          port {
            container_port = 6379
            protocol      = "TCP"
          }
        }

        restart_policy = "Always"
      }
    }
  }
}

resource "kubernetes_service" "redis" {
  depends_on = [aws_eks_cluster.my_eks_cluster, aws_eks_node_group.my_node_group]

  metadata {
    name      = "redis"
    namespace = "default"
    labels = {
      "io.kompose.service" = "redis"
    }
  }

  spec {
    port {
      name        = "6379"
      port        = 6379
      target_port = 6379
    }

    selector = {
      "io.kompose.service" = "redis"
    }
  }
}


resource "kubernetes_manifest" "scale_celery_up_cronjob" {
  manifest = {
    apiVersion = "batch/v1"
    kind       = "CronJob"
    metadata = {
      name      = "scale-celery-up"
      namespace = "default"
    }
    spec = {
      schedule = "10 23 * * *"
      jobTemplate = {
        spec = {
          template = {
            spec = {
              containers = [
                {
                  name  = "scale-celery"
                  image = "bitnami/kubectl:latest"
                  command = [
                    "/bin/sh",
                    "-c",
                    "kubectl scale deployment celery --replicas=4 -n default"
                  ]
                }
              ]
              restartPolicy = "OnFailure"
            }
          }
        }
      }
    }
  }
}

data "kubernetes_service" "backend_service" {
  metadata {
    name      = "backend"
    namespace = "default"
  }
}

resource "aws_route53_record" "backend_cname" {
  zone_id = "Z0787172Q9SOK5I6GQH9"
  name    = "api.rahometest.click"
  type    = "CNAME"
  ttl     = 300

  records = [
    data.kubernetes_service.backend_service.status[0].load_balancer[0].ingress[0].hostname
  ]
}
