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
                sh '''
                    python3 -m venv /tmp/obs-venv
                    /tmp/obs-venv/bin/pip install -r app/requirements.txt
                    /tmp/obs-venv/bin/python -m compileall app/
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ./app
                '''
            }
        }

        stage('Load Image into Kind') {
            steps {
                sh '''
                    kind load docker-image ${IMAGE_NAME}:${IMAGE_TAG} \
                        --name ${CLUSTER}
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    kubectl apply -f k8s/app-deployment.yaml
                    kubectl apply -f k8s/app-service.yaml
                    kubectl apply -f k8s/app-servicemonitor.yaml
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    kubectl rollout status deployment/observability-app \
                        -n observability --timeout=120s

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
