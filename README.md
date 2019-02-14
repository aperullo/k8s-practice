A repo of the various mini projects I've used to help learn how to use kubernetes.

To run this use:
minikube start
kubectl create -f env_app.yaml

To ping it and try the env variable:
curl $(minikube ip):31110/listenv

