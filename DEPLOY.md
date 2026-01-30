# Deploy Hướng Dẫn

## Cập nhật: Port 1132 & Deployment Safety

Ứng dụng hiện đã được cấu hình để chạy trên **port 1132** thay vì 5000 với **deployment safety checks**.

## 📋 Mục lục

1. [Cấu hình GitHub Secrets](#1-cấu-hình-github-secrets)
2. [Automatic Deployment](#2-automatic-deployment-cicd)
3. [Deployment Safety Features](#3-deployment-safety-features)
4. [Health Check](#4-health-check)
5. [Rollback Strategy](#5-rollback-strategy)
6. [Monitoring](#6-monitoring)
7. [Troubleshooting](#7-troubleshooting)

## 1. Cấu hình GitHub Secrets

Trước tiên, hãy thiết lập các secrets trong repository GitHub của bạn:

1. Đi tới **Settings > Secrets and variables > Actions**
2. Thêm các secrets sau:
   - `SSH_HOST`: IP hoặc domain của VPS
   - `SSH_PORT`: SSH port (thường là 22)
   - `SSH_USER`: Username SSH (thường là root hoặc user khác)
   - `SSH_PRIVATE_KEY`: Nội dung của private SSH key (Ed25519 format)
   - `GEMINI_API_KEY`: API key của bạn

## 2. Automatic Deployment (CI/CD)

Ứng dụng sẽ tự động deploy khi bạn push tới branch `main`:

```bash
git add .
git commit -m "Update code"
git push origin main
```

GitHub Actions sẽ tự động thực hiện:
- ✅ Check prerequisites (Git, Docker)
- ✅ Clone/update code từ repository
- ✅ Backup trước deploy
- ✅ Build Docker image
- ✅ Start container
- ✅ Health check (7 bước kiểm tra)
- ✅ Save logs

## 3. Deployment Safety Features

### 3.1 Pre-Deployment Checks
```yaml
[1/7] Checking prerequisites
      - Git installed
      - Docker installed
```

### 3.2 Backup Strategy
```yaml
[2/7] Creating backup directory
[5/7] Backing up current state
      - Docker state snapshot
      - Application logs
      - Deployment logs
```

Backups được lưu tại: `/home/SSH_USER/quiz-app-backups/`

### 3.3 Environment Configuration
```yaml
[4/7] Setting up environment
      - .env file created/updated
      - GEMINI_API_KEY configured
      - SECRET_KEY generated
```

### 3.4 Health Check (Chi tiết)
```yaml
[6/7] Deploying application
[7/7] Performing health checks
      ✓ Container is running
      ✓ HTTP endpoint responding (http://localhost:1132)
      ✓ Max retries: 10 attempts with 2s interval
```

## 4. Health Check

### 4.1 Automatic Health Check (sau deploy)
```bash
# Đã được tích hợp trong CI/CD
curl -s http://localhost:1132
```

### 4.2 Manual Health Check
```bash
# Chạy trên local machine
./check_health.sh <VPS_IP> <SSH_PORT> <SSH_USER> [<SSH_KEY>]

# Ví dụ
./check_health.sh 203.0.113.10 22 root ~/.ssh/id_ed25519
```

Script sẽ kiểm tra:
- Container status
- HTTP endpoint
- Recent logs
- Resource usage
- Disk space

### 4.3 SSH vào VPS để check
```bash
ssh -p YOUR_SSH_PORT USERNAME@YOUR_VPS_IP

# Check container
cd /home/YOUR_USER/quiz-app
docker compose ps
docker compose logs -f web

# Check API endpoint
curl http://localhost:1132
```

## 5. Rollback Strategy

### 5.1 Automatic Rollback (nếu health check fail)
CI/CD workflow sẽ **tự động dừng và không tiếp tục** nếu:
- Container fail to start
- Health check timeout
- HTTP endpoint không respond

Lúc đó:
1. Tất cả logs được save trong `/home/SSH_USER/quiz-app-backups/`
2. Containers được stop
3. Deployment fail và notify

### 5.2 Manual Rollback
```bash
# SSH vào VPS
ssh -p YOUR_SSH_PORT USERNAME@YOUR_VPS_IP

# Chạy rollback script
cd /home/YOUR_USER/quiz-app
bash ../../rollback.sh

# hoặc từ local
./rollback.sh /home/YOUR_USER/quiz-app
```

Script sẽ:
- Stop current containers
- Restart từ backup
- Health check

### 5.3 Manual Git Rollback
```bash
ssh -p YOUR_SSH_PORT USERNAME@YOUR_VPS_IP

cd /home/YOUR_USER/quiz-app

# Xem history commits
git log --oneline | head -10

# Rollback to specific commit
git reset --hard <COMMIT_HASH>

# Rebuild and restart
docker compose down
docker compose up -d --build
```

## 6. Monitoring

### 6.1 GitHub Actions Logs
```
https://github.com/TrinhChung/Quiz_En/actions
```

Xem:
- Deployment status
- Build logs
- Health check results
- Errors

### 6.2 VPS Logs

```bash
# Recent backup/deployment logs
ls -lah /home/YOUR_USER/quiz-app-backups/

# View specific log
cat /home/YOUR_USER/quiz-app-backups/deploy-20260130_120000.log

# View error logs
cat /home/YOUR_USER/quiz-app-backups/error-20260130_120000.log
```

### 6.3 Application Logs

```bash
ssh -p YOUR_SSH_PORT USERNAME@YOUR_VPS_IP

cd /home/YOUR_USER/quiz-app

# Real-time logs
docker compose logs -f

# Last N lines
docker compose logs --tail=100

# Specific service
docker compose logs web
```

### 6.4 System Health

```bash
# Check disk space
df -h

# Check memory
free -h

# Check CPU
top -bn1 | head -20

# Check Docker
docker ps -a
docker stats
```

## 7. Troubleshooting

### 7.1 Deployment Failed - "Docker not found"
**Giải pháp:**
```bash
ssh -p YOUR_SSH_PORT USERNAME@YOUR_VPS_IP

# Install Docker
curl -fsSL https://get.docker.com | bash

# Add user to docker group
sudo usermod -aG docker $USER

# Verify
docker --version
```

### 7.2 Health Check Timeout
**Nguyên nhân:**
- App startup chậm
- Port 1132 đã được sử dụng
- Memory không đủ

**Giải pháp:**
```bash
# Check port
lsof -i :1132

# Kill process if needed
sudo kill -9 <PID>

# Check memory
free -h

# Check logs
docker compose logs
```

### 7.3 Container Fails to Start
```bash
cd /home/YOUR_USER/quiz-app

# Check logs
docker compose logs web

# Try manual build
docker compose build --no-cache

# Try restart
docker compose restart web
```

### 7.4 .env File Lost
```bash
cd /home/YOUR_USER/quiz-app

# Recreate .env
cat > .env << EOF
GEMINI_API_KEY=YOUR_KEY
SECRET_KEY=$(openssl rand -hex 32)
EOF

# Restart
docker compose restart web
```

### 7.5 Port Already in Use
```bash
# Find what's using port 1132
sudo lsof -i :1132

# Kill it (if it's old process)
sudo kill -9 <PID>

# Or change docker-compose port mapping and update nginx
```

## 8. Best Practices

### 8.1 Deployment Checklist
- [ ] Test locally first
- [ ] Check GitHub Actions for any secrets missing
- [ ] Verify SSH key is Ed25519 format
- [ ] Run health check after deploy
- [ ] Check logs on VPS
- [ ] Monitor for 5-10 minutes after deploy

### 8.2 Code Changes
```bash
# Before pushing
git status                          # Check changes
git diff                            # Review changes
python -m pytest tests/             # Run tests locally

# Push with clear commit message
git add .
git commit -m "Feature: Add new feature"
git push origin main

# Monitor
# Check: https://github.com/TrinhChung/Quiz_En/actions
```

### 8.3 Environment Variables
```bash
# Never commit .env
echo ".env" >> .gitignore

# Keep GEMINI_API_KEY safe
# Use GitHub Secrets, not plain text
```

### 8.4 Regular Backups
```bash
# On VPS, periodic backup of backups directory
cd /home/YOUR_USER
tar -czf quiz-app-backup-$(date +%Y%m%d).tar.gz quiz-app-backups/

# Upload to cloud storage periodically
```

## 9. File cấu hình liên quan

| File | Mô tả |
|------|-------|
| `.github/workflows/deploy.yml` | CI/CD workflow - deployment automation |
| `docker-compose.yml` | Docker configuration (port: 1132) |
| `Dockerfile` | Container image (port: 1132) |
| `rollback.sh` | Manual rollback script |
| `check_health.sh` | Health check script |
| `deploy.sh` | Local deployment script |

## 10. Support

Nếu gặp vấn đề:
1. Check GitHub Actions logs
2. Check VPS logs tại `/home/YOUR_USER/quiz-app-backups/`
3. Run `./check_health.sh`
4. Check application logs: `docker compose logs`
