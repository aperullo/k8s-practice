# K8S Learning

A repo of the various mini projects I've used to help learn how to use kubernetes.
The Kubernetes quick reference is the main product of this repo.

## Projects
- **ConfigMaps** - Shows an example on how to use config maps to load settings either by file or environment variable.
- **Secrets** - Shows an example of how to create and pass secrets to containers through volumes.

- **Scaling** - Shows an example of how to scale the number of nodes in a deployment, and the behavior of K8S restarting nodes when they fail.
- **Dictionary** - An app that gives definitions of words through an exposed restful api. Combines the concepts of the previous 3, plus inter-pod communication via an internally visible service.

## Instructions
Go inside the folders of the mini projects for instructions on how to run them.
In general it will be: 
```
minikube start
kubectl create -f <app_name>.yaml
```

