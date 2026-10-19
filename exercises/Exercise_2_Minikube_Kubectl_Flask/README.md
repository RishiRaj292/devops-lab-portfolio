# Exercise 2 — Deploy Flask on Minikube using kubectl and YAML

## Objective
Build a small Flask web application, package it as a Docker image, deploy it to Minikube with a Kubernetes Deployment, expose it with a NodePort Service, and verify the HTTP response.

Expected response:
`Hello from Flask on Kubernetes!`

## Files
- `app.py` — Flask app listening on `0.0.0.0:15000`.
- `Dockerfile` — builds the `flask-app:latest` image.
- `k8s/flask-deployment.yaml` — Deployment and NodePort Service.
- `screenshots/README.txt` — instructions for adding genuine runtime evidence.

## Run on Windows PowerShell

Ensure Docker Desktop is running and Minikube is available:

```powershell
minikube status
kubectl get nodes
```

Build the image and load it into Minikube's node image store:

```powershell
docker build -t flask-app:latest .
minikube image load flask-app:latest
```

Apply Kubernetes resources:

```powershell
kubectl apply -f k8s/flask-deployment.yaml
kubectl rollout status deployment/flask-app
kubectl get deployments
kubectl get pods -l app=flask-app
kubectl get services flask-app-service
```

Wait until the Pod is `1/1 Running`.

Expose a local URL:

```powershell
minikube service flask-app-service --url
```

Keep that terminal open while using the URL it prints. In a second PowerShell window, replace `<URL>` below with the actual URL (for example, `http://127.0.0.1:36157`):

```powershell
Invoke-RestMethod <URL>
```

Expected response:

```text
Hello from Flask on Kubernetes!
```

You can also open the printed URL in a browser and take a screenshot showing the actual response.

## Important notes
- The original exercise uses `eval $(minikube docker-env)`, which is a Bash command and is not suitable for ordinary Windows PowerShell. This README uses `minikube image load` instead.
- `imagePullPolicy: Never` requires the image to exist in Minikube's node image store.
- `containerPort` documents the container's listening port; the Service makes the application reachable through Kubernetes networking.
- The `port` is the Service port; `targetPort` is the container port.
- A Minikube URL may be temporary and may require the terminal to stay open on Windows with the Docker driver.

## Troubleshooting

### ImagePullBackOff / ErrImageNeverPull
Run:

```powershell
docker images flask-app
minikube image ls
minikube image load flask-app:latest
kubectl describe pod -l app=flask-app
```

### Pod is not Running
Run:

```powershell
kubectl get pods -l app=flask-app
kubectl describe pod -l app=flask-app
kubectl logs deployment/flask-app
```

### Cannot access URL
Keep the terminal running after `minikube service flask-app-service --url` and use the exact URL it prints.

## Cleanup (optional)
Only after saving your evidence:

```powershell
kubectl delete -f k8s/flask-deployment.yaml
```

## Result checklist
- [ ] Docker image built successfully.
- [ ] Image loaded into Minikube.
- [ ] Deployment has 1/1 available replica.
- [ ] Flask Pod is `1/1 Running`.
- [ ] NodePort Service exists.
- [ ] Actual HTTP response verified.
- [ ] Genuine screenshot saved in `screenshots/`.
