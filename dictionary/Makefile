.DEFAULT_GOAL := all

# build based environment vars
APP_SRC=./app_src
SRC_SECRET_DIR=./app_src/secret_dir
K8S_BUILD_DIR=./target


# yaml substituted environment vars
DB_IMAGE_NAME=dict-db
QUERYER_IMAGE_NAME=dict-queryer
SECRET_DIR=/etc/secret_dir
DICT_LOC=/dict_data/dictionary.json
LOGIN=""
PASSW=""
# based on the default name of the service
DB_SERVICE_NAME=APP_DICT_DB_S_SERVICE_HOST
DB_SERVICE_PORT=APP_DICT_DB_S_SERVICE_PORT


.PHONY: build-db
build-db:
	@eval $$(minikube docker-env); \
	cd $(APP_SRC)/dict_db && \
	pwd && \
	docker build -t ${DB_IMAGE_NAME} -f Dockerfile . && \
	cd - && \
	mkdir -p $(K8S_BUILD_DIR) && \
	docker save ${DB_IMAGE_NAME} -o $(K8S_BUILD_DIR)/${DB_IMAGE_NAME}.tar.gz 

.PHONY: build-queryer
build-queryer:
	@eval $$(minikube docker-env); \
	cd $(APP_SRC)/dict_queryer && \
	pwd && \
	docker build -t ${QUERYER_IMAGE_NAME} -f Dockerfile . && \
	cd - && \
	mkdir -p $(K8S_BUILD_DIR) && \
	docker save ${QUERYER_IMAGE_NAME} -o $(K8S_BUILD_DIR)/${QUERYER_IMAGE_NAME}.tar.gz
	
.PHONY: envsub
envsub:
	mkdir -p $(K8S_BUILD_DIR) && \
	export SECRET_DIR=${SECRET_DIR} && \
	export DICT_LOC=${DICT_LOC} && \
	export DB_SERVICE_NAME=${DB_SERVICE_NAME} && \
	export DB_SERVICE_PORT=${DB_SERVICE_PORT} && \
	export DB_IMAGE_NAME=${DB_IMAGE_NAME} && \
	export QUERYER_IMAGE_NAME=${QUERYER_IMAGE_NAME} && \
	envsubst < $(APP_SRC)/app-dict.yaml > $(K8S_BUILD_DIR)/app-dict.yaml

.PHONY: instructions
instructions:
	mkdir -p $(K8S_BUILD_DIR)
	cp 

all: clean build-db build-queryer envsub


.PHONY: clean
clean:
	rm -rf $(K8S_BUILD_DIR)
	

