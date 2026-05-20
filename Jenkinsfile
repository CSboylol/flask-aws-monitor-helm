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

        stage('Push Simulation') {
            container('docker') {
                echo "Simulating docker push..."
                sh "echo docker push ${appimage}"
            }
        }
    }
}
