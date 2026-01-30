#!/bin/bash

# Rollback script - Restore from backup if deployment fails

set -e

PROJECT_DIR="${1:-.}"
BACKUP_DIR="$PROJECT_DIR/../quiz-app-backups"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}========== Quiz App Rollback Script ==========${NC}"

# 1. Check if backups exist
echo -e "${YELLOW}[1/4] Checking backups...${NC}"
if [ ! -d "$BACKUP_DIR" ]; then
    echo -e "${RED}❌ No backups found at $BACKUP_DIR${NC}"
    exit 1
fi

# 2. List available backups
echo -e "${YELLOW}[2/4] Available backups:${NC}"
ls -lah "$BACKUP_DIR" | grep docker-state | head -5

# 3. Stop current containers
echo -e "${YELLOW}[3/4] Stopping current containers...${NC}"
cd "$PROJECT_DIR"

if docker compose down 2>&1; then
    echo -e "${GREEN}✓ Containers stopped${NC}"
else
    echo -e "${YELLOW}⚠ Warning: Could not stop containers${NC}"
fi

# 4. Restart containers
echo -e "${YELLOW}[4/4] Restarting application...${NC}"
if docker compose up -d 2>&1; then
    echo -e "${GREEN}✓ Containers restarted${NC}"
    sleep 2
    
    # Check health
    if curl -s http://localhost:1132 > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Application restored!${NC}"
        echo -e "${GREEN}   Check: http://$(hostname -I | awk '{print $1}'):1132${NC}"
    else
        echo -e "${RED}❌ Health check failed${NC}"
        docker compose logs
        exit 1
    fi
else
    echo -e "${RED}❌ Failed to restart containers${NC}"
    exit 1
fi

echo -e "${YELLOW}========== Rollback Complete ==========${NC}"
