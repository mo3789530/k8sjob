from logging import getLogger
import logging
from k8sClient import k8sClient
from flask import Flask,request
import os

app = Flask(__name__)

logger = getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@app.route("/")
def root():
    return {"message": "Hello World"}, 200

@app.route("/api/health")
def health():
    return {"message": "Hello World"}, 200

@app.route("/api/deployment/restart/all", methods=['POST'])
def restart_all():
    namespace = request.get_json()["namespace"]
    try:
        k8s = k8sClient()
        is_cluster =- bool(os.environ.get("IsCluster",False))
        k8s.get_k8s_config(is_cluster=is_cluster)
        k8s.restart_deployment_all(namespace=namespace)
    except Exception as e:
        logger.error(e)
        return {"error": str(e)}, 400
    return request.get_data(), 200

@app.route("/api/deployment/restart", methods=['POST'])
def restart():
    namespace = request.get_json()["namespace"]
    name = request.get_json()["name"]
    try:
        k8s = k8sClient()
        is_cluster =- bool(os.environ.get("IsCluster",False))
        k8s.get_k8s_config(is_cluster=is_cluster)
        k8s.restart_deployment(namespace=namespace, name=name)
    except Exception as e:
        logger.error(e)
        return {"error": str(e)}, 400
    return request.get_data(), 200

if __name__ == "__main__":
    production = bool(os.environ.get("Production",True))
    app.run(debug=production, host='0.0.0.0')