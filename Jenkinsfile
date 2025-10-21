pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "18venky/ticket-booking-flask"
        K8S_NAMESPACE = "default"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker') {
            steps {
                // Use credentials ID directly
                withCredentials([usernamePassword(credentialsId: 'docker-id-cred', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat """
                    echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
                    docker build -t ${DOCKER_IMAGE}:%BUILD_NUMBER% .
                    docker tag ${DOCKER_IMAGE}:%BUILD_NUMBER% ${DOCKER_IMAGE}:latest
                    docker push ${DOCKER_IMAGE}:%BUILD_NUMBER%
                    docker push ${DOCKER_IMAGE}:latest
                    """
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                // Use kubeconfig file credential directly
                withCredentials([file(credentialsId: 'kubeconfig-cred', variable: 'KUBECONFIG_FILE')]) {
                    bat '''
                    if not exist "%USERPROFILE%\\.kube" mkdir "%USERPROFILE%\\.kube"
                    copy "%KUBECONFIG_FILE%" "%USERPROFILE%\\.kube\\config"
                    '''
                    bat """
                    kubectl apply -f k8s\\deployment.yaml --namespace ${K8S_NAMESPACE}
                    kubectl apply -f k8s\\service.yaml --namespace ${K8S_NAMESPACE}
                    kubectl apply -f k8s\\hpa.yaml --namespace ${K8S_NAMESPACE} || echo HPA skipped
                    kubectl set image deployment/ticket-booking-deployment ticket-booking-container=${DOCKER_IMAGE}:%BUILD_NUMBER% --namespace ${K8S_NAMESPACE}
                    kubectl rollout status deployment/ticket-booking-deployment --namespace ${K8S_NAMESPACE} --timeout=120s
                    """
                }
            }
        }
    }

    post {
        success {
            echo "✅ SUCCESS: Build ${env.BUILD_NUMBER}"
        }
        failure {
            echo "❌ FAIL: Build ${env.BUILD_NUMBER}"
        }
    }
}
