# Deployment Guide - University Server

This guide covers deploying the Flask chat application on a single university server using Gunicorn or uWSGI.

---

## Prerequisites

- Linux server with Python 3.8+
- SSH access to the server
- Ability to install Python packages
- Port 80/443 access (or alternative port)

---

## Project Structure

```
chat-experiment/
├── app/
│   ├── __init__.py          # Application factory
│   ├── models.py            # Database models
│   ├── routes.py            # Routes and views
│   └── templates/
│       └── chat.html        # Chat interface
├── bot.py                   # Bot logic
├── experimental_conditions.json
├── wsgi.py                  # WSGI entry point
├── requirements.txt
├── db_utils.py             # Database utilities
└── .env                    # Environment variables
```

---

## Installation Steps

### 1. Clone/Upload Your Code

```bash
# On your server
mkdir -p ~/chat-experiment
cd ~/chat-experiment

# Upload your files via scp, git, or file transfer
# Make sure you have all files from the project structure above
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create `.env` file:

```bash
# Azure OpenAI Configuration (Required)
MODEL_ENDPOINT=https://your-resource.openai.azure.com/
MODEL_DEPLOYMENT=gpt-4
MODEL_API_VERSION=2024-02-15-preview
MODEL_SUBSCRIPTION_KEY=your-api-key-here

# Model Parameters (Required)
MODEL_TEMPERATURE=1.0
MODEL_MAX_COMPLETION_TOKENS=2500
MODEL_MAX_RETRIES=5
MODEL_RETRY_DELAY=2.0

# Flask Configuration (Required)
FLASK_SECRET_KEY=your-very-secure-random-key-here

# Security - Iframe Embedding Control (Required for Production)
# Set to your Qualtrics domain to restrict iframe embedding
# Leave blank during development/testing
# Example: ALLOWED_FRAME_ANCESTORS=yourschool.qualtrics.com
ALLOWED_FRAME_ANCESTORS=

# Database - use absolute path for production
DATABASE_URL=sqlite:////home/yourusername/chat-experiment/data/chat_experiment.db
```

**Generate a secure secret key:**
```bash
python -c 'import secrets; print(secrets.token_hex(32))'
```

### 4. Create Data Directory

```bash
mkdir -p data
chmod 755 data
```

### 5. Configure Production Security

**Before launching, configure iframe embedding restrictions:**

```bash
# In your .env file, add your Qualtrics domain:
ALLOWED_FRAME_ANCESTORS=yourschool.qualtrics.com
```

**To find your Qualtrics domain:**
1. Log into Qualtrics
2. Look at the URL: `https://yourschool.az1.qualtrics.com/...`
3. Use everything after `https://` up to the first `/`

**Examples:**
- `yourschool.qualtrics.com`
- `yourschool.az1.qualtrics.com`
- `yourschool.ca1.qualtrics.com`

**Multiple domains (if needed):**
```bash
ALLOWED_FRAME_ANCESTORS=yourschool.qualtrics.com,yourschool.az1.qualtrics.com
```

**Verification:**
After setting this and restarting the app:
- ✅ Chat works when embedded in Qualtrics
- ❌ Chat blocked when embedded on other websites

### 6. Initialize Database

```bash
# Development mode test
python -m flask --app wsgi:app run

# Or just run once to create tables
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
```

---

## Running the Application

### Option 1: Development (Testing Only)

```bash
# Using Flask's built-in server
export FLASK_APP=wsgi:app
python -m flask run --host 0.0.0.0 --port 5000

# Or
python wsgi.py
```

**Note:** Flask's built-in server is NOT suitable for production. Use Gunicorn below.

### Option 2: Production with Gunicorn (Recommended)

```bash
# Basic command
gunicorn --bind 0.0.0.0:5000 wsgi:app

# Production settings
gunicorn \
  --bind 0.0.0.0:5000 \
  --workers 4 \
  --threads 2 \
  --timeout 120 \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log \
  --log-level info \
  wsgi:app
```

