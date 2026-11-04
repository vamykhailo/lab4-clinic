pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {
        stage('Checkout') {
            steps {
                deleteDir()
                checkout scm
            }
        }

        stage('Test') {
            agent {
                docker {
                    image 'python:3.12-slim'
                    reuseNode true
                }
            }

            steps {
                sh '''
                    python -m venv .venv
                    .venv/bin/python -m pip install --no-cache-dir \
                        -r requirements.txt unittest-xml-reporting
                    .venv/bin/python run_tests.py
                '''
            }

            post {
                always {
                    junit testResults: 'test-reports/*.xml'
                }
            }
        }

        stage('Build images') {
            steps {
                sh '''
                    docker build -f Dockerfile.registry \
                        -t lab4-clinic-registry:${BUILD_NUMBER} .

                    docker build -f Dockerfile.appointments \
                        -t lab4-clinic-appointments:${BUILD_NUMBER} .
                '''
            }
        }
    }
}