from kubernetes import client, config
import datetime
import pytz

class k8sClient():

    def get_k8s_config(self, is_cluster):
        print("Is cluster:" + str(is_cluster))
        if is_cluster == True:
            # https://github.com/kubernetes-client/python/blob/master/examples/in_cluster_config.py
            return config.load_incluster_config()
        else:
            # https://github.com/kubernetes-client/python/blob/master/examples/out_of_cluster_config.py
            return config.load_kube_config()

    def get_pods_status(self, config, namespace):
        k8s_core = client.CoreV1Api()
        pods = k8s_core.list_namespaced_pod('default')
        k8s_core.read_namespaced_pod_status('default')
        k8s_core.read_namespace_status('default')
        for item in pods.items:
            print(item.matadata.name)
            container_statuses = item.status.container_statuses
            for status in container_statuses:
                print(status.state)

    def delete_pod(self, namespaces, pod):
        k8s_core = client.CoreV1Api()
        k8s_core.delete_namespaced_pod(name=pod, namespace=namespaces)


    def get_deployments(self, namespace):
        v1_apps = client.AppsV1Api()
        deployments = v1_apps.list_namespaced_deployment(namespace)
        return deployments

    def get_deployment(self, namespace, name):
        v1_apps = client.AppsV1Api()
        deployment = v1_apps.list_namespaced_deployment(namespace)
        for d in deployment.items:
            if name == d.metadata.name:
                return d
        raise Exception("Not found exception")

    def restart_deployment(self, namespace, name):
        v1_apps = client.AppsV1Api()
        deployment = self.get_deployment(namespace, name)
        deployment.spec.template.metadata.annotations = {
            "kubectl.kubernetes.io/restartedAt": datetime.datetime.utcnow().replace(tzinfo=pytz.UTC).isoformat()
        }
        deployment.api_version = "apps/v1"
        deployment.kind = "Deployment"
        try:
            resp = v1_apps.patch_namespaced_deployment(name, namespace, deployment, pretty='true')
            print("%s\t%s\t\t\t%s\t%s" % ("NAMESPACE", "NAME", "REVISION", "IMAGE"))
            print(
                "%s\t\t%s\t%s\t\t%s\n"
                % (
                    resp.metadata.namespace,
                    resp.metadata.name,
                    resp.metadata.generation,
                    resp.spec.template.spec.containers[0].image,
                )
            )
        except ApiException as e:
            print("Exception when calling AppsV1Api->patch_namespaced_deployment %s\n" % e)
            raise e

    def restart_deployment_all(self, namespace):
        v1_apps = client.AppsV1Api()
        deployments = self.get_deployments(namespace)
        for d in deployments.items:
            d.spec.template.metadata.annotations = {
                "kubectl.kubernetes.io/restartedAt": datetime.datetime.utcnow().replace(tzinfo=pytz.UTC).isoformat()
            }
            d.api_version = "apps/v1"
            d.kind = "Deployment"
            try:
                resp = v1_apps.patch_namespaced_deployment(d.metadata.name, namespace, d, pretty='true')
                print("%s\t%s\t\t\t%s\t%s" % ("NAMESPACE", "NAME", "REVISION", "IMAGE"))
                print(
                    "%s\t\t%s\t%s\t\t%s\n"
                    % (
                        resp.metadata.namespace,
                        resp.metadata.name,
                        resp.metadata.generation,
                        resp.spec.template.spec.containers[0].image,
                    )
                )
            except ApiException as e:
                print("Exception when calling AppsV1Api->patch_namespaced_deployment %s\n" % e)
                raise e
    