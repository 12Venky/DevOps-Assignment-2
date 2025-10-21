pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "18venky/ticket-booking-flask"
        K8S_NAMESPACE = "default"
        DOCKER_TAG = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-id-cred', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat """
                    echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
                    docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                    docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                    """
                }
            }
        }

        stage('Test Application') {
            steps {
                script {
                    // Remove existing container if exists
                    bat "docker rm -f test-app || echo No existing container"

                    // Run container on port 5000
                    bat "docker run -d --name test-app -p 5000:5000 ${DOCKER_IMAGE}:${DOCKER_TAG}"
                    
                    // Wait for app to start
                    bat 'ping 127.0.0.1 -n 10 >nul'

                    // Health check using PowerShell curl
                    bat """
                    powershell -Command "curl http://localhost:5000/health -UseBasicParsing"
                    powershell -Command "curl http://localhost:5000/ -UseBasicParsing"
                    """

                    // Stop and remove container
                    bat "docker stop test-app && docker rm test-app"
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-id-cred', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat """
                    docker login -u %DOCKER_USER% -p %DOCKER_PASS%
                    docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                    docker push ${DOCKER_IMAGE}:latest
                    """
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig-cred', variable: 'KUBECONFIG_FILE')]) {
                    bat '''
                    if not exist "%USERPROFILE%\\.kube" mkdir "%USERPROFILE%\\.kube"
                    copy "%KUBECONFIG_FILE%" "%USERPROFILE%\\.kube\\config"
                    '''
                    bat """
                    kubectl apply -f k8s\\deployment.yaml --namespace ${K8S_NAMESPACE}
                    kubectl apply -f k8s\\service.yaml --namespace ${K8S_NAMESPACE}
                    kubectl apply -f k8s\\hpa.yaml --namespace ${K8S_NAMESPACE} || echo HPA skipped

                    kubectl set image deployment/ticket-booking-deployment ticket-booking-container=${DOCKER_IMAGE}:${DOCKER_TAG} --namespace ${K8S_NAMESPACE}
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
