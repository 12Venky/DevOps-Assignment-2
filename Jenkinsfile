pipeline {
  agent any

  environment {
    DOCKER_IMAGE = "18venky/ticket-booking-flask"
    DOCKER_CREDENTIALS = 'docker-id-cred'     
    KUBECONFIG_CRED = 'kubeconfig-cred'         
    K8S_NAMESPACE = 'default'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Install & Lint') {
      steps {
        bat '''
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        '''
        // Add pytest or lint tools if needed
      }
    }

    stage('Build Docker') {
      steps {
        withCredentials([usernamePassword(credentialsId: env.DOCKER_CREDENTIALS, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
          bat """
          echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
          docker build -t ${DOCKER_IMAGE}:${env.BUILD_NUMBER} .
          docker tag ${DOCKER_IMAGE}:${env.BUILD_NUMBER} ${DOCKER_IMAGE}:latest
          docker push ${DOCKER_IMAGE}:${env.BUILD_NUMBER}
          docker push ${DOCKER_IMAGE}:latest
          """
        }
      }
    }

    stage('Deploy to Kubernetes') {
      steps {
        withCredentials([file(credentialsId: env.KUBECONFIG_CRED, variable: 'KUBECONFIG_FILE')]) {
          bat '''
          if not exist "%USERPROFILE%\\.kube" mkdir "%USERPROFILE%\\.kube"
          copy "%KUBECONFIG_FILE%" "%USERPROFILE%\\.kube\\config"
          '''
          bat """
          kubectl apply -f k8s\\deployment.yaml --namespace ${env.K8S_NAMESPACE}
          kubectl apply -f k8s\\service.yaml --namespace ${env.K8S_NAMESPACE}
          kubectl apply -f k8s\\hpa.yaml --namespace ${env.K8S_NAMESPACE} || echo HPA skipped
          kubectl set image deployment/ticket-booking-deployment ticket-booking-container=${DOCKER_IMAGE}:${env.BUILD_NUMBER} --namespace ${env.K8S_NAMESPACE}
          kubectl rollout status deployment/ticket-booking-deployment --namespace ${env.K8S_NAMESPACE} --timeout=120s
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
