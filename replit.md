# SSH Connectivity Dashboard

## Overview

This is a Streamlit-based web application that provides SSH connectivity testing capabilities for multiple servers. The application allows users to test SSH connections to a list of servers with configurable parameters like username, password, port, and timeout. It features parallel processing for efficient batch testing and real-time progress tracking.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a simple two-tier architecture:

1. **Frontend Layer**: Streamlit web interface providing user interaction and real-time updates
2. **Backend Layer**: Python-based SSH connectivity testing using paramiko library

The architecture is designed for simplicity and ease of use, with all components running in a single Python process.

## Key Components

### Frontend (app.py)
- **Streamlit Interface**: Provides the web-based user interface
- **Session State Management**: Maintains results and checking status across interactions
- **Progress Tracking**: Real-time progress bars and status updates
- **Parallel Processing Control**: Manages concurrent SSH connection attempts

### Backend (ssh_checker.py)
- **SSHConnectivityChecker Class**: Core functionality for testing SSH connections
- **Paramiko Integration**: Handles SSH protocol communications
- **Error Handling**: Comprehensive error capture and reporting
- **Performance Monitoring**: Response time measurement for each connection

## Data Flow

1. **Input Collection**: User provides server list and optional SSH credentials
2. **Parallel Processing**: Application creates multiple threads to test connections simultaneously
3. **Real-time Updates**: Progress and results are displayed as tests complete
4. **Result Aggregation**: All test results are collected and displayed in a unified format

The application uses ThreadPoolExecutor for concurrent testing, limiting to a maximum of 10 simultaneous connections to prevent overwhelming the system.

## External Dependencies

### Core Libraries
- **Streamlit**: Web application framework for the user interface
- **Paramiko**: SSH2 protocol library for Python
- **Pandas**: Data manipulation and analysis (for results handling)
- **concurrent.futures**: Built-in Python library for parallel processing

### System Dependencies
- **Socket**: Low-level networking interface (Python built-in)
- **Time**: Timing and performance measurement (Python built-in)

## Deployment Strategy

The application is designed for simple deployment scenarios:

1. **Local Development**: Can be run directly using `streamlit run app.py`
2. **Container Deployment**: Suitable for containerization with Docker
3. **Cloud Platforms**: Compatible with Streamlit Cloud, Heroku, and similar platforms

### Configuration Considerations
- No database required - all data is session-based
- Stateless design allows for easy scaling
- Minimal external dependencies for simplified deployment

### Security Considerations
- SSH credentials are handled in-memory only
- No persistent storage of sensitive information
- Configurable timeout prevents hanging connections
- Auto-accept host keys policy (development-friendly but less secure)

The application prioritizes ease of use and quick deployment over complex security measures, making it ideal for internal network testing and development environments.