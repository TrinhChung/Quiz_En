#!/bin/bash

# Check deployment health on VPS
# Usage: ./check_health.sh <vps_host> <vps_port> <ssh_user> <ssh_key>

VPS_HOST="${1:-your-vps-ip}"
VPS_PORT="${2:-22}"
SSH_USER="${3:-root}"
SSH_KEY="${4:-~/.ssh/id_ed25519}"

echo "========== Checking Deployment Health =========="
echo "VPS: $SSH_USER@$VPS_HOST:$VPS_PORT"
echo ""

ssh -i "$SSH_KEY" -p $VPS_PORT $SSH_USER@$VPS_HOST << 'EOF'
PROJECT_DIR="/home/$SSH_USER/quiz-app"

if [ ! -d "$PROJECT_DIR" ]; then
    echo "❌ Project directory not found"
    exit 1
fi

cd "$PROJECT_DIR"

echo "[1] Container Status:"
echo "=========================="
docker compose ps

echo ""
echo "[2] Application Health:"
echo "=========================="
if curl -s http://localhost:1132 > /dev/null 2>&1; then
    echo "✅ HTTP endpoint responding"
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:1132)
    echo "   Status Code: $HTTP_CODE"
else
    echo "❌ HTTP endpoint not responding"
fi

echo ""
echo "[3] Recent Logs (last 30 lines):"
echo "=========================="
docker compose logs --tail=30

echo ""
echo "[4] Resource Usage:"
echo "=========================="
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"

echo ""
echo "[5] Disk Space:"
echo "=========================="
df -h | grep -E "Filesystem|/$"

echo ""
echo "========== Health Check Complete =========="
EOF
