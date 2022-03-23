from kubernetes import client, config
import datetime
import pytz

class k8sClient():
    def get_config(isIncluster):
        if isIncluster == true:
            # https://github.com/kubernetes-client/python/blob/master/examples/in_cluster_config.py
            return config.load_incluster_config()
        else:
            # https://github.com/kubernetes-client/python/blob/master/examples/out_of_cluster_config.py
            return config.load_kube_config()

    def get_pods_status(config, namespace):
        k8s_core = client.CoreV1Api()
        pods = k8s_core.list_namespaced_pod('default')
        k8s_core.read_namespaced_pod_status('default')
        k8s_core.read_namespace_status('default')
        for item in pods.items:
            print(item.matadata.name)
            container_statuses = item.status.container_statuses
            for status in container_statuses:
                print(status.state)

    def delete_pod(namespaces, pod):
        k8s_core = client.CoreV1Api()
        k8s_core.delete_namespaced_pod(name=pod, namespace=namespaces)


    def get_deployments(namespace):
        v1_apps = client.AppsV1Api()
        deployments = v1_apps.list_namespaced_deployment(namespace)
        return deployments

    def get_deployment(namespace, name):
        v1_apps = client.AppsV1Api()
        deployment = v1_app.list_namespaced_deployment(namespace)
        for d in deployment.items:
            if name == d.metadata.name:
                return d
        raise Exception("Not found exception")

    def restart_deployment(namespace, name):
        v1_apps = client.AppsV1Api()
        deployment = get_deployment(namespace, name)
        deployment.spec.template.metadata.annotations = {
            "kubectl.kubernetes.io/restartedAt": datetime.datetime.utcnow().replace(tzinfo=pytz.UTC).isoformat()
        }
        deployment.api_version = "apps/v1"
        deployment.kind = "Deployment"
        try:
            v1_apps.patch_namespaced_deployment(name, namespace, deployment, pretty='true')
        except ApiException as e:
            print("Exception when calling AppsV1Api->patch_namespaced_deployment %s\n" % e)
            raise e

    def restart_deployment_all(namespace):
        v1_apps = get_v1_apps()
        deployments = get_deployments()
        for d in deployment.items:
            d.spec.template.metadata.annotations = {
                "kubectl.kubernetes.io/restartedAt": datetime.datetime.utcnow().replace(tzinfo=pytz.UTC).isoformat()
            }
            d.api_version = "apps/v1"
            d.kind = "Deployment"
            try:
                v1_apps.patch_namespaced_deployment(d.metadata.name, namespace, d, pretty='true')
            except ApiException as e:
                print("Exception when calling AppsV1Api->patch_namespaced_deployment %s\n" % e)
                raise e
    