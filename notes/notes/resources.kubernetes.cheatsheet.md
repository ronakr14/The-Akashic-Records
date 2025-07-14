---
id: yp339s4hw4zwc42083rq2pl
title: Cheatsheet
desc: ''
updated: 1752473067116
created: 1752473066489
---

## 🧾 Cheat Sheets

* **kubectl Core**:

```bash
kubectl get pods
kubectl logs pod-name
kubectl exec -it pod-name -- bash
kubectl apply -f deployment.yaml
kubectl delete -f deployment.yaml
```

* **Minimal Deployment YAML**:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
        - name: my-container
          image: my-image:latest
          ports:
            - containerPort: 8080
```

* **Service YAML**:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  selector:
    app: my-app
  ports:
    - port: 80
      targetPort: 8080
  type: LoadBalancer
```

* **Horizontal Pod Autoscaler (HPA)**:

```bash
kubectl autoscale deployment my-app --cpu-percent=50 --min=2 --max=10
```
