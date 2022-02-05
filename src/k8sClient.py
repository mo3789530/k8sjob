from kubernetes import client, config

class k8sClient():

    def getPods(namespace):
        config.load_config()
        k8s_core = client.CoreV1Api()
        pods = k8s_core.list_namespaced_pod(namespace=namespace)
        for item in pods.items:
            print(item.matadata.name)
            print(item.status)


    def restart(namespaces, pod):
        config.load_config()
        k8s_core = client.CoreV1Api()
        k8s_core.delete_namespaced_pod(name=pod, namespace=namespaces)