#!/bin/bash

# Jenkins Setup Script for Django Todo App
# This script helps you set up Jenkins for CI/CD

set -e

echo "🚀 Jenkins Setup for Django Todo App"
echo "===================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"
echo ""

# Start Jenkins
echo "📦 Starting Jenkins server..."
docker-compose -f docker-compose.jenkins.yml up -d jenkins

echo ""
echo "⏳ Waiting for Jenkins to start (this may take a minute)..."
sleep 30

# Get initial admin password
echo ""
echo "🔑 Getting Jenkins initial admin password..."
JENKINS_PASSWORD=$(docker exec jenkins_server cat /var/jenkins_home/secrets/initialAdminPassword 2>/dev/null || echo "Password not available yet")

echo ""
echo "✅ Jenkins is starting!"
echo ""
echo "📋 Setup Instructions:"
echo "====================="
echo ""
echo "1. Open your browser and go to: http://localhost:8080"
echo ""
echo "2. Use this initial admin password:"
echo "   ${JENKINS_PASSWORD}"
echo ""
echo "3. Install suggested plugins"
echo ""
echo "4. Create your admin user"
echo ""
echo "5. Install additional plugins:"
echo "   - Docker Pipeline"
echo "   - GitHub Integration"
echo "   - Pipeline"
echo "   - Blue Ocean (optional, for better UI)"
echo ""
echo "6. Configure Jenkins:"
echo "   - Add Docker Hub credentials (if pushing images)"
echo "   - Set up GitHub webhook (for automatic builds)"
echo ""
echo "📖 For detailed setup instructions, see JENKINS_GUIDE.md"
echo ""

# Check Jenkins status
echo "🔍 Checking Jenkins container status..."
docker ps | grep jenkins_server

echo ""
echo "✅ Setup complete!"
echo ""
echo "To view Jenkins logs:"
echo "  docker logs -f jenkins_server"
echo ""
echo "To stop Jenkins:"
echo "  docker-compose -f docker-compose.jenkins.yml down"
echo ""