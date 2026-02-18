pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'django-todo-app'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
        DOCKER_REGISTRY = 'docker.io'  // Change to your registry
        REGISTRY_CREDENTIAL = 'dockerhub-credentials'  // Jenkins credential ID
        APP_NAME = 'todo-app'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code from repository...'
                checkout scm
            }
        }
        
        stage('Environment Setup') {
            steps {
                echo 'Setting up environment variables...'
                sh '''
                    cp .env.example .env
                    echo "Building for environment: ${BRANCH_NAME}"
                '''
            }
        }
        
        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Code Quality Analysis') {
            parallel {
                stage('Linting') {
                    steps {
                        echo 'Running flake8 for code linting...'
                        sh '''
                            . venv/bin/activate
                            pip install flake8
                            flake8 todo_app/ --max-line-length=120 --exclude=migrations || true
                        '''
                    }
                }
                
                stage('Security Scan') {
                    steps {
                        echo 'Running bandit for security analysis...'
                        sh '''
                            . venv/bin/activate
                            pip install bandit
                            bandit -r todo_app/ -f json -o bandit-report.json || true
                        '''
                    }
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                echo 'Running Django tests...'
                sh '''
                    . venv/bin/activate
                    python manage.py test --verbosity=2
                '''
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                script {
                    docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                    docker.build("${DOCKER_IMAGE}:latest")
                }
            }
        }
        
        stage('Docker Security Scan') {
            steps {
                echo 'Scanning Docker image for vulnerabilities...'
                sh '''
                    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
                        aquasec/trivy image ${DOCKER_IMAGE}:${DOCKER_TAG} || true
                '''
            }
        }
        
        stage('Push to Registry') {
            when {
                branch 'main'
            }
            steps {
                echo 'Pushing Docker image to registry...'
                script {
                    docker.withRegistry("https://${DOCKER_REGISTRY}", REGISTRY_CREDENTIAL) {
                        docker.image("${DOCKER_IMAGE}:${DOCKER_TAG}").push()
                        docker.image("${DOCKER_IMAGE}:latest").push()
                    }
                }
            }
        }
        
        stage('Deploy to Staging') {
            when {
                branch 'develop'
            }
            steps {
                echo 'Deploying to staging environment...'
                sh '''
                    docker-compose -f docker-compose.staging.yml down
                    docker-compose -f docker-compose.staging.yml up -d
                    docker-compose -f docker-compose.staging.yml exec -T web python manage.py migrate
                '''
            }
        }
        
        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                echo 'Deploying to production environment...'
                input message: 'Deploy to Production?', ok: 'Deploy'
                sh '''
                    docker-compose -f docker-compose.prod.yml down
                    docker-compose -f docker-compose.prod.yml pull
                    docker-compose -f docker-compose.prod.yml up -d
                    docker-compose -f docker-compose.prod.yml exec -T web python manage.py migrate --noinput
                    docker-compose -f docker-compose.prod.yml exec -T web python manage.py collectstatic --noinput
                '''
            }
        }
        
        stage('Health Check') {
            steps {
                echo 'Performing health check...'
                sh '''
                    sleep 10
                    curl -f http://localhost:8000 || exit 1
                '''
            }
        }
    }
    
    post {
        always {
            echo 'Cleaning up workspace...'
            cleanWs()
        }
        
        success {
            echo 'Pipeline completed successfully!'
            // Send notification (email, Slack, etc.)
        }
        
        failure {
            echo 'Pipeline failed!'
            // Send failure notification
        }
    }
}