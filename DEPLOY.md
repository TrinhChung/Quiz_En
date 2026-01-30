# Deploy Hướng Dẫn

## Cập nhật: Port 1132

Ứng dụng hiện đã được cấu hình để chạy trên **port 1132** thay vì 5000.

## 1. Cấu hình GitHub Secrets

Trước tiên, hãy thiết lập các secrets trong repository GitHub của bạn:

1. Đi tới **Settings > Secrets and variables > Actions**
2. Thêm các secrets sau:
   - `SSH_HOST`: IP hoặc domain của VPS
   - `SSH_PORT`: SSH port (thường là 22)
   - `SSH_USER`: Username SSH (thường là root hoặc user khác)
   - `SSH_PRIVATE_KEY`: Nội dung của private SSH key (bắt đầu với `-----BEGIN RSA PRIVATE KEY-----`)
   - `GEMINI_API_KEY`: API key của bạn

## 2. Automatic Deployment (CI/CD)

Ứng dụng sẽ tự động deploy khi bạn push tới branch `main`:

```bash
git add .
git commit -m "Update port to 1132"
git push origin main
```

GitHub Actions sẽ tự động:
- SSH vào VPS của bạn
- Clone hoặc update code từ repository
- Build Docker image
- Start container trên port 1132

Theo dõi deployment tại: `https://github.com/YOUR_USERNAME/Quiz_En/actions`

## 3. Manual Deployment (Local Script)

Nếu muốn deploy thủ công từ máy local:

### Yêu cầu:
- SSH key đã được setup tại `~/.ssh/id_rsa`
- Có quyền SSH truy cập VPS

### Cách sử dụng:

```bash
# Setup environment variables (tuỳ chọn)
export SSH_USER=your_username
export SSH_HOST=your_vps_ip
export SSH_PORT=22
export GITHUB_REPO=TrinhChung/Quiz_En

# Chạy script deploy
./deploy.sh
```

## 4. Yêu cầu trên VPS

VPS của bạn phải có:
- ✅ Docker Compose v2.39.1 (bạn đã có)
- ✅ Docker (nếu chưa có, script sẽ kiểm tra)
- ✅ Git (nếu chưa có, script sẽ cài đặt)

## 5. Kiểm tra Deployment

Sau khi deploy, kiểm tra:

```bash
# SSH vào VPS
ssh -p YOUR_SSH_PORT USERNAME@YOUR_VPS_IP

# Kiểm tra docker containers
cd /home/YOUR_USER/quiz-app
docker-compose ps

# Xem logs
docker-compose logs -f web

# Kiểm tra ứng dụng
curl http://localhost:1132
```

## 6. Cấu hình Firewall

Đảm bảo port 1132 được mở trên VPS:

```bash
# UFW (nếu sử dụng)
sudo ufw allow 1132/tcp

# hoặc AWS Security Group, DigitalOcean Firewall, etc.
```

## 7. Reverse Proxy (Tuỳ chọn)

Nếu bạn muốn sử dụng domain với SSL, hãy cấu hình Nginx/Apache:

### Ví dụ Nginx:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:1132;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Sau đó cài đặt SSL:
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## 8. Troubleshooting

### SSH connection refused
- Kiểm tra IP VPS có đúng không
- Kiểm tra SSH port có mở không
- Kiểm tra private key có quyền đúng: `chmod 600 ~/.ssh/id_rsa`

### Docker command not found on VPS
- Cài đặt Docker: `curl -fsSL https://get.docker.com | sudo bash`
- Cấu hình quyền: `sudo usermod -aG docker $USER`

### Port 1132 already in use
```bash
# Tìm process sử dụng port
sudo lsof -i :1132

# Kill process
sudo kill -9 <PID>
```

### Environment variables not found
- Kiểm tra file `.env` trên VPS: `cat /home/YOUR_USER/quiz-app/.env`
- Thêm biến nếu thiếu
- Restart container: `docker-compose restart web`

## 9. Cập nhật ứng dụng

Để cập nhật ứng dụng:

1. **Automatic**: Push code lên main branch, GitHub Actions sẽ tự động deploy
2. **Manual**: Chạy `./deploy.sh` từ local

## File cấu hình liên quan

- `.github/workflows/deploy.yml` - CI/CD workflow
- `docker-compose.yml` - Docker Compose configuration (port: 1132)
- `Dockerfile` - Container configuration (port: 1132)
- `run.py` - Development server port (1132)
- `deploy.sh` - Manual deploy script
