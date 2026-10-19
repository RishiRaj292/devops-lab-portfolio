# Exercise 10 — Multi-Node Minikube with Multiple Applications

Deploys Product Catalog (2 replicas) and Shopping Cart (3 replicas), with required pod anti-affinity so each application's replicas land on separate nodes.

## 1. Create a separate three-node profile

This avoids deleting the existing `minikube` profile from earlier exercises:

```powershell
minikube start --nodes 3 -p devops-multinode --driver=docker
minikube -p devops-multinode addons enable registry
```

## 2. Build and load images

From the repository root:

```powershell
docker build -t product-catalog:latest -f exercises/10-minikube-multinode-multi-app/Dockerfile.product exercises/10-minikube-multinode-multi-app
docker build -t shopping-cart:latest -f exercises/10-minikube-multinode-multi-app/Dockerfile.shopping exercises/10-minikube-multinode-multi-app
minikube -p devops-multinode image load product-catalog:latest
minikube -p devops-multinode image load shopping-cart:latest
```

## 3. Deploy and check distribution

```powershell
kubectl --context=devops-multinode apply -f exercises/10-minikube-multinode-multi-app/product_catalog_deployment.yaml
kubectl --context=devops-multinode apply -f exercises/10-minikube-multinode-multi-app/shopping_cart_deployment.yaml
kubectl --context=devops-multinode apply -f exercises/10-minikube-multinode-multi-app/product_catalog_service.yaml
kubectl --context=devops-multinode apply -f exercises/10-minikube-multinode-multi-app/shopping_cart_service.yaml
kubectl --context=devops-multinode get pods -o wide
kubectl --context=devops-multinode get services
```

## 4. Access and test the services

Run each in its own PowerShell window and keep it open:

```powershell
minikube -p devops-multinode service product-catalog-service --url
```

```powershell
minikube -p devops-multinode service shopping-cart-service --url
```

Use the returned localhost URLs (replace `<PRODUCT_URL>` and `<CART_URL>` below):

```powershell
Invoke-RestMethod <PRODUCT_URL>/products
Invoke-RestMethod <CART_URL>/cart
Invoke-RestMethod -Method Post -Uri <CART_URL>/cart -ContentType 'application/json' -Body '{"id":1,"name":"Laptop","quantity":1}'
```

The source manual placed Shopping Cart in a `devops-exercise` namespace without creating that namespace, while its Service was in `default`. Both Shopping Cart resources are set to `default` here so the provided apply commands work consistently.
