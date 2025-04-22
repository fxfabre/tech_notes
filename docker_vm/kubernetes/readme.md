# Kubernetes

Ressources :
- Installation K3s, multipass ... : https://luc.run/practice/udemy/kubernetes/installation/k3s/


Presentation :
- Process isolé de Linux par l'utilisation de namespace & control groups (cgroups)
- Archi micro-service => déplace la complexité sur le déploiement = rôle de K8s
- Soutenu par la Cloud native computing foundation (cncf.io)
- DevOps = minimiser le temps de livraison d'une fonctionnalité

Fonctionnalités :
- Gestion d'apps tournant dans des containers
- Self-healing = auto détection de services défaillant
- Service discovery : facilite la connexion entre containers
- Gestion des secrets & des configs
- Role Based Access Control (RBAC)
- Orchestration du stockage

Composition d'un cluster :
- Composé de nodes = VM ou serveur physique
- Node ControlPlane (= master) : Gestion du cluster, fait tourner les composants de base :
  API server, controler manager, scheduler et etcd
- Node worker : mettent à dispo leurs ressources pour faire tourner des pods
- Pod = groupe de containers qui partagent une stack réseau et du stockage
- Une application tourne dans un namespace

Accès au cluster :
- API de k8s, hébergée sur le node master. Config par le fichier kubeconfig. kubectl
- Les users accedent à leur app dans les pods par un load balancer 

Ressources pour la gestion :
- Deploiement : server web pour s'assurer qu'on a un certain nb de pods similaires
- DaemonSet : agent sur chaque node, pour collecte logs et monitoring
- Job / CronJob : pour lancer des batch
- StatefulSet : applications stateful (base de données)
- ConfigMap : gestion des données de config dans un pod
- Secret : données sensibles
- PersistentVolumeClaim (PVC) : demande de stockage
- PersistentVolume (PV) : volume pour stockage applicatif

Création d'une ressource
- Définition d'une spec en yaml
- Envoi de la spec à l'API server avec kubectl apply -f config.yaml
  - ApiVersion : dépendant de la ressource
  - kind : pod
  - metadata : name, label
  - spec : containers : list of container (name, image ...)

Architecture
- Node ControlPlane (master)
  - API server : point d'entrée du server
  - Scheduler
  - Controler manager : 
  - etcd : base de données distribuée clé-valeur qui stocke l'état du server
- Sur tous les nodes (Master & Worker)
  - Kubelet : agent géré par system D, redémarre les containers en cas de crash
    - Composant CRI : container runtime interface : pour relancer les containers
    - Composant CNI : container network interface pour accéder au plugin réseau du cluster
    - Composant CSI : container storage interface
  - kube proxy : règles iptable
- Node worker :
  - pods pour faire tourner les apps

API Server :
- Communication par kubectl, interface web ou app tournant dans le cluster
- Pipeline de traitement des requetes :
  - Authentification : utilisateur connu
  - Autorisation : utilisateur a le droit
  - Admission contrôleurs : post traitement de la requete pour ajouter par ex les valeurs par défaut

Etcd :
- Toutes les infos sur les ressources dans le cluster
- Base de données clé-valeur
- Seul l'API server communique avec lui
- Les réplicas d'etcd communiquent avec le protocol RAFT

Scheduler :
- En charge de trouver un node pour chaque nouveau pod
- Paramètres / contraintes
  - nodeSelector / nodeAffinity
  - podAffinity / podAntiAffinity
  - resources.requests
  - taint / toleration

Controler manager
- Surveille l'état courant du cluster via API server
- En charge d'atteindre l'état souhaité






Setup :
- Installer Minikube et kubectl 
- Démarrer un cluster avec minikube start 
- Déployer une application avec kubectl create deployment 
- Exposer et tester avec kubectl expose et minikube service 
- Activer un Ingress Controller pour simuler un vrai cluster 
- Gérer le cluster avec minikube stop/delete

Gestionnaire de cluster :
- Minikube
  - Kubernetes complet avec etcd, plus proche d’une infra cloud.
  - Pilotes de stockage configurables (ex: hostpath).
  - Ingress : Nginx en add-on optionnel.
- kind
  - k8s in Docker
- k3s
  - Kubernetes allégé, optimisé pour les environnements de production légers
  - SQLite au lieu d’etcd, moins de composants.
  - Ingress	: Traefik par défaut.

Setup :
- Minikube :
  - brew install minikube
  - minikube version
  - minikube start --driver=docker
  - kubectl get nodes
  - kubectl create deployment my-nginx --image=nginx
  - kubectl expose deployment my-nginx --type=NodePort --port=80
  - kubectl get pods,svc
  - minikube service my-nginx --url
  - minikube addons enable ingress
  - kubectl apply -f ingress.yaml
  - sudo echo "127.0.0.1 myapp.local" >> /etc/hosts
  - minikube profile list
  - minikube stop
  - minikube delete
- kind
  - brew install kind
  - kind create cluster --name test-cluster
  - kind delete cluster --name test-cluster

Kubectl
- brew install kubectl
- kubectl version --client
- kubectl cluster-name
- kubectl create deployment nginx-test --image=nginx 
- kubectl expose deployment nginx-test --type=NodePort --port=80 
- kubectl get pods,services
- kubectl get service nginx-test
- kubectl port-forward svc/nginx-test 8080:80 & open http://localhost:8080

# Utilitaires
- brew install kompose
  - Creer une config k8s à partir de docker-compose : kompose convert -f docker-compose.yml
  - kubectl apply -f .

Composants :
- Ingress Controller (Traefik ou Nginx)
  - helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
  - helm install nginx ingress-nginx/ingress-nginx 
  - kubectl get pods -n default
