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

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ./app
                '''
            }
        }

        stage('Test Container') {
            steps {
                sh '''
                    docker rm -f jenkins-test-app 2>/dev/null || true

                    docker run -d \
                        --name jenkins-test-app \
                        -p 8001:8000 \
                        ${IMAGE_NAME}:${IMAGE_TAG}

                    sleep 5

                    curl -f http://localhost:8001/health

                    docker rm -f jenkins-test-app
                '''
            }
        }

        stage('Load Image into Kind') {
            steps {
                sh '''
                    kind load docker-image \
                        ${IMAGE_NAME}:${IMAGE_TAG} \
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
                    kubectl rollout status \
                        deployment/observability-app \
                        -n observability \
                        --timeout=120s

                    kubectl get pods -n observability
                    kubectl get service -n observability
                '''
            }
        }
    }

    post {
        always {
            sh '''
                docker rm -f jenkins-test-app 2>/dev/null || true
            '''
        }

        success {
            echo 'Kubernetes observability deployment completed successfully!'
        }

        failure {
            echo 'Pipeline failed. Check the failed stage.'
        }
    }
}
