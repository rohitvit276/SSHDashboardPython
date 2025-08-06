# SSH Connectivity Dashboard

A Streamlit-based web application for testing SSH connectivity across multiple servers with real-time monitoring and batch processing capabilities.

## Features

### 🔧 Dual Input Methods
- **Manual Input**: Quick testing of up to 5 servers
- **File Upload**: Batch processing via CSV or TXT files

### 🚀 Advanced Capabilities
- **Parallel Processing**: Tests multiple servers simultaneously (up to 10 concurrent connections)
- **Real-time Progress**: Live updates with progress bars and status tracking
- **Comprehensive Results**: Shows connection status, response times, and detailed error messages
- **Export Functionality**: Download results as CSV files
- **Flexible Authentication**: Supports both authenticated and unauthenticated SSH testing

### 📊 Professional Interface
- Color-coded status indicators (Connected/Failed/Timeout/Error)
- Summary statistics with percentage breakdowns
- Responsive design suitable for office dashboards
- Session-based results storage

## Quick Start

### Option 1: Automated Setup (Recommended)
```bash
# Run the setup script
python setup.py

# Start the dashboard
streamlit run app.py --server.port 5000
```

### Option 2: Manual Installation
```bash
# Install dependencies
pip install streamlit pandas paramiko

# Start the dashboard
streamlit run app.py --server.port 5000
```

Then open your browser to: `http://localhost:5000`

## File Structure

```
ssh-connectivity-dashboard/
├── app.py                    # Main dashboard application
├── ssh_checker.py           # SSH connectivity logic
├── .streamlit/
│   └── config.toml          # Streamlit server configuration
├── setup.py                 # Automated setup script
├── install_dependencies.txt # Python package requirements
├── deployment_guide.md      # Complete deployment instructions
└── README.md               # This file
```

## Supported File Formats

### CSV Files
Must contain a column with server names/IPs. Supported column names:
- `server`, `hostname`, `fqdn`, `host`, `ip`, `address`

Example:
```csv
server,description
web1.company.com,Web Server 1
db1.company.com,Database Server
192.168.1.10,File Server
```

### TXT Files
One server per line:
```text
web1.company.com
db1.company.com
192.168.1.10
```

## Configuration

### SSH Settings (Configurable via sidebar)
- **Username**: SSH username (optional)
- **Password**: SSH password (optional)
- **Port**: SSH port (default: 22)
- **Timeout**: Connection timeout in seconds (default: 10)

### Server Settings
Edit `.streamlit/config.toml` to customize:
- Server address and port
- File upload size limits
- Theme customization

## Security Notes

- SSH credentials are handled in memory only
- No persistent storage of sensitive information
- Auto-accept host keys policy (suitable for internal networks)
- Configurable timeout prevents hanging connections

## System Requirements

- Python 3.11+
- Network access to target SSH servers
- 2GB RAM (recommended)
- Modern web browser

## Deployment Options

1. **Local Development**: Direct Python execution
2. **Docker**: Containerized deployment
3. **Cloud Platforms**: Compatible with most cloud providers
4. **Enterprise**: Behind reverse proxy with SSL

For detailed deployment instructions, see `deployment_guide.md`.

## Troubleshooting

### Common Issues
- **Port in use**: Use different port with `--server.port 8080`
- **Permission denied**: Use ports > 1024 or run with appropriate permissions
- **Module errors**: Ensure all dependencies are installed

### Performance Tips
- Adjust timeout for slower networks
- Use smaller batches for large server lists
- Run during off-peak hours for extensive scans

## License

This project is designed for internal network monitoring and SSH connectivity testing in enterprise environments.