**Worker calculation:** `(2 x CPU cores) + 1`
- 2 cores = 5 workers
- 4 cores = 9 workers

### Option 3: Production with uWSGI

Create `uwsgi.ini`:

```ini
[uwsgi]
module = wsgi:app
master = true
processes = 4
threads = 2
socket = 0.0.0.0:5000
protocol = http
chmod-socket = 660
vacuum = true
die-on-term = true
logto = logs/uwsgi.log
```

Run:
```bash
uwsgi --ini uwsgi.ini
```

---

## Setting Up as a System Service

### Using systemd (Most common)

Create `/etc/systemd/system/chat-experiment.service`:

```ini
[Unit]
Description=Chat Experiment Flask App
After=network.target

[Service]
User=yourusername
Group=yourusername
WorkingDirectory=/home/yourusername/chat-experiment
Environment="PATH=/home/yourusername/chat-experiment/venv/bin"
ExecStart=/home/yourusername/chat-experiment/venv/bin/gunicorn \
    --bind 0.0.0.0:5000 \
    --workers 4 \
    --timeout 120 \
    --access-logfile /home/yourusername/chat-experiment/logs/access.log \
    --error-logfile /home/yourusername/chat-experiment/logs/error.log \
    wsgi:app

Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable chat-experiment
sudo systemctl start chat-experiment
sudo systemctl status chat-experiment
```

Manage the service:
```bash
# Stop
sudo systemctl stop chat-experiment

# Restart
sudo systemctl restart chat-experiment

# View logs
sudo journalctl -u chat-experiment -f
```

---

## Setting Up Nginx (Recommended)

### Install Nginx

```bash
sudo apt update
sudo apt install nginx
```

### Configure Nginx

Create `/etc/nginx/sites-available/chat-experiment`:

```nginx
server {
    listen 80;
    server_name your-domain.university.edu;

    # Increase timeout for long-running LLM requests
    proxy_read_timeout 300;
    proxy_connect_timeout 300;
    proxy_send_timeout 300;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support (if needed in future)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # Serve static files directly (if you add any later)
    location /static {
        alias /home/yourusername/chat-experiment/app/static;
        expires 30d;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/chat-experiment /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Add HTTPS (Optional but Recommended)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.university.edu

# Auto-renewal is set up automatically
```

---

## Monitoring and Maintenance

### Check Application Status

```bash
# Service status
sudo systemctl status chat-experiment

# View logs
tail -f logs/error.log
tail -f logs/access.log

# Database stats
python db_utils.py stats
```

### Backup Database

```bash
# Create backup script
cat > backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR=/home/yourusername/backups
DATE=$(date +%Y%m%d_%H%M%S)
cp data/chat_experiment.db $BACKUP_DIR/chat_experiment_$DATE.db
# Keep only last 30 days
find $BACKUP_DIR -name "chat_experiment_*.db" -mtime +30 -delete
EOF

chmod +x backup.sh

# Add to crontab (daily backup at 2 AM)
crontab -e
# Add: 0 2 * * * /home/yourusername/chat-experiment/backup.sh
```

### Log Rotation

Create `/etc/logrotate.d/chat-experiment`:

```
/home/yourusername/chat-experiment/logs/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 yourusername yourusername
    sharedscripts
    postrotate
        systemctl reload chat-experiment > /dev/null 2>&1 || true
    endscript
}
```

---

## Secure Data Export

All data export is handled via command-line tools for security. This requires SSH access to the server.

### Export from Server

```bash
# SSH into your server
ssh yourusername@your-server.university.edu

# Navigate to app directory
cd ~/chat-experiment

# Activate virtual environment
source venv/bin/activate

# Export to JSON (most comprehensive)
python db_utils.py export-json --output data_export_$(date +%Y%m%d).json

# Or export to CSV (conversations format)
python db_utils.py export-conversations --output conversations_$(date +%Y%m%d).csv

# Or export to CSV (messages format)
python db_utils.py export-csv --output messages_$(date +%Y%m%d).csv
```

