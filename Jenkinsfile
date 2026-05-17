@Library('my-shared-library') _

pipeline {
    agent any

    stages {
        stage('Start') {
            steps {
                echo 'Pipeline started'
            }
        }

        stage('SonarQube Project') {
            steps {
                script {
                    codeQuality.sonarCreateProject(env.JOB_NAME)
                }
            }
        }

        stage('SonarQube Scan') {
            steps {
                script {
                    codeQuality.sonarLocalScan()
                }
            }
        }
    }
}
