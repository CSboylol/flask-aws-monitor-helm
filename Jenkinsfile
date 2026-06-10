pipeline {
    agent any

    environment {
        IMAGE_REPO = 'csboylol23/flask-aws-monitor'
        IMAGE_TAG = "${BUILD_NUMBER}"
        DOCKERHUB_CREDS = credentials('dockerhub-credentials')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Parallel Checks') {
            parallel {
                stage('Python Lint') {
                    steps {
                        sh '''
                            docker run --rm \
                              -v "$PWD:/app" \
                              -w /app \
                              python:3.12-slim \
                              sh -c "pip install --no-cache-dir flake8 && flake8 app.py tests --ignore=E501,W503"
                        '''
                    }
                }

                stage('Python Security Scan') {
                    steps {
                        sh '''
                            docker run --rm \
                              -v "$PWD:/app" \
                              -w /app \
                              python:3.12-slim \
                              sh -c "pip install --no-cache-dir bandit && bandit -r app.py"
                        '''
                    }
                }
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                    docker run --rm \
                      -v "$PWD:/app" \
                      -w /app \
                      python:3.12-slim \
                      sh -c "pip install --no-cache-dir -r requirements.txt pytest && pytest"
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build \
                      -t ${IMAGE_REPO}:${IMAGE_TAG} \
                      -t ${IMAGE_REPO}:latest \
                      .
                '''
            }
        }

        stage('Container Security Scan') {
            steps {
                sh '''
                    docker run --rm \
                      -v /var/run/docker.sock:/var/run/docker.sock \
                      aquasec/trivy:latest \
                      image --exit-code 0 --severity HIGH,CRITICAL ${IMAGE_REPO}:${IMAGE_TAG}
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                sh '''
                    echo "$DOCKERHUB_CREDS_PSW" | docker login \
                      -u "$DOCKERHUB_CREDS_USR" \
                      --password-stdin

                    docker push ${IMAGE_REPO}:${IMAGE_TAG}
                    docker push ${IMAGE_REPO}:latest
                '''
            }
        }

        stage('Helm Validation') {
            steps {
                sh '''
                    docker run --rm \
                      -v "$PWD:/workspace" \
                      -w /workspace \
                      alpine/helm:3.14.4 \
                      lint helmchart

                    docker run --rm \
                      -v "$PWD:/workspace" \
                      -w /workspace \
                      alpine/helm:3.14.4 \
                      template flask-monitor helmchart \
                      --set image.repository=${IMAGE_REPO} \
                      --set image.tag=${IMAGE_TAG}
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully.'
        }

        failure {
            echo 'Pipeline failed. Review the stage logs.'
        }

        always {
            sh 'docker logout || true'
        }
    }
}
