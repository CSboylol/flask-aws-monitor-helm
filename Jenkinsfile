def appname = "hello-newapp"
def repo = "csboylol23"
def apptag = "${env.BUILD_NUMBER}"

def appimage = "docker.io/${repo}/${appname}:${apptag}"

podTemplate(
    cloud: 'kubernetes',
    containers: [
        containerTemplate(
            name: 'jnlp',
            image: 'jenkins/inbound-agent:latest'
        ),
        containerTemplate(
            name: 'docker',
            image: 'docker:26-dind',
            privileged: true,
            args: '--storage-driver=vfs'
        ),
        containerTemplate(
            name: 'helm',
            image: 'alpine/helm:3.14.4',
            command: 'cat',
            ttyEnabled: true
        )
    ],
    volumes: [
        emptyDirVolume(mountPath: '/var/lib/docker', memory: false)
    ]
) {

    node(POD_LABEL) {

        stage('Checkout') {
            container('jnlp') {
                sh '/usr/bin/git config --global http.sslVerify false'
                checkout scm
            }
        }

        stage('Build') {
            container('docker') {
                echo "Building docker image: ${appimage}"
                sh "docker build -t ${appimage} ."
            }
        }
        stage('Helm Template') {
            container('helm') {
                sh """
                helm template flask-app helmchart \
                  --set image.repository=${repo}/${appname} \
                  --set image.tag=${apptag}
                """
            }
        }
        stage('Push') {
            container('docker') {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh 'echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin'
                    sh "docker push ${appimage}"
                }
            }
        }
    }
}
