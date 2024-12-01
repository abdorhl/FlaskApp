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
        
       /* stage('Security Scan') {
            steps {
                sh '''
                    . venv/bin/activate
                    mkdir -p security-reports
                    bandit -r . -f json -o security-reports/bandit-report.json || true
                '''
            }}
        */
        
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
                        sudo apt-get update
                        sudo apt-get install -y sshpass
                        export ANSIBLE_HOST_KEY_CHECKING=False
                        ansible-playbook -i ansible/inventory.ini ansible/deploy.yml
                    '''
                }
            }
        }
        
        stage('Security Tests') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                        sh '''
                            mkdir -p security-reports
                            echo "$DOCKER_PASSWORD" | podman login -u "$DOCKER_USERNAME" --password-stdin docker.io
                            podman pull docker.io/owasp/zap2docker-stable:latest
                            podman run -v $(pwd)/security-reports:/zap/wrk/:rw docker.io/owasp/zap2docker-stable:latest zap-baseline.py -t http://192.168.88.132:5000 -r security-reports/zap-report.html || true
                            podman logout docker.io
                        '''
                    }
                }
            }
        }
    }
    
    post {
        always {
            junit allowEmptyResults: true, testResults: 'test-reports/*.xml'
            archiveArtifacts artifacts: 'security-reports/*', allowEmptyArchive: true
            cleanWs()
        }
    }
}
