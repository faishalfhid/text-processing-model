pipeline {
	agent any
	environment {
        DOCKERHUB_CREDENTIAL_ID = 'cicd-jenkins-test-token'
        DOCKERHUB_REGISTRY = 'https://registry.hub.docker.com'
        DOCKERHUB_REPOSITORY = 'akmalzakia/text-processing-cicd'
				MODELS_PATH = 'models'
				NOTEBOOKS_PATH = 'notebooks'
				DATASET_PATH = 'datasets'
				SCRIPTS_PATH = 'scripts'
    }
	stages {
		stage('Clone Repository') {
			steps {
				script {
					echo 'Cloning Repository'
					checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'text-processing-cicd-cred', url: 'https://github.com/faishalfhid/text-processing-model.git']])
          sh "python -m pip install --break-system-packages -r requirements.txt"
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
		stage('Code Quality & Security') {
				stages {
						stage('Format Code') {
								steps {
										echo "Formatting Python code with Black..."
										sh "black app.py ${SCRIPTS_PATH}"
								}
						}
						stage('Lint Python Scripts') {
								steps {
										echo 'Linting Python scripts with Pylint...'
										sh "pylint ${SCRIPTS_PATH} --output=pylint-report.txt --exit-zero"
								}
						}
						stage('Filesystem Vulnerability Scan') {
								steps {
										echo 'Scanning Filesystem with Trivy...'
										sh "trivy fs --format table -o trivy-fs-report.html ." // Scan the whole directory
								}
						}
				}
		}
		stage('Model Preprocessing') {
			steps {
				dir('scripts') {
					echo "Model Preprocessing..."
					sh "python cleaning.py"
				}
			}
		}
		stage('Model Training') {
			steps {
				dir('scripts') {
					echo "Model Preprocessing..."
					sh "python train.py"
				}
			}
		}
		stage('Build Docker Image') {
			stages {
				stage('Build Image') {
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
			}
		}
		stage('Push Docker Image') {
			steps {
				script {
					echo 'Pushing Docker Image to DockerHub...'
					docker.withRegistry("${DOCKERHUB_REGISTRY}", "${DOCKERHUB_CREDENTIAL_ID}"){
						dockerImage.push('latest')
					}
				}
			}
		}
	}
}