resource_group_name = "rg-devops-acr"
location            = "East US"
acr_name            = "acrdevops1629085875" # ✅ use your existing ACR name
aks_cluster_name    = "aks-devops-cluster"
dns_prefix          = "aksdevops"
node_count          = 2
vm_size             = "Standard_D2_v2"

tags = {
  Environment = "Development"
  Project     = "DevOps-Demo"
  ManagedBy   = "Terraform"
  Owner       = "SheronXalxo"
}
