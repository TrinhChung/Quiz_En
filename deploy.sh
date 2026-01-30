#!/bin/bash

# Script deploy to VPS
# Usage: ./deploy.sh

set -e

# Configuration
SSH_USER="${SSH_USER:-root}"
SSH_HOST="${SSH_HOST:-your-vps-ip}"
SSH_PORT="${SSH_PORT:-22}"
PROJECT_DIR="/home/$SSH_USER/quiz-app"
GITHUB_REPO="${GITHUB_REPO:-TrinhChung/Quiz_En}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}Deploy Quiz App to VPS${NC}"
echo -e "${YELLOW}========================================${NC}"

echo -e "${YELLOW}Pushing code to GitHub...${NC}"
git add .
git commit -m "Deploy: Auto deployment at $(date +%Y-%m-%d\ %H:%M:%S)" || echo "No changes to commit"
git push origin main

echo -e "${GREEN}✓ Code pushed to GitHub${NC}"
echo -e "${YELLOW}GitHub Actions will automatically deploy in a few seconds...${NC}"

# Lấy URL repository từ git
REPO_URL=$(git config --get remote.origin.url | sed 's/.*:\(.*\)\.git/\1/' | sed 's/.*github.com\/\(.*\)/\1/')
echo -e "${YELLOW}Check deployment status:${NC}"
echo -e "${YELLOW}➜ https://github.com/${REPO_URL}/actions${NC}"
echo ""

# Kiểm tra xem có muốn deploy thủ công hay không
read -p "Do you want to deploy manually via SSH? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${GREEN}GitHub Actions will handle the deployment automatically.${NC}"
    echo -e "${YELLOW}If deployment fails, check the logs at the link above.${NC}"
    exit 0
fi

# Kiểm tra SSH key
if [ ! -f ~/.ssh/id_rsa ]; then
    echo -e "${RED}Error: SSH private key not found at ~/.ssh/id_rsa${NC}"
    exit 1
fi

# Test SSH connection
echo -e "${YELLOW}Testing SSH connection...${NC}"
if ! ssh -p $SSH_PORT -o ConnectTimeout=5 $SSH_USER@$SSH_HOST "echo 'SSH connection successful'" > /dev/null; then
    echo -e "${RED}Error: Cannot connect to VPS${NC}"
    exit 1
fi
echo -e "${GREEN}SSH connection successful!${NC}"

# Deploy
echo -e "${YELLOW}Deploying to VPS...${NC}"
ssh -p $SSH_PORT $SSH_USER@$SSH_HOST << EOF
set -e

echo -e "${YELLOW}Checking prerequisites...${NC}"

# Kiểm tra git
if ! command -v git &> /dev/null; then
    echo "Installing git..."
    sudo apt-get update && sudo apt-get install -y git
fi

# Kiểm tra docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker not installed. Please install Docker first.${NC}"
    exit 1
fi

# Kiểm tra docker-compose
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Docker Compose not installed. Your server has Docker Compose v2.39.1${NC}"
fi

# Di chuyển tới thư mục dự án
if [ ! -d "$PROJECT_DIR" ]; then
    echo "Creating project directory..."
    mkdir -p "$PROJECT_DIR"
    cd "$PROJECT_DIR"
    git clone https://github.com/$GITHUB_REPO.git .
else
    cd "$PROJECT_DIR"
    echo "Updating repository..."
    git fetch origin
    git reset --hard origin/main
    git pull origin main
fi

echo -e "${GREEN}Repository ready at $PROJECT_DIR${NC}"

# Dừng container cũ
echo "Stopping old containers..."
docker-compose down || true

# Build và run
echo "Building and starting application..."
docker-compose up -d --build

# Kiểm tra status
sleep 2
if docker-compose ps | grep -q "quiz-app.*Up"; then
    echo -e "${GREEN}Application is running!${NC}"
    echo -e "${GREEN}Access your app at: http://$SSH_HOST:1132${NC}"
else
    echo -e "${RED}Failed to start application${NC}"
    docker-compose logs
    exit 1
fi
EOF

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Deployment completed successfully!${NC}"
echo -e "${GREEN}========================================${NC}"
