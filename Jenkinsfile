pipeline {
    agent any

    environment {
        IMAGE_NAME = "observability-app"
        IMAGE_TAG  = "v1"
        CLUSTER    = "observability-cluster"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test') {
            steps {
                bat '''
                    python --version
                    python -m compileall app
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                bat '''
                    docker build -t %IMAGE_NAME%:%IMAGE_TAG% ./app
                '''
            }
        }

        stage('Load Image into Kind') {
            steps {
                bat '''
                    kind load docker-image %IMAGE_NAME%:%IMAGE_TAG% --name %CLUSTER%
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat '''
                    kubectl apply -f k8s/app-deployment.yaml
                    kubectl apply -f k8s/app-service.yaml
                    kubectl apply -f k8s/app-servicemonitor.yaml
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                bat '''
                    kubectl rollout status deployment/observability-app -n observability --timeout=120s
                    kubectl get pods -n observability
                '''
            }
        }
    }

    post {
        success {
            echo 'Deployment completed successfully!'
        }

        failure {
            echo 'Pipeline failed. Check the stage logs.'
        }
    }
}
