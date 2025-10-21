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
                echo "🔄 Checking out source code..."
                checkout scm
            }
        }

        stage('Build Docker') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-id-cred', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat """
                    echo Logging into Docker Hub...
                    echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin

                    echo Building Docker image...
                    docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                    docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                    """
                }
            }
        }

        stage('Test Application') {
            steps {
                script {
                    echo "⚡ Testing Docker container..."

                    // Remove old container safely
                    bat "docker rm -f test-app || echo No existing container"

                    // Run container
                    bat "docker run -d --name test-app -p 5000:5000 ${DOCKER_IMAGE}:${DOCKER_TAG}"

                    // Wait for app startup
                    bat 'ping 127.0.0.1 -n 10 >nul'

                    // Health checks (fail build if not reachable)
                    def health1 = bat(script: 'powershell -Command "curl http://localhost:5000/health -UseBasicParsing"', returnStatus: true)
                    def health2 = bat(script: 'powershell -Command "curl http://localhost:5000/ -UseBasicParsing"', returnStatus: true)
                    if (health1 != 0 || health2 != 0) {
                        error("❌ Health check failed!")
                    }

                    // Stop and remove container
                    bat "docker stop test-app && docker rm test-app"
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-id-cred', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat """
                    echo Pushing Docker images...
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
                    echo Setting up kubeconfig...
                    if not exist "%USERPROFILE%\\.kube" mkdir "%USERPROFILE%\\.kube"
                    copy /Y "%KUBECONFIG_FILE%" "%USERPROFILE%\\.kube\\config"
                    '''

                    bat """
                    echo Deploying to Kubernetes...
                    kubectl apply -f k8s\\deployment.yaml --namespace ${K8S_NAMESPACE}
                    kubectl apply -f k8s\\service.yaml --namespace ${K8S_NAMESPACE} || echo Service skipped
                    kubectl apply -f k8s\\hpa.yaml --namespace ${K8S_NAMESPACE} || echo HPA skipped

                    echo Updating image in deployment...
                    kubectl set image deployment/ticket-booking-deployment ticket-booking-container=${DOCKER_IMAGE}:${DOCKER_TAG} --namespace ${K8S_NAMESPACE}
                    kubectl rollout status deployment/ticket-booking-deployment --namespace ${K8S_NAMESPACE} --timeout=120s
                    """
                }
            }
        }
    }

    post {
        success {
            echo "✅ SUCCESS: Build ${env.BUILD_NUMBER} completed."
        }
        failure {
            echo "❌ FAILED: Build ${env.BUILD_NUMBER}."
        }
        always {
            echo "🧹 Cleaning up Docker images..."
            bat "docker image prune -f"
        }
    }
}
