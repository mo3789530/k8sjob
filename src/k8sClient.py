from kubernetes import client, config

class k8sClient():

    def getPods(namespace):
        config.load_config()
        k8s_core = client.CoreV1Api()
        pods = k8s_core.list_namespaced_pod('default')
        k8s_core.read_namespaced_pod_status('default')
        k8s_core.read_namespace_status('default')
        for item in pods.items:
            print(item.matadata.name)
            container_statuses = item.status.container_statuses
            for status in container_statuses:
                print(status.state)


    def restart(namespaces, pod):
        config.load_config()
        k8s_core = client.CoreV1Api()
        k8s_core.delete_namespaced_pod(name=pod, namespace=namespaces)