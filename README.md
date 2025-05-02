# Brain Station 23 DevOps Task | Weather API — Zero Downtime Deployment

A Django-based Weather API project built with CI/CD automation and Kubernetes infrastructure — ready for local development and scalable production deployments.

- [Part A](#features)
- [Part B](#part-b-e-commerce-architecture)

## Features

- `/api/hello`: Returns server metadata, version, timestamp, and live weather data for Dhaka
- `/api/health`: Verifies server health and 3rd-party API availability
- Dockerized for local and production environments
- GitHub Actions CI/CD pipeline with zero-downtime deployments
- Modular Terraform setup for AWS EKS cluster provisioning
- Kubernetes manifests for scalable deployment and service exposure

## Run Locally with Docker

### 1. Clone the Repository

```bash
git clone https://github.com/mdfathi99/WeatherAPIZeroDowntime.git
cd WeatherAPIZeroDowntime
```

### API Endpoints

- `GET /api/hello`

Returns:
```json
{
  "hostname": "server1",
  "datetime": "YYMMDDHHmm",
  "version": "1.0.0",
  "weather": {
    "dhaka": {
      "temperature": "14",
      "temp_unit": "c"
    }
  }
}
```
- `GET /api/health`

This endpoint returns

- Django application status

- Weather API reachability

Run Locallay:

```bash
docker-compose up --build
```
App will be available at http://localhost:8000/ with swagger UI

<img width="983" alt="image" src="https://github.com/user-attachments/assets/b3489ee0-0f8e-461b-b3d8-43946c365cf5" />


## Part 3: Version Control & CI/CD Pipeline [Asked in Part 3]

### GitHub Actions

- Trigger: On Release Creation
- Steps:
  - Build and tag Docker image with release version
  - Push to Docker Hub
  - SSH deploy to server using `docker-compose`
  - Perform health check post-deployment

### Secrets are Required

| Name              | Purpose                 |
|-------------------|--------------------------|
| DOCKER_USERNAME   | Docker Hub Login        |
| DOCKER_PASSWORD   | Docker Hub Password     |
| SERVER_HOST       | SSH Host for Deployment |
| SERVER_USER       | SSH Username            |
| SERVER_SSH_KEY    | Private Key for Access  |

---

### Preview CICD Workflow:
First, we created a release version which triggerted the action which builds and push the docker image into dockerhub's public or private reposiroty based on what I have added as secret in the github setings.
<img width="1231" alt="image" src="https://github.com/user-attachments/assets/c0761734-ae1c-421f-9ea3-2a0fcc877f07" />

Image has been uploaded into dockerhub by github action 
<img width="998" alt="image" src="https://github.com/user-attachments/assets/2e21b31f-204b-4b70-b69a-d7bc1c57717d" />

## Part 4: Terraform & Kubernetes (IaC & Zero Downtime)

### Terraform Infrastructure

- AWS Region: \`eu-central-1\`
- Modules:
  - VPC
  - EKS Cluster
  - Node Groups
- Remote Backend: S3-compatible

### Kubernetes Setup

- \`k8s/configmap.yaml\`: Application config
- \`k8s/deployment.yaml\`: Deployment resource
- \`k8s/service.yaml\`: Exposes app using LoadBalancer

### CI/CD to Kubernetes

- Future pipeline support for:
  - \`kubectl apply\` using GitHub Actions
  - Rolling updates to ensure zero-downtime

---

## Observability (Planned/Extendable)

- Logs: via EKS CloudWatch integration
- Metrics: Prometheus (future)
- Tracing: OpenTelemetry support (future)

---

# Part B (E-commerce Architecture)

![diagram-export-5-2-2025-1_48_27-PM](https://github.com/user-attachments/assets/e438908a-8766-4280-83c0-d57119ca9ce4)

## Components Breakdown

### 1. **Frontend and API Gateway**
- **CloudFront**: Global content delivery for low-latency access.
- **Route 53**: DNS routing based on geography.
- **API Gateway**: Handles incoming API requests securely and routes them to backend services.

### 2. **Microservices Cluster**
- **EKS (Kubernetes)**: Manages containerized services:
  - `read-service`
  - `write-service`
  - `product-service`
- **Horizontal scaling** managed by EKS auto-scaling groups.

### 3. **Background Job Processing**
- **AWS Lambda**: For small/quick jobs.
- **K8s Jobs (Pods)**: For large data processing jobs.
- Triggered asynchronously via internal services or event-driven pipelines.

### 4. **Data Layer**
- **Amazon Aurora (PostgreSQL)**: Primary transactional database.
- **Redis**: Used for caching product data and API responses.
- **OpenSearch**: Full-text search capabilities across product catalogs.
- **SNS + SQS**: Asynchronous event handling and inter-service communication.

### 5. **Observability and Monitoring**
- **AWS X-Ray**: Request tracing.
- **CloudWatch**: Logs and metrics.
- **Prometheus + Grafana**: Custom metrics and dashboards.

### 6. **Security**
- **WAF**: Protects API Gateway from common web exploits.
- **Secrets Manager**: Securely stores API keys, database credentials.
- **IAM**: Role-based access control for services and users.

### 7. **Infrastructure as Code & CI/CD**
- **Terraform**: Manages infrastructure with modular templates.
- **CI/CD**:
  - GitHub Actions
  - GitLab CI
  - Jenkins
- Fully automated build-test-deploy pipeline for all services.

### 8. **External System Integrations**
- Product lists are fetched via **Partner APIs**, ingested via scheduled jobs.
- Cached and stored in the DB for quick access.

---

## Best Practices Followed

- **Security First**: Credentials managed securely with Secrets Manager and IAM.
- **Modularity**: Terraform and CI/CD pipelines follow modular design for reusability.
- **Cost Efficiency**: Uses auto-scaling services and serverless components where appropriate.
- **High Availability**: Globally distributed architecture with failover configurations.
- **Observability**: Comprehensive monitoring ensures visibility and debugging.

---
