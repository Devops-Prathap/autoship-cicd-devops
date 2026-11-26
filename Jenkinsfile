
pipeline {
    agent any

    environment {
        AWS_DEFAULT_REGION = 'ap-south-1'
        ECR_REGISTRY = '194722409383.dkr.ecr.ap-south-1.amazonaws.com'
        ECR_REPOSITORY = 'autoship'
        IMAGE_TAG = "build-${BUILD_NUMBER}"
        ECR_IMAGE = "${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}"
        KIND_CLUSTER = 'autoship-local-cluster'
    }

    stages {
        stage('Checkout Source') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %ECR_REPOSITORY%:%IMAGE_TAG% .'
            }
        }

        stage('Login to AWS ECR') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'aws-ecr-credentials',
                        usernameVariable: 'AWS_ACCESS_KEY_ID',
                        passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                    )
                ]) {
                    bat '''
                        aws ecr get-login-password --region %AWS_DEFAULT_REGION% | docker login --username AWS --password-stdin %ECR_REGISTRY%
                    '''
                }
            }
        }

        stage('Tag and Push to ECR') {
            steps {
                bat 'docker tag %ECR_REPOSITORY%:%IMAGE_TAG% %ECR_IMAGE%'
                bat 'docker push %ECR_IMAGE%'
            }
        }

        stage('Load Image into Kind') {
            steps {
                bat 'kind load docker-image %ECR_IMAGE% --name %KIND_CLUSTER%'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat 'kubectl set image deployment/autoship-deployment autoship=%ECR_IMAGE%'
                bat 'kubectl rollout status deployment/autoship-deployment --timeout=180s'
            }
        }

        stage('Verify Deployment') {
            steps {
                bat 'kubectl get deployments'
                bat 'kubectl get pods -o wide'
                bat 'kubectl get services'
            }
        }
    }

    post {
        success {
            echo 'AutoShip CI/CD pipeline completed successfully!'
            echo "Deployed image: ${ECR_IMAGE}"
        }
        failure {
            echo 'AutoShip CI/CD pipeline failed. Check the stage logs.'
        }
    }
}
