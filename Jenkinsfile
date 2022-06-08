pipeline {
    agent any

    stages{
        stage('Build') {
            steps {
                sh 'docker build --tag tests .'
            }
        }
        stage('Tests') {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    sh """docker run --name my_first_container_from_dockerfile \
			   --network selenoid \
			   tests pytest"""
                }
            }
        }
        stage('Copy Artefact') {
            steps {
                sh 'docker cp test_run:/app/allure-results .'
            }
        }
        stage('Remove container') {
            steps {
                sh 'docker rm my_first_container_from_dockerfile'
            }
        }
        stage('report-allure') {
            steps {
                script {
                    allure([
                        includeProperties: false,
                        jdk: '',
                        properties: [],
                        reportBuildPolicy: 'ALWAYS',
                        results: [[path: 'allure-results']]
                    ])
                }
            }
        }
    }
}