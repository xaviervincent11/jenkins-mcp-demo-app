pipeline {
  agent {
    kubernetes {
      defaultContainer 'helm'
      yaml '''
apiVersion: v1
kind: Pod
spec:
  serviceAccountName: demo-app-deployer
  containers:
    - name: kaniko
      image: gcr.io/kaniko-project/executor:v1.23.2-debug
      command:
        - /busybox/cat
      tty: true
    - name: helm
      image: alpine/helm:3.17.3
      command:
        - /bin/sh
        - -c
        - cat
      tty: true
'''
    }
  }

  options {
    skipDefaultCheckout(true)
  }

  environment {
    IMAGE_NAME = 'demo-app'
    IMAGE_TAG = "${env.BUILD_NUMBER}"
    PUSH_REGISTRY = 'registry.kube-system.svc.cluster.local:80'
    IMAGE_REPOSITORY = 'localhost:5000/demo-app'
    RELEASE = 'demo'
    NAMESPACE = 'demo'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build and publish image') {
      steps {
        container('kaniko') {
          sh '''
            /kaniko/executor \
              --context="dir://${WORKSPACE}" \
              --dockerfile="${WORKSPACE}/Dockerfile" \
              --destination="${PUSH_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}" \
              --insecure
          '''
        }
      }
    }

    stage('Helm lint') {
      steps {
        container('helm') {
          sh 'helm lint chart/demo-app'
        }
      }
    }

    stage('Deploy') {
      steps {
        container('helm') {
          sh '''
            helm upgrade --install "${RELEASE}" chart/demo-app \
              --namespace "${NAMESPACE}" \
              --set-string image.repository="${IMAGE_REPOSITORY}" \
              --set-string image.tag="${IMAGE_TAG}" \
              --wait --timeout 120s
          '''
        }
      }
    }

    stage('Smoke test') {
      steps {
        container('helm') {
          sh '''
            response="$(wget -qO- -T 10 -t 5 "http://${RELEASE}.${NAMESPACE}.svc.cluster.local/health")"
            [ "$response" = "ok" ]
          '''
        }
      }
    }
  }

  post {
    failure {
      container('helm') {
        sh 'helm status "${RELEASE}" --namespace "${NAMESPACE}" --show-resources || true'
        sh 'helm get all "${RELEASE}" --namespace "${NAMESPACE}" || true'
      }
    }
  }
}
