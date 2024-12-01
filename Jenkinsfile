pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.9'
        APP_PORT = '5000'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup Python Environment') {
    steps {
        sh '''
            python -m venv venv
            . venv/bin/activate
            pip install -r requirements.txt
            mkdir -p test-reports
            mkdir -p security-reports
        '''
    }
}
        
        stage('Security Scan') {
            steps {
                sh '''
                    . venv/bin/activate
                    bandit -r . -f json -o security-reports/bandit-report.json || true
                '''
            }}
        
        stage('Run Tests') {
             steps {
               sh '''
                    . venv/bin/activate
                    mkdir -p test-reports
                    python -m pytest tests/ --junitxml=test-reports/test-results.xml || true
                '''
            }
        }
        
        stage('Deploy with Ansible') {
            steps {
                ansiblePlaybook(
                    playbook: 'ansible/deploy.yml',
                    inventory: 'ansible/inventory.ini'
                )
            }
        }
        
        stage('Security Tests') {
            steps {
               catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                sh '''
                    docker run -t owasp/zap2docker-stable zap-baseline.py -t http://192.168.88.132:5000 || true
                '''
               }
            }
        }
    }
    
    post {
    always {
        junit(
            allowEmptyResults: true,
            testResults: 'test-reports/*.xml',
            skipPublishingChecks: true
        )
        publishHTML(target: [
            allowMissing: true,
            alwaysLinkToLastBuild: true,
            keepAll: true,
            reportDir: 'security-reports',
            reportFiles: 'bandit-report.json',
            reportName: 'Security Report',
            reportTitles: 'Security Scan Results'
        ])
    }
}}
