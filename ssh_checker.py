import paramiko
import socket
import time
from typing import Dict, Any

class SSHConnectivityChecker:
    """SSH connectivity checker class"""
    
    def __init__(self, username: str = "", password: str = "", port: int = 22, timeout: int = 10):
        """
        Initialize SSH connectivity checker
        
        Args:
            username: SSH username (optional)
            password: SSH password (optional)
            port: SSH port (default: 22)
            timeout: Connection timeout in seconds (default: 10)
        """
        self.username = username
        self.password = password
        self.port = port
        self.timeout = timeout
    
    def check_connectivity(self, server: str) -> Dict[str, Any]:
        """
        Check SSH connectivity to a single server
        
        Args:
            server: Server hostname or IP address
            
        Returns:
            Dictionary containing connectivity results
        """
        start_time = time.time()
        result = {
            'server': server,
            'status': 'Unknown',
            'response_time': 'N/A',
            'error': ''
        }
        
        try:
            # Create SSH client
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # Attempt connection
            if self.username and self.password:
                # Use provided credentials
                ssh.connect(
                    hostname=server,
                    port=self.port,
                    username=self.username,
                    password=self.password,
                    timeout=self.timeout,
                    banner_timeout=self.timeout
                )
            else:
                # Try connection without authentication (just to test connectivity)
                try:
                    ssh.connect(
                        hostname=server,
                        port=self.port,
                        timeout=self.timeout,
                        banner_timeout=self.timeout,
                        look_for_keys=False,
                        allow_agent=False
                    )
                except paramiko.AuthenticationException:
                    # Authentication failed, but connection was successful
                    pass
                except paramiko.SSHException as e:
                    if "No authentication methods available" in str(e):
                        # Server is reachable but requires auth
                        pass
                    else:
                        raise e
            
            # Calculate response time
            response_time = round((time.time() - start_time) * 1000, 2)
            result.update({
                'status': 'Connected',
                'response_time': f"{response_time} ms"
            })
            
        except socket.timeout:
            response_time = round((time.time() - start_time) * 1000, 2)
            result.update({
                'status': 'Timeout',
                'response_time': f"{response_time} ms",
                'error': f'Connection timeout after {self.timeout} seconds'
            })
            
        except socket.gaierror as e:
            response_time = round((time.time() - start_time) * 1000, 2)
            result.update({
                'status': 'Failed',
                'response_time': f"{response_time} ms",
                'error': f'DNS resolution failed: {str(e)}'
            })
            
        except ConnectionRefusedError:
            response_time = round((time.time() - start_time) * 1000, 2)
            result.update({
                'status': 'Failed',
                'response_time': f"{response_time} ms",
                'error': f'Connection refused on port {self.port}'
            })
            
        except paramiko.AuthenticationException:
            response_time = round((time.time() - start_time) * 1000, 2)
            result.update({
                'status': 'Connected',
                'response_time': f"{response_time} ms",
                'error': 'Authentication required (but SSH service is running)'
            })
            
        except paramiko.SSHException as e:
            response_time = round((time.time() - start_time) * 1000, 2)
            if "No authentication methods available" in str(e):
                result.update({
                    'status': 'Connected',
                    'response_time': f"{response_time} ms",
                    'error': 'SSH service running (no auth methods configured)'
                })
            else:
                result.update({
                    'status': 'Failed',
                    'response_time': f"{response_time} ms",
                    'error': f'SSH error: {str(e)}'
                })
                
        except Exception as e:
            response_time = round((time.time() - start_time) * 1000, 2)
            result.update({
                'status': 'Error',
                'response_time': f"{response_time} ms",
                'error': f'Unexpected error: {str(e)}'
            })
            
        finally:
            try:
                ssh.close()
            except:
                pass
        
        return result
    
    def check_multiple_servers(self, servers: list) -> list:
        """
        Check SSH connectivity to multiple servers
        
        Args:
            servers: List of server hostnames or IP addresses
            
        Returns:
            List of dictionaries containing connectivity results
        """
        results = []
        for server in servers:
            result = self.check_connectivity(server)
            results.append(result)
        return results
