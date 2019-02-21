# Scaling

Testing out kubernetes replica scaling when a container shuts down or is upgraded.

## How to use this
You need to get the app-scale image into your minikube's docker image repo.

##### Steps

Acquire environment vars for minikube: 
```
eval $(minikube docker-env)
```
From the `app_src` directory: 
```
> docker build -t app-scale .
```
``cd ..` then start the deployment and service:

```
kubectl create -f app_scale.yaml
```

Verify it worked by finding the pod/pods with:
```
> kubectl get pods
NAME                              READY   STATUS    RESTARTS   AGE
app-scale-d-6cbc47f55c-hfjsx     1/1     Running   0          21m
```

You can also view the id's of the pods with:
```
> curl "http://$(minikube ip):31110/id 
```

everytime a pod dies and respawns it will have a different id.

To kill a pod do:
```
> curl "http://$(minikube ip):31110/killme 
```

In a seperate terminal, if you want to see the db pods dying and respawning as they are killed, do:
```
> watch -n 0.1 "kubectl get pods -o wide"
```

To manually scale the deployment:
```
kubectl scale deployment app-scale-d --replicas=7
```

## Learned things

Deployment states are automatically managed. If the desired state and actual states differ, the deployment will start raising or bringing down pods as necessary. This is good in the event a pod fails, another replaces it. 

Deployments can be used to rollout updates whil keeping the service up; it will reduce the old image pods over time and replace them with new image ones. 

