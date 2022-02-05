from logging import getLogger
import logging
from k8sClient import k8sClient

logger = getLogger(__name__)
logging.basicConfig(level=logging.INFO)



def main():
    k8s = k8sClient()
    k8s.getPods()


if __name__ == '__main__':
    main()