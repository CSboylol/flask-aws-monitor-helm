Flask AWS Monitor - Helm Deployment
This project packages a Flask-based AWS monitoring application and deploys it to Kubernetes using Helm.

Overview
The application connects to AWS using environment variables and displays resources such as EC2 instances, VPCs, subnets, AMIs, and load balancers.
The Helm chart allows flexible deployment by controlling configuration through values.yaml, without modifying the Kubernetes manifests directly.

Deployment
Install the chart:
helm install flask-monitor .

Verify the deployment:
kubectl get pods
kubectl get svc

Accessing the Application
Local (ClusterIP)
By default, the service is configured as ClusterIP, which is suitable for local environments.

Forward the port:
kubectl port-forward svc/flask-monitor-service 5001:5001
Access in browser:
http://localhost:5001

External Access (LoadBalancer)
To expose the application externally:
helm upgrade flask-monitor . --set service.type=LoadBalancer
Then check:
kubectl get svc

Once an external IP is available:
http://<external-ip>:5001
Configuration
Configuration is managed through values.yaml.