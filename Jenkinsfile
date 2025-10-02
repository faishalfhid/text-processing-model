pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIAL_ID = 'cicd-jenkins-test-token'
        DOCKERHUB_REGISTRY = 'https://registry.hub.docker.com'
        DOCKERHUB_REPOSITORY = 'akmalzakia/text-processing-cicd'
        MODELS_PATH = 'models'
        NOTEBOOKS_PATH = 'notebooks'
        SCRIPTS_PATH = 'scripts'
    }
    stages {
        stage('Clone Repository') {
            steps {
                script {
                    echo 'Cloning Repository'
                    checkout scmGit(
                        branches: [[name: '*/main']],
                        extensions: [],
                        userRemoteConfigs: [[
                            credentialsId: 'text-processing-cicd-cred',
                            url: 'https://github.com/faishalfhid/text-processing-model.git'
                        ]]
                    )
                    sh 'python -m pip install --break-system-packages -r requirements.txt'
                }
            }
        }
        stage('Convert Notebooks') {
            steps {
                script {
                    echo 'Converting to Scripts'
                    sh "mkdir -p ${SCRIPTS_PATH}"
                    sh "jupyter nbconvert --to script ${NOTEBOOKS_PATH}/*.ipynb --output-dir ${SCRIPTS_PATH}"
                }
            }
        }
        stage('Format Code') {
            steps {
                script {
                    echo 'Formatting Python code with Black...'
                    sh "black app.py ${SCRIPTS_PATH}"
                }
            }
        }
        stage('Lint Python Scripts') {
            steps {
                script {
                    echo 'Linting Python scripts with Pylint...'
                    sh "pylint ${SCRIPTS_PATH} --output=pylint-report.txt --exit-zero"
                }
            }
        }
        stage('Filesystem Vulnerability Scan') {
            steps {
                script {
                    echo 'Scanning Filesystem with Trivy...'
                    sh 'trivy fs --format table -o trivy-fs-report.html .'
                }
            }
        }
        stage('Unit Test') {
            steps {
                script {
                    echo 'Running unit tests...'
                    sh 'python -m unittest discover -s tests'
                }
            }
        }
        stage('Model Preprocessing') {
            steps {
                dir(SCRIPTS_PATH) {
                    echo 'Model Preprocessing...'
                    sh 'python cleaning.py'
                }
            }
        }
        stage('Model Training') {
            steps {
                dir(SCRIPTS_PATH) {
                    echo 'Training Model...'
                    sh 'python train.py'
                }
            }
        }
        stage('Model Evaluation') {
            steps {
                dir(SCRIPTS_PATH) {
                    echo 'Evaluating Model...'
                    sh 'python eval.py'
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker Image...'
                    dockerImage = docker.build("${DOCKERHUB_REPOSITORY}:latest")
                }
            }
        }
        stage('Trivy Docker Image Scan') {
            steps {
                script {
                    echo 'Scanning Docker Image with Trivy...'
                    sh "trivy image --format table -o trivy-image-report.html ${DOCKERHUB_REPOSITORY}:latest"
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    echo 'Pushing Docker Image...'
                    docker.withRegistry("${DOCKERHUB_REGISTRY}", "${DOCKERHUB_CREDENTIAL_ID}") {
                        dockerImage.push('latest')
                    }
                }
            }
        }
    }
}
