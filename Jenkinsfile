pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
    }
    parameters {
        choice(
            name: 'TARGET_ENV',
            choices: ['dev', 'qa', 'prd'],
            description: 'Environment to update in the GitOps repository'
        )
    }

    environment {
        IMAGE_REPO = 'csboylol23/flask-aws-monitor'
        IMAGE_TAG = "${BUILD_NUMBER}"
        DOCKERHUB_CREDS = credentials('dockerhub-credentials')
        WORKSPACE_VOLUME = "flask-aws-monitor-workspace-${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Prepare Docker Workspace') {
            steps {
                sh '''
                    docker volume rm -f ${WORKSPACE_VOLUME} >/dev/null 2>&1 || true
                    docker volume create ${WORKSPACE_VOLUME}

                    tar -cf - . | docker run --rm -i \
                      -v ${WORKSPACE_VOLUME}:/workspace \
                      alpine:3.20 \
                      sh -c "cd /workspace && tar -xf -"
                '''
            }
        }

        stage('Parallel Checks') {
            parallel {
                stage('Python Lint') {
                    steps {
                        sh '''
                            docker run --rm \
                              -v ${WORKSPACE_VOLUME}:/workspace \
                              -w /workspace \
                              python:3.12-slim \
                              sh -c "pip install --no-cache-dir flake8 && flake8 app.py tests --ignore=E501,W503"
                        '''
                    }
                }

                stage('Python Security Scan') {
                    steps {
                        sh '''
                            docker run --rm \
                              -v ${WORKSPACE_VOLUME}:/workspace \
                              -w /workspace \
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
                      -v ${WORKSPACE_VOLUME}:/workspace \
                      -w /workspace \
                      python:3.12-slim \
                      sh -c "pip install --no-cache-dir -r requirements.txt pytest && python -m pytest"
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
                      -v ${WORKSPACE_VOLUME}:/workspace \
                      -w /workspace \
                      alpine/helm:3.14.4 \
                      lint helmchart

                    docker run --rm \
                      -v ${WORKSPACE_VOLUME}:/workspace \
                      -w /workspace \
                      alpine/helm:3.14.4 \
                      template flask-monitor helmchart \
                      --set image.repository=${IMAGE_REPO} \
                      --set image.tag=${IMAGE_TAG}
                '''
            }
        }

        stage('Push to ArgoCD') {
            steps {
                script {
                    def selectedEnv = params.TARGET_ENV

                    echo "Deploying build ${BUILD_NUMBER} to ${selectedEnv}"

                    withCredentials([usernamePassword(
                        credentialsId: 'github-argoCD',
                        usernameVariable: 'GIT_USER',
                        passwordVariable: 'GIT_TOKEN'
                    )]) {
                        sh '''
                            docker run --rm \
                              -v ${WORKSPACE_VOLUME}:/workspace \
                              -w /workspace \
                              alpine/helm:3.14.4 \
                              template flask-aws-monitor helmchart \
                              --set image.repository=${IMAGE_REPO} \
                              --set image.tag=${IMAGE_TAG} \
                              > devops-template.yaml

                            rm -rf gitops-deploy
                            git clone https://github.com/CSboylol/gitops.git gitops-deploy

                            mkdir -p gitops-deploy/deployments/${TARGET_ENV}
                            cp devops-template.yaml \
                              gitops-deploy/deployments/${TARGET_ENV}/devops-template.yaml

                            cd gitops-deploy

                            git config user.name "Jenkins Bot"
                            git config user.email "jenkins-bot@example.com"

                            git add deployments/${TARGET_ENV}/devops-template.yaml

                            git commit \
                              -m "Deploy build ${BUILD_NUMBER} to ${TARGET_ENV}" || \
                              echo "No GitOps changes to commit"

                            git push \
                              https://x-access-token:${GIT_TOKEN}@github.com/CSboylol/gitops.git \
                              HEAD:main
                        '''
                    }
                }
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
            sh '''
                docker logout || true
                docker volume rm -f ${WORKSPACE_VOLUME} >/dev/null 2>&1 || true
            '''
        }
    }
}






