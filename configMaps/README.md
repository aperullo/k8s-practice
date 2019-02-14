//To run this use:
minikube start
kubectl create -f env_app.yaml

//To ping it and try the env variable:
curl $(minikube ip):31110/listenv

//To stop it:
kcl delete deployments,services,configmaps -l app=env-app
