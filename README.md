# memlookup

## Overview
Produce a program capable of storing and retrieving items of data from a lookup table stored in
memory. The lookup table should be located on a remote machine and accessed over a network
connection. For simplicity, it can be assumed the data is indexed by a string and that the payload
(value) is also a string.
The server program should expose a network service, and the client program should be able to
communicate with the server to access data. For example, it should be possible to run the server
program on a machine as follows:

- Runs the server
$ ./server

On the same machine (or a second machine), it should be possible to store items of data and
retrieve them using a second “client” program. The interface should look roughly as follows:

- Stores a value against a specific key in the server located at "node".
$ ./client <node> set <key> <value>

- Retrieves a value for a specific key and prints it, if found.
$ ./client <node> get <key>
<value>
Below is an example of what should be expected to work. In this example, the server is being used to
store the names of capital cities for a country.

$ ./client 127.0.0.1 set norway oslo
$ ./client 127.0.0.1 set denmark copenhagen
$ ./client 127.0.0.1 get norway
oslo
$ ./client 127.0.0.1 get sweden
error: not found
Submission
Submit the following files:
A single .zip or .tar.gz file with the source code for your "server" and "client" program.

## How to run?
The code provided here can be executed in three ways:

1. **Through local Python**: install Python3.9 in your system; install requirements (`pip install -r requirements.txt`); define `SERVER_DATA_DIR` environment variable; run server (`uvicorn main:app --host 0.0.0.0 --port 8080`) and execute client (Check `python client.py --help` for options)
2. **Through Docker**: install docker in your system; build image (`sudo docker build -t server .`); run container (`sudo docker run server`); execute client
3. **Deployed on [Kind](https://kind.sigs.k8s.io/)**: [follow instructions bellow](#how-to-deploy-on-Kind?)


## How to deploy on Kind?

### Building image on local registry

[Docker Hub](https://hub.docker.com/) is the premier Image Repository with thousands of Official Images ready for use. However, some Docker Images are not meant to be used outside local firewall. In order to deploy our application on Kind, we will first need to push the server image to local registry:

1. **Run local version of the Distribution project**: `sudo docker run -d -p 5000:5000 --restart=always --name registry registry:2`
2. **Build server image**: `sudo docker build -t localhost:5000/server:2.0 .`
3. **Push image to local registry**: `sudo docker push localhost:5000/server:2.0`

### Setup cluster and its objects

Kubernetes in Docker (kind) is a tool for running Kubernetes clusters locally using Docker containers as Kubernetes nodes. Kind was originally developed to create virtualized “Kubernetes-in-Kubernetes” clusters to use in Kubernetes Continuous Integration (CI) testing. Rather than relying on a pre-configured Kubernetes cluster and pre-installed clients, this step proposes a method for bundling kind and kubectl:

1. **Create cluster based on configuration file**: `sudo kind create cluster --config cluster.yaml`
2. **Load server image into cluster**: `sudo kind load docker-image localhost:5000/server:2.0 --name kind`
3. **Install Metrics Server for scaling capabilities**: `kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml`
4. **Allow unsafe environment for testing purposes**: `kube-system metrics-server --type "json" -p '[{"op": "add", "path": "/spec/template/spec/containers/0/args/-", "value": --kubelet-insecure-tls}]'`
5. **Configure Kind to interact with NGINX as an Ingress Controller**: `kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml`
6. **Wait until Ingress setup is over**: `kubectl wait --namespace ingress-nginx \  --for=condition=ready pod --selector=app.kubernetes.io/component=controller --timeout=90s`
7. **Create Deployment, Service and Volumes**: `kubectl apply -f server-deployment.yaml`

**All steps above in one command**:  `sudo kind create cluster --config cluster.yaml && sudo kind load docker-image localhost:5000/server:2.0 --name kind && kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml && kubectl patch deployment -n kube-system metrics-server --type "json" -p '[{"op": "add", "path": "/spec/template/spec/containers/0/args/-", "value": --kubelet-insecure-tls}]' && kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml && kubectl wait --namespace ingress-nginx --for=condition=ready pod --selector=app.kubernetes.io/component=controller --timeout=90s && kubectl apply -f server-deployment.yaml`
  