### Download to Local Machine

From your **local terminal** (not the server):

```bash
# Download JSON export
scp yourusername@your-server.university.edu:~/chat-experiment/data_export_*.json ./

# Or download CSV
scp yourusername@your-server.university.edu:~/chat-experiment/conversations_*.csv ./
```

### Security Benefits

This approach:
- ✅ Requires server SSH authentication
- ✅ No web exposure of sensitive data
- ✅ Creates audit trail in server access logs
- ✅ Leverages existing security infrastructure
- ✅ More flexible export options than web API

### Automated Exports (Optional)

For regular backups, create a cron job:

```bash
# Edit crontab
crontab -e

# Add daily export at 2 AM (after database backup)
0 2 * * * cd /home/yourusername/chat-experiment && source venv/bin/activate && python db_utils.py export-json --output /home/yourusername/backups/export_$(date +\%Y\%m\%d).json
```

---

## Troubleshooting

### Application won't start

```bash
# Check logs
sudo journalctl -u chat-experiment -n 50

# Check if port is already in use
sudo netstat -tulpn | grep 5000

# Test manually
source venv/bin/activate
python wsgi.py
```

### Database permission errors

```bash
# Ensure correct ownership
chown -R yourusername:yourusername data/
chmod 755 data/
chmod 644 data/chat_experiment.db
```

### Nginx 502 Bad Gateway

```bash
# Check if gunicorn is running
sudo systemctl status chat-experiment

# Check nginx error logs
sudo tail -f /var/log/nginx/error.log

# Test gunicorn directly
curl http://127.0.0.1:5000
```

### High memory usage

```bash
# Reduce number of workers in systemd service or gunicorn command
# Monitor memory
htop

# Check SQLite journal size (can grow large)
ls -lh data/
```

---

## Security Checklist

- [ ] Changed `FLASK_SECRET_KEY` to a secure random value
- [ ] Database file has correct permissions (644)
- [ ] `.env` file has restricted permissions (600): `chmod 600 .env`
- [ ] Firewall configured (only ports 80, 443, and SSH open)
- [ ] Running as non-root user
- [ ] HTTPS enabled with valid certificate
- [ ] Regular backups scheduled
- [ ] Log rotation configured
- [ ] API keys not exposed in logs or error messages
- [ ] Data export requires SSH access (no web endpoint)
- [ ] **Set `ALLOWED_FRAME_ANCESTORS` to Qualtrics domain** (prevents unauthorized embedding)
- [ ] **Session token authentication active** (prevents API abuse)
- [ ] **Rate limiting configured** (30/min, 500/day per IP)
- [ ] **Input validation active** (participant IDs, message length)

---

## Updating the Application

```bash
# Stop the service
sudo systemctl stop chat-experiment

# Activate virtual environment
cd ~/chat-experiment
source venv/bin/activate

# Pull updates (if using git)
git pull

# Install any new dependencies
pip install -r requirements.txt

# Restart the service
sudo systemctl start chat-experiment

# Check status
sudo systemctl status chat-experiment
```

---

## URLs After Deployment

Once deployed, your application will be accessible at:

**Direct access:**
- `http://your-domain.university.edu/?participant_id=TEST001&condition=0`

**For Qualtrics:**
Use `https://your-domain.university.edu` as your `CHAT_APP_URL` in the JavaScript code.

---

## Getting Help

**Check status:**
```bash
# Is the service running?
sudo systemctl status chat-experiment

# Are there errors in logs?
tail -50 logs/error.log

# Can you reach it locally?
curl http://127.0.0.1:5000/
```

**Common issues:**
- Port conflicts: Change port in systemd service file
- Permission errors: Check file ownership and permissions
- Database locked: Only one writer at a time with SQLite (normal for low traffic)
- Timeout errors: Increase proxy_read_timeout in nginx config

For university IT support, provide:
- Service status output
- Last 50 lines of error log
- Nginx configuration file