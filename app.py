import streamlit as st
import pandas as pd
import io
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from ssh_checker import SSHConnectivityChecker

# Configure page
st.set_page_config(
    page_title="SSH Connectivity Dashboard",
    page_icon="🔌",
    layout="wide"
)

# Initialize session state
if 'results' not in st.session_state:
    st.session_state.results = []
if 'checking' not in st.session_state:
    st.session_state.checking = False

def reset_results():
    """Reset results and checking state"""
    st.session_state.results = []
    st.session_state.checking = False

def check_ssh_connectivity(servers, username="", password="", port=22, timeout=10):
    """Check SSH connectivity for multiple servers with progress tracking"""
    if not servers:
        return []
    
    checker = SSHConnectivityChecker(username, password, port, timeout)
    results = []
    
    # Create progress containers
    progress_bar = st.progress(0)
    status_text = st.empty()
    results_container = st.container()
    
    total_servers = len(servers)
    completed = 0
    
    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor(max_workers=min(10, total_servers)) as executor:
        # Submit all tasks
        future_to_server = {
            executor.submit(checker.check_connectivity, server): server 
            for server in servers
        }
        
        # Process completed tasks
        for future in as_completed(future_to_server):
            server = future_to_server[future]
            try:
                result = future.result()
                results.append(result)
                completed += 1
                
                # Update progress
                progress = completed / total_servers
                progress_bar.progress(progress)
                status_text.text(f"Checking connectivity... {completed}/{total_servers} completed")
                
                # Display intermediate results
                with results_container:
                    display_results(results)
                
            except Exception as e:
                # Handle individual server check failures
                error_result = {
                    'server': server,
                    'status': 'Error',
                    'response_time': 'N/A',
                    'error': str(e)
                }
                results.append(error_result)
                completed += 1
                
                progress = completed / total_servers
                progress_bar.progress(progress)
                status_text.text(f"Checking connectivity... {completed}/{total_servers} completed")
    
    # Clear progress indicators
    progress_bar.empty()
    status_text.text("✅ Connectivity check completed!")
    
    return results

def display_results(results):
    """Display results in a formatted table"""
    if not results:
        return
    
    df = pd.DataFrame(results)
    
    # Apply color coding based on status
    def style_status(val):
        if val == 'Connected':
            return 'background-color: #d4edda; color: #155724'
        elif val == 'Failed':
            return 'background-color: #f8d7da; color: #721c24'
        elif val == 'Timeout':
            return 'background-color: #fff3cd; color: #856404'
        else:
            return 'background-color: #f8d7da; color: #721c24'
    
    # Style the dataframe
    styled_df = df.style.map(style_status, subset=['status'])
    
    st.dataframe(styled_df, use_container_width=True)

def parse_uploaded_file(uploaded_file):
    """Parse uploaded CSV or TXT file to extract server list"""
    try:
        if uploaded_file.name.endswith('.csv'):
            # Read CSV file
            df = pd.read_csv(uploaded_file)
            
            # Try to find server column (common column names)
            server_columns = ['server', 'hostname', 'fqdn', 'host', 'ip', 'address']
            server_col = None
            
            for col in server_columns:
                if col.lower() in [c.lower() for c in df.columns]:
                    server_col = col
                    break
            
            if server_col is None and len(df.columns) > 0:
                # Use first column if no standard column found
                server_col = df.columns[0]
                st.warning(f"No standard server column found. Using '{server_col}' as server names.")
            
            if server_col:
                servers = df[server_col].dropna().astype(str).tolist()
                return [server.strip() for server in servers if server.strip()]
            else:
                st.error("Could not find server data in CSV file.")
                return []
                
        elif uploaded_file.name.endswith('.txt'):
            # Read TXT file (one server per line)
            content = uploaded_file.read().decode('utf-8')
            servers = [line.strip() for line in content.split('\n') if line.strip()]
            return servers
        else:
            st.error("Unsupported file format. Please upload CSV or TXT files only.")
            return []
            
    except Exception as e:
        st.error(f"Error parsing file: {str(e)}")
        return []

