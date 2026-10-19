# Exercise 1 — Kubernetes: Hello Pod

## Objective
Deploy Nginx in a Kubernetes Pod, expose it with a NodePort Service, and verify it in a browser.

## Environment used
- Windows 11 + PowerShell
- Docker Desktop using the `desktop-linux` context and WSL2
- Minikube v1.38.1
- Kubernetes v1.35.1
- kubectl client v1.30.2

> Note: the kubectl client is older than the Kubernetes cluster. The exercise succeeded, but if commands behave unexpectedly, use `minikube kubectl -- <command>` or install a kubectl client closer to the cluster version.

## Files
- `manifests/hello-pod.yaml` — Pod manifest for Nginx.
- `manifests/hello-service.yaml` — NodePort Service manifest.
- `screenshots/nginx-welcome.png` — browser evidence captured after deployment.
- `docs/Exercise_1_Kubernetes_Hello_Pod_Revision.pdf` — revision notes.
- `docs/Exercise_1_Kubernetes_Hello_Pod_Revision.docx` — editable revision notes.

## Run the exercise

Start Docker Desktop and wait until its Linux engine is running. Then run in PowerShell:

```powershell
minikube start --driver=docker
kubectl get nodes
kubectl apply -f manifests/hello-pod.yaml
kubectl get pods
kubectl apply -f manifests/hello-service.yaml
kubectl get services
minikube service hello-k8s
```

Expected:
- `kubectl get nodes` shows the `minikube` node as `Ready`.
- Pod `hello-k8s` reaches `1/1 Running`.
- Service `hello-k8s` is of type `NodePort`.
- Browser displays **Welcome to nginx!**

On Windows with the Docker driver, Minikube may create a local tunnel URL such as `http://127.0.0.1:<port>`. Keep the PowerShell terminal running while using that URL.

## Original command-based method used successfully

These were the commands used during the successful run:

```powershell
kubectl run hello-k8s --image=nginx --port=80
kubectl get pods
kubectl expose pod hello-k8s --type=NodePort --port=80
kubectl get services
minikube service hello-k8s
```

Observed service mapping in this run: `80:31768/TCP`. Cluster IPs and NodePorts may differ on another run.

## Cleanup (optional)

Run only after you have finished your demonstration and saved evidence:

```powershell
kubectl delete service hello-k8s
kubectl delete pod hello-k8s
```

## Result
**Completed successfully:** the Pod reached `Running`, the NodePort Service was created, and the Nginx welcome page was visible in the browser.
