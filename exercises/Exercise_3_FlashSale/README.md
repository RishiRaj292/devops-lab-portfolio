# Exercise 3: Scaling a Flask Flash-Sale App with ReplicaSets

## Objective
Use a Kubernetes ReplicaSet to run a Flask flash-sale service, scale from 3 to 5 Pods, delete a Pod and observe automatic replacement, and inspect where Pods run.

## Files
- `app.py` — Flask endpoints `/`, `/buy`, and `/health`. Responses include the serving Pod hostname.
- `Dockerfile` — Python 3.11 slim image running the app with Gunicorn on port 5000.
- `flashsale-replicaset.yaml` — ReplicaSet (initially 3 replicas) and ClusterIP Service.

## Prerequisites
Docker Desktop must be running, with `kubectl` and Minikube installed. These commands use Windows PowerShell and the existing Minikube profile. They do **not** delete or recreate your cluster.

## 1. Start/check Minikube

```powershell
minikube status
kubectl get nodes
```

If Minikube is stopped, start it with `minikube start`. Do not run `minikube delete` unless you intentionally want to remove the existing cluster.

## 2. Build the image for Minikube

Run these commands from the folder containing this README, `app.py`, and `Dockerfile`:

```powershell
minikube image build -t flashsale:1.0 .
minikube image ls | Select-String flashsale
```

The image is built into Minikube's image store, so this local lab does not require a Docker Hub account or a public image push.

## 3. Apply the ReplicaSet and Service

```powershell
kubectl apply -f .\flashsale-replicaset.yaml
kubectl get rs flashsale-rs
kubectl get pods -l app=flashsale -o wide
kubectl get service flashsale-svc
```

Initially, the ReplicaSet should show 3 desired replicas and, once the Pods are ready, 3 ready Pods.

## 4. Scale from 3 to 5 replicas

```powershell
kubectl scale rs flashsale-rs --replicas=5
kubectl get rs flashsale-rs
kubectl get pods -l app=flashsale -o wide
```

Wait until all 5 Pods are `Running` and `READY` is `1/1`. If needed, watch progress with `kubectl get pods -l app=flashsale -w` and press Ctrl+C to stop watching.

## 5. Test the service and endpoints

In one PowerShell window, start port forwarding and leave it running:

```powershell
kubectl port-forward service/flashsale-svc 8080:80
```

In a second PowerShell window, call the endpoints:

```powershell
Invoke-RestMethod http://127.0.0.1:8080/
Invoke-RestMethod 'http://127.0.0.1:8080/buy?user=123'
Invoke-RestMethod http://127.0.0.1:8080/health
```

Repeat the `/` or `/buy` request several times. The `pod` or `served_by_pod` field identifies the Pod that served each request. Because this is a small local cluster, repeated requests are not guaranteed to show every Pod immediately; Service routing is not a strict round-robin guarantee.

## 6. Demonstrate ReplicaSet self-healing

List Pods and choose one name whose prefix is `flashsale-rs-`:

```powershell
kubectl get pods -l app=flashsale
kubectl delete pod <replace-with-one-flashsale-pod-name>
kubectl get pods -l app=flashsale -w
```

The deleted Pod should be replaced so the ReplicaSet returns to 5 desired Pods. Press Ctrl+C to stop watching, then verify:

```powershell
kubectl get rs flashsale-rs
kubectl get pods -l app=flashsale -o wide
kubectl describe rs flashsale-rs
```

## Lab questions and answers

1. **What is the initial number of replicas?** 3.
2. **How many Pods should run after applying the initial configuration?** 3, once they become ready.
3. **What happens when the ReplicaSet is scaled to 5?** Kubernetes creates two additional Pods and reconciles the desired count to five.
4. **What happens when one Pod is deleted?** The ReplicaSet controller creates a replacement Pod to return to the desired count of five.
5. **How does Kubernetes maintain the desired number of replicas?** The controller continuously compares the actual matching Pods with the desired replica count and creates or removes Pods as needed.
6. **How many nodes are running?** For the exercise's single-node Minikube setup, one node. Verify with `kubectl get nodes`.
7. **Where do the five Pods run?** In a single-node cluster, all five run on that node. Verify the `NODE` column using `kubectl get pods -l app=flashsale -o wide`.

## Troubleshooting

- **Pods show `ImagePullBackOff` or `ErrImagePull`:** confirm Minikube's image list contains `flashsale:1.0`, then rebuild with `minikube image build -t flashsale:1.0 .`.
- **Pods are not ready:** inspect `kubectl describe pod <pod-name>` and `kubectl logs <pod-name>`.
- **Port 8080 is already in use:** choose another local port, for example `kubectl port-forward service/flashsale-svc 8081:80`, then use `http://127.0.0.1:8081/`.
- **Cleanup this exercise's resources only:** `kubectl delete -f .\flashsale-replicaset.yaml`. This does not delete the Minikube cluster.

## Submission checklist

- [ ] `app.py`, `Dockerfile`, and `flashsale-replicaset.yaml` are included.
- [ ] The app image was built and the ReplicaSet initially ran 3 Pods.
- [ ] The ReplicaSet was scaled to 5 Pods.
- [ ] A deleted Pod was replaced.
- [ ] The endpoints and Pod distribution were checked using actual terminal output.
- [ ] Add your own genuine screenshots if your instructor asks for them. No screenshots are fabricated or included in this ZIP.
