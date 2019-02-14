# Secrets

Testing out kubernetes secrets.

## How to use this
You need to get the app_secret image into your minikube's docker image repo.

##### Steps

Acquire environment vars for minikube: 
```
eval $(minikube docker-env)
```
From the `app_src` directory: 
```
> python3 -m venv venv
> . venv/bin/activate
> pip install Flask
> docker build -t app_secret .
> deactivate
```
`cd ..` then choose which secret type you want to use:

For secrets from files:
```
kubectl create -f app_secrets.yaml
```

For secrets through env variables:
```
kubectl create -f app_secrets_env.yaml
```

Verify it worked by finding the container with:
```
> kubectl get pods
NAME                              READY   STATUS    RESTARTS   AGE
app-secret-d-6cbc47f55c-hfjsx     1/1     Running   0          21m
```
For secrets from files:
```
> kubectl exec -it app-secret-d-6cbc47f55c-hfjsx bin/sh
/ # cd etc/secret_dir 
/ # ls
password  username
/ # cat username password
usernamevalue
passwordvalue
```
For secrets through env variables:
```
> kcl exec -it app-secret-d-6cbc47f55c-hfjsx bin/sh
/ # env
USERNAME=usernamevalue
PASSWORD=passwordvalue
```

## Learned things

Create a secret by command. Automatically base64 encodes them:
```
kubectl create secret generic user-pass --from-file=./secrets_files/username.txt --from-file=./secrets_files/password.txt
```

Create a secret from yaml. Have to manually base64 encode. See `secret_file.yaml`.

Decode a secret:
```
> kubectl get secrets -o yaml 
> echo "BASE64SECRET" | base64 --decode
