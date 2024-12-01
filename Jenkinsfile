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
                    mkdir -p security-reports
                    bandit -r . -f json -o security-reports/bandit-report.json || true
                '''
            }
        }
        
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
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    sh '''
                        ansible-playbook -i ansible/inventory.ini ansible/deploy.yml
                    '''
                }
            }
        }
        
        stage('Security Tests') {
            steps {
               catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                sh '''
                    mkdir -p security-reports
                    docker run -v $(pwd)/security-reports:/zap/wrk/:rw -t owasp/zap2docker-stable zap-baseline.py -t http://192.168.88.132:5000 -r security-reports/zap-report.html || true
                '''
               }
            }
        }
    }
    
    post {
        always {
            junit(
                allowEmptyResults: true,
                testResults: 'test-reports/*.xml'
            )
            
            archiveArtifacts(
                artifacts: 'security-reports/*',
                allowEmptyArchive: true,
                fingerprint: true
            )
        }
    }
}
