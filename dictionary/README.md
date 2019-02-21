# Secrets

An app integrating a bunch of things I've learned into one project. A dictionary definition fetcher.
User puts a word in query parameter and gets definition back.

It has an exposed service that talks to some query pods. The queryers know of an internal service through their environment variables. This internal service talks to the DB pods which have the dictionary. These DB pods have a high chance of dying before completing the request. The query pods will retry the request, the service should direct to one of the pods that are still responding. The query pod will try up to 5 times before declaring the request a failure. 

Makefile:
TODO: should load the secrets from file and put them through kcl create secrets.
TODO: delete secret_dir

## How to use this
You need to get the images into your minikube's docker image repo.

##### Steps

```
> make

> kubectl create -f target/app-dict.yaml

> curl $(minikube ip):31100/define/word

> kubectl delete services,deployment,secrets,configmaps -l app=app-dict

```

## Learned things

Kubernetes pods get environment variables related to the available services they can see.
The names are based on the name of the service, such as:
```APP_DICT_DB_S_SERVICE_HOST
APP_DICT_DB_S_SERVICE_Port```