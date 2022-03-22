from kubernetes import client, config
import datetime


class k8sClient():

    def get_config(isIncluster):
        if isIncluster == true:
            # https://github.com/kubernetes-client/python/blob/master/examples/in_cluster_config.py
            return config.load_incluster_config()
        else 
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


    def get_v1_apps():
        v1_apps = client.AppsV1Api()
        return v1_apps

    def get_deployments(namespace):
        v1_apps = get_v1_apps()
        deployment = v1_apps.list_namespaced_deployment(namespace)
        print(deployment)

    def get_deployment(namespace, name):
        pass


    def restart_deployment(namespace, name, deployment):
        v1_apps = get_v1_apps()
        deployment.spec.template.metadata.annotations = {
            "kubectl.kubernetes.io/restartedAt": datetime.datetime.utcnow()
            .replace(tzinfo=pytz.UTC)
            .isoformat()
        }
        try:
            v1_apps.patch_namespaced_deployment(name, namespace, deployment, pretty='true')
        except ApiException as e:
            print("Exception when calling AppsV1Api->patch_namespaced_deployment %s\n" % e)


