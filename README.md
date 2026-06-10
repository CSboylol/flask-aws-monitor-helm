# Flask AWS Monitor

## Overview
This repository contains a Flask application that displays AWS resources from the configured AWS account.

The application lists:

- EC2 instances
- VPCs
- Subnets
- Load Balancers
- AMIs owned by the account

## Repository Contents

- app.py - Flask application
- requirements.txt - Python dependencies
- Dockerfile - Container image definition
- Jenkinsfile - CI/CD pipeline
- helmchart - Helm chart for Kubernetes deployment
- tests - Unit tests

## Local Run

Install dependencies:

pip install -r requirements.txt

Run the application:

python app.py

Open:

http://localhost:5001

## Docker

Build the image:

docker build -t flask-aws-monitor:local .

Run the container:

docker run --rm -p 5001:5001 flask-aws-monitor:local

## AWS Environment Variables

- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_DEFAULT_REGION

Do not commit real AWS credentials.

## Tests

python -m pytest

## Helm Validation

helm lint ./helmchart

helm template flask-monitor ./helmchart

## Jenkins Pipeline

The Jenkins pipeline performs:

- Repository checkout
- Python linting
- Python security scanning
- Unit tests
- Docker image build
- Trivy container scan
- Docker Hub push
- Helm validation

## Current Validation Status

The application has passed:

- Docker build
- Local container run
- HTTP 200 response check
- Unit tests
- Helm lint
- Helm template rendering