def main():
    st.title("🔌 SSH Connectivity Dashboard")
    st.markdown("Check SSH connectivity for multiple servers using manual input or file upload")
    
    # Sidebar for SSH configuration
    st.sidebar.header("SSH Configuration")
    ssh_username = st.sidebar.text_input("Username (optional)", placeholder="ssh_user")
    ssh_password = st.sidebar.text_input("Password (optional)", type="password", placeholder="ssh_password")
    ssh_port = st.sidebar.number_input("SSH Port", min_value=1, max_value=65535, value=22)
    ssh_timeout = st.sidebar.number_input("Timeout (seconds)", min_value=1, max_value=300, value=10)
    
    # Main interface tabs
    tab1, tab2 = st.tabs(["Manual Input", "File Upload"])
    
    with tab1:
        st.header("Manual Server Input")
        st.markdown("Enter up to 5 server FQDNs or IP addresses for quick connectivity checks")
        
        # Manual input form
        with st.form("manual_input_form"):
            servers = []
            for i in range(5):
                server = st.text_input(f"Server {i+1}", placeholder="example.com or 192.168.1.1", key=f"server_{i}")
                if server.strip():
                    servers.append(server.strip())
            
            col1, col2 = st.columns([1, 4])
            with col1:
                submit_manual = st.form_submit_button("Check Connectivity", type="primary")
            with col2:
                if st.form_submit_button("Clear Results"):
                    reset_results()
                    st.rerun()
        
        if submit_manual and servers:
            st.session_state.checking = True
            st.session_state.results = check_ssh_connectivity(
                servers, ssh_username, ssh_password, ssh_port, ssh_timeout
            )
            st.session_state.checking = False
    
    with tab2:
        st.header("File Upload")
        st.markdown("Upload a CSV or TXT file containing server lists for batch connectivity checks")
        
        # File format instructions
        with st.expander("📋 File Format Requirements"):
            st.markdown("""
            **CSV Format:**
            - Must contain a column with server names/IPs
            - Supported column names: server, hostname, fqdn, host, ip, address
            - If none found, first column will be used
            
            **TXT Format:**
            - One server name/IP per line
            - Empty lines will be ignored
            
            **Example CSV:**
            ```
            server,description
            web1.example.com,Web Server 1
            db1.example.com,Database Server
            192.168.1.10,File Server
            ```
            
            **Example TXT:**
            ```
            web1.example.com
            db1.example.com
            192.168.1.10
            ```
            """)
        
        # File upload
        uploaded_file = st.file_uploader(
            "Choose a CSV or TXT file",
            type=['csv', 'txt'],
            help="Upload a file containing server names or IP addresses"
        )
        
        if uploaded_file is not None:
            servers = parse_uploaded_file(uploaded_file)
            
            if servers:
                st.success(f"✅ Found {len(servers)} servers in uploaded file")
                
                # Show preview of servers
                with st.expander(f"Preview servers ({min(10, len(servers))} of {len(servers)})"):
                    preview_servers = servers[:10]
                    for i, server in enumerate(preview_servers, 1):
                        st.write(f"{i}. {server}")
                    if len(servers) > 10:
                        st.write(f"... and {len(servers) - 10} more")
                
                col1, col2 = st.columns([1, 4])
                with col1:
                    if st.button("Check All Servers", type="primary"):
                        st.session_state.checking = True
                        st.session_state.results = check_ssh_connectivity(
                            servers, ssh_username, ssh_password, ssh_port, ssh_timeout
                        )
                        st.session_state.checking = False
                
                with col2:
                    if st.button("Clear Results"):
                        reset_results()
                        st.rerun()
    
    # Display results section
    if st.session_state.results:
        st.header("📊 Connectivity Results")
        
        # Summary statistics
        df = pd.DataFrame(st.session_state.results)
        total = len(df)
        connected = len(df[df['status'] == 'Connected'])
        failed = len(df[df['status'] == 'Failed'])
        timeout = len(df[df['status'] == 'Timeout'])
        error = len(df[df['status'] == 'Error'])
        
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Total", total)
        col2.metric("Connected", connected, delta=f"{connected/total*100:.1f}%" if total > 0 else "0%")
        col3.metric("Failed", failed, delta=f"{failed/total*100:.1f}%" if total > 0 else "0%")
        col4.metric("Timeout", timeout, delta=f"{timeout/total*100:.1f}%" if total > 0 else "0%")
        col5.metric("Error", error, delta=f"{error/total*100:.1f}%" if total > 0 else "0%")
        
        # Results table
        display_results(st.session_state.results)
        
        # Export functionality
        if st.button("📥 Export Results to CSV"):
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue()
            
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name=f"ssh_connectivity_results_{int(time.time())}.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()
