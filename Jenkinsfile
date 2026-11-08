pipeline {
  agent any

  environment {
    IMAGE_NAME = 'demo-app'
    IMAGE_TAG  = "${env.BUILD_NUMBER}"
    RELEASE    = 'demo'
    NAMESPACE  = 'demo'
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Build image') {
      steps {
        sh 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .'
      }
    }

    stage('Load into minikube') {
      steps {
        sh 'minikube image load ${IMAGE_NAME}:${IMAGE_TAG}'
      }
    }

    stage('Helm lint') {
      steps {
        sh 'helm lint chart/demo-app'
      }
    }

    stage('Deploy') {
      steps {
        sh '''
          helm upgrade --install ${RELEASE} chart/demo-app \
            --namespace ${NAMESPACE} --create-namespace \
            --set image.repository=${IMAGE_NAME} \
            --set image.tag=${IMAGE_TAG} \
            --wait --timeout 90s
        '''
      }
    }

    stage('Smoke test') {
      steps {
        sh 'kubectl -n ${NAMESPACE} rollout status deploy/${RELEASE} --timeout=60s'
      }
    }
  }

  post {
    failure {
      sh 'kubectl -n ${NAMESPACE} get pods || true'
      sh 'kubectl -n ${NAMESPACE} describe deploy/${RELEASE} || true'
    }
  }
}
