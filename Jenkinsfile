def appname = "hello-newapp"
def repo = "elevy99927"
def apptag = "${env.BUILD_NUMBER}"

def appimage = "docker.io/${repo}/${appname}:${apptag}"
def latestimage = "docker.io/${repo}/${appname}:latest"

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

        stage('Build Docker Image') {
            container('docker') {
                echo "Building Docker image: ${appimage}"
                sh "docker build -t ${appimage} ."
                sh "docker tag ${appimage} ${latestimage}"
            }
        }

        stage('Push Docker Image') {
            container('docker') {
                echo "Pushing Docker image: ${appimage}"
                sh "docker push ${appimage}"

                echo "Pushing Docker image: ${latestimage}"
                sh "docker push ${latestimage}"
            }
        }
    }
}
