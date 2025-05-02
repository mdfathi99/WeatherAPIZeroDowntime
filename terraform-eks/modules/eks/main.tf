module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = var.cluster_name
  cluster_version = "1.28"
  subnet_ids      = module.vpc.private_subnets
  vpc_id          = module.vpc.vpc_id

  node_groups = {
    default = {
      desired_capacity = 2
      max_capacity     = 3
      min_capacity     = 1

      instance_types = [var.node_instance_type]
    }
  }

  manage_aws_auth = true
}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  name    = "weather-api-vpc"
  cidr    = "10.0.0.0/16"
  azs     = ["eu-central-1a", "eu-central-1b", "eu-central-1c"]

  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = true
}
