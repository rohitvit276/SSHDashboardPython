# SSH Connectivity Dashboard - Deployment Guide

## Overview
This guide helps you deploy the SSH Connectivity Dashboard to your work environment. The dashboard provides both manual input (up to 5 servers) and file upload capabilities for testing SSH connectivity across multiple servers.

## System Requirements

### Minimum Requirements
- Python 3.11 or newer
- 2GB RAM
- 1GB free disk space
- Network access to target SSH servers

### Supported Operating Systems
- Linux (Ubuntu 20.04+, CentOS 7+, RHEL 8+)
- Windows 10/11 with Python
- macOS 10.15+

## Installation Methods

### Method 1: Direct Python Installation (Recommended)

#### Step 1: Install Python Dependencies
```bash
# Install required packages
pip install streamlit pandas paramiko

# Or using requirements.txt (provided in package)
pip install -r requirements.txt
```

#### Step 2: Copy Application Files
Extract all files to your desired directory:
- `app.py` - Main dashboard application
- `ssh_checker.py` - SSH connectivity logic
- `.streamlit/config.toml` - Server configuration
- `requirements.txt` - Python dependencies

#### Step 3: Run the Dashboard
```bash
# Navigate to application directory
cd /path/to/ssh-dashboard

# Start the dashboard
streamlit run app.py --server.port 5000
```

#### Step 4: Access Dashboard
Open your web browser and navigate to:
- Local access: `http://localhost:5000`
- Network access: `http://your-server-ip:5000`

### Method 2: Docker Deployment

#### Step 1: Create Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy application files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 5000

# Run application
CMD ["streamlit", "run", "app.py", "--server.port", "5000", "--server.address", "0.0.0.0"]
```

#### Step 2: Build and Run Container
```bash
# Build Docker image
docker build -t ssh-dashboard .

# Run container
docker run -p 5000:5000 ssh-dashboard
```

### Method 3: Virtual Environment (Isolated Installation)

#### Step 1: Create Virtual Environment
```bash
# Create virtual environment
python -m venv ssh-dashboard-env

# Activate virtual environment
# On Linux/macOS:
source ssh-dashboard-env/bin/activate
# On Windows:
ssh-dashboard-env\Scripts\activate
```

#### Step 2: Install Dependencies and Run
```bash
# Install dependencies
pip install streamlit pandas paramiko

# Run dashboard
streamlit run app.py --server.port 5000
```

## Configuration Options

### Network Configuration
Edit `.streamlit/config.toml` to customize:

```toml
[server]
headless = true
address = "0.0.0.0"    # Change to "127.0.0.1" for local access only
port = 5000            # Change port if needed
maxUploadSize = 200    # Max file upload size in MB

[theme]
# Uncomment and modify for custom theming
# primaryColor = "#ff6347"
# backgroundColor = "#ffffff"
# secondaryBackgroundColor = "#f0f2f6"
# textColor = "#262730"
```

### Firewall Configuration
Ensure port 5000 (or your chosen port) is open:

```bash
# Ubuntu/Debian
sudo ufw allow 5000

# CentOS/RHEL
sudo firewall-cmd --permanent --add-port=5000/tcp
sudo firewall-cmd --reload
```

## Security Considerations

### Network Security
- Run behind a reverse proxy (nginx/Apache) for production
- Use HTTPS in production environments
- Restrict access to trusted networks only

### SSH Credentials
- Dashboard handles credentials in memory only
- No persistent storage of sensitive information
- Consider using SSH key authentication for production

### Example nginx Configuration
```nginx
server {
    listen 80;
    server_name your-dashboard.company.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Usage Instructions

### Manual Input Mode
1. Enter up to 5 server FQDNs or IP addresses
2. Configure SSH settings in the sidebar (optional)
3. Click "Check Connectivity"
4. View real-time results with status and response times

### File Upload Mode
1. Prepare CSV or TXT file with server list
2. Upload file using the file uploader
3. Preview detected servers
4. Click "Check All Servers"
5. Export results as CSV if needed

### File Format Examples

**CSV Format:**
```csv
server,description
web1.company.com,Web Server 1
db1.company.com,Database Server
192.168.1.10,File Server
```

**TXT Format:**
```text
web1.company.com
db1.company.com
192.168.1.10
```

## Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000

# Kill process if needed
kill -9 <PID>

# Or use different port
streamlit run app.py --server.port 8080
```

#### Permission Denied
```bash
# On Linux, use sudo for ports < 1024
sudo streamlit run app.py --server.port 80

# Or use higher port number (recommended)
streamlit run app.py --server.port 8080
```

#### Module Import Errors
```bash
# Ensure all dependencies are installed
pip install --upgrade streamlit pandas paramiko

# Check Python version
python --version  # Should be 3.11+
```

### Performance Tuning

#### For Large Server Lists
- Dashboard supports up to 10 concurrent connections
- Adjust timeout settings for slower networks
- Consider running during off-peak hours for large scans

#### Memory Usage
- Typical usage: 50-100MB RAM
- Scales with number of concurrent connections
- Results are stored in session state (temporary)

## Support and Maintenance

### Log Files
Dashboard logs are displayed in the terminal where you started the application.

### Updates
To update the dashboard:
1. Stop the running application (Ctrl+C)
2. Replace application files with newer versions
3. Restart the application

### Backup
Important files to backup:
- `app.py`
- `ssh_checker.py`
- `.streamlit/config.toml`
- Any custom server lists

## Contact Information
For technical support or questions about deployment, refer to your internal IT documentation or contact your system administrator.