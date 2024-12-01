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
                '''
            }
        }
        
        stage('Security Scan') {
            steps {
                sh '''
                    . venv/bin/activate
                    bandit -r . -f json -o bandit-report.json
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest tests/
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
                sh '''
                    # Exécuter OWASP ZAP
                    docker run -t owasp/zap2docker-stable zap-baseline.py -t http://your-app-url:5000
                '''
            }
        }
    }
    
    post {
        always {
            junit 'test-reports/*.xml'
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: false,
                keepAll: true,
                reportDir: 'security-reports',
                reportFiles: 'bandit-report.html',
                reportName: 'Security Report'
            ])
        }
    }
}
