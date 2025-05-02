module "eks" {
  source           = "./modules/eks"
  cluster_name     = var.cluster_name
  region           = var.region
  node_instance_type = var.node_instance_type
}
