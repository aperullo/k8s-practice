
# Config Maps

Testing out kubernetes config maps

## How to use this
You need to get the env-app image into your minikube's docker image repo.

##### Steps

Acquire environment vars for minikube: 
```
> minkube start
> eval $(minikube docker-env)
```
From the directory with the dockerfile directory: 
```
> docker build -t doc_env_app .
> kubectl create -f env_app.yaml
```

Verify it worked by finding the container with:
```
> kubectl get pods
NAME                              READY   STATUS    RESTARTS   AGE
env-app-d-6cbc47f55c-hfjsx     1/1     Running   0          21m
```

To ping it and try the env variable:
```> curl $(minikube ip):31110/listenv```

To delete it:
```> kubectl delete services,deployment,configmaps -l app=env-app```
