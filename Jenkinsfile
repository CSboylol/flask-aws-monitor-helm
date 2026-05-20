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
            name: 'kaniko',
            image: 'gcr.io/kaniko-project/executor:debug',
            command: '/busybox/cat',
            ttyEnabled: true
        ),

        containerTemplate(
            name: 'helm',
            image: 'alpine/helm:3.14.4',
            command: 'cat',
            ttyEnabled: true
        )
    ],

    volumes: [

        configMapVolume(
            mountPath: '/kaniko/.docker/',
            configMapName: 'docker-cred'
        )
    ]
) {

    node(POD_LABEL) {

        stage('Checkout') {

            container('jnlp') {

                sh '/usr/bin/git config --global http.sslVerify false'

                checkout scm
            }
        }

        stage('Build & Push With Kaniko') {

            container('kaniko') {

                echo "Building and pushing image with Kaniko: ${appimage}"

                sh """
                /kaniko/executor \
                  --context=`pwd` \
                  --dockerfile=Dockerfile \
                  --destination=${appimage} \
                  --cache=true
                """
            }
        }

        stage('Helm Template') {

            container('helm') {

                echo "Rendering Helm template..."

                sh """
                helm template flask-app helmchart \
                  --set image.repository=${repo}/${appname} \
                  --set image.tag=${apptag}
                """
            }
        }
    }
}
