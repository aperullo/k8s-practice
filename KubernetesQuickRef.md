## Definitions
**Pods**- The smallest K8s unit, runs one or more containers. Generally managed by higher level mechanisms.

**Nodes**- The physical or virtual machine running 1 or more pods.

**Deployments**- Deployments of pods. Manages the number of pods, takes requests to it and distributes them among the pods inside it. Can scale. 1 or more pods

**Service**- A loose coupling of some exposed endpoint (such as a port, or subdomain) to a bunch of pods (through a deployment).

## Baisc Commands
Start a local K8S cluster
```minikube start```

Create a deployment
```kubectl create deployment <deployment_name> --image=<image_name>```

### Inspecting Commands:
```kubectl <get|describe> <pods|services|deployments|services|secrets>```

Ex:
```
kubectl get pods
kubectl get services
kubectl get pods -o wide
kubectl get pods -o yaml
kubectl describe pods 
kubectl describe service
```

##### Inspect by label
Labels are key-value pairs that can be set in the .yaml files or manually. Not just pods can be labelled, so too can services, deployments, and most other resources.

Set them with:
```kubectl label pod <pod_name> app=v1```

View them with:
```kubectl describe pod <pod_name>```

View pods with specific labels:
```
kubectl get pods -l app=app-scale
kubectl get services,deployments -l tier=frontend
```

## Services
#### Expose a new service
```
kubectl expose deployment/<deployment-name> --type=<ClusterIP|NodePort|LoadBalancer|ExternalName>
kubectl expose deployment/kubernetes-bootcamp --type="NodePort" --port 8080
```
**ClusterIP**- Makes the services only visible within the k8s cluster. See Dictionary's app-dict-db-s in the .yaml for an example.

**NodePort**- Makes the service visible from outside the cluster at the specified port

**LoadBalancer**- Makes service visible, but using an external load balancer.

**ExternalName**- Maps the service to an external name like `foo.bar.example.com`

#### Test exposed port
get the nodeport from `kubectl get services -o wide` or use
```
export NODE_PORT=$(kubectl get services/app-secret-s -o go-template='{{(index .spec.ports 0).nodePort}}')
echo NODE_PORT=$NODE_PORT

curl $(minikube ip):$NODE_PORT```
```

#### Delete a service
```
kubectl delete service <service_name>
kubectl delete service -l run=kubernetes-bootcamp 
```
## Deployments

#### Scale a deployment
```kubectl scale deployments/kubernetes-bootcamp --replicas=4```

#### Update a deployment
```
kubectl set image deployments/<deployment_name> <deployment_name>=<image>:<version>
kubectl set image deployments/kubernetes-bootcamp kubernetes-bootcamp=jocatalin/kubernetes-bootcamp:v2
```

#### View update progress
```
kubectl describe deployments
kubectl rollout status deployments/app-scale
```

#### Rollback an update
```kubectl rollout undo deployments/app-scale```

## Debugging

#### To get bash in a container 
In a seperate terminal be running `kubectl proxy`. Then get the pod name either with `kubectl get pods -o wide`
```
export POD_NAME=$(kubectl get pods -o go-template --template '{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}')
kubectl exec -it $POD_NAME bin/sh
```

#### See env variables
```kubectl exec <pod_name> env```

## Local Images
First get the minikube docker env vars loaded in your terminal:
```eval $(minikube docker-env)```
Then you can build the image and verify its among minikube's images:
```
docker build -t <image_name:latest> .
docker images
```

## Secrets
#### Create secret from txt file.
```kubectl create secret generic user-pass --from-file=./secrets_files/username.txt --from-file=./secrets_files/password.txt```

#### Create secret from yaml file. See secret_file.yaml for syntax. Secret must be encoded in base64
```kubectl create -f secret_file.yaml```

#### To decode secret
```kubectl get secrets -o yaml```
//take value from data section
```echo "<base64_secret>" | base64 --decode```
