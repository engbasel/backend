"""
NeuroAid System Orchestrator
=============================
Unified script to launch all backend services together.
Handles graceful shutdown with CTRL+C.
Fixed for Windows UTF-8 encoding support.
"""

import subprocess
import signal
import sys
import time
import os
from threading import Thread
import platform
import socket

# Fix Windows encoding issues - MUST BE FIRST
if sys.platform == 'win32':
    import codecs
    # Force UTF-8 for stdout and stderr
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    if sys.stderr.encoding != 'utf-8':
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    # Set environment variable for all child processes
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


# Service configurations
SERVICES = [
    {
        'name': 'Main Flask Server',
        'port': 5000,
        'script': 'flask_server/app.py',
        'env': {'PORT': '5000'},
        'emoji': '🌐'
    },
    {
        'name': 'AI Chatbot Service',
        'port': 5001,
        'script': 'ai_services/chatbot/app.py',
        'env': {'PORT': '5001'},
        'emoji': '🤖'
    },
    {
        'name': 'Stroke Assessment Service',
        'port': 5002,
        'script': 'ai_services/stroke_assessment/app.py',
        'env': {'PORT': '5002'},
        'emoji': '🏥'
    },
    {
        'name': 'Stroke Image Analysis Service',
        'port': 5003,
        'script': 'ai_services/stroke_image/app.py',
        'env': {'PORT': '5003'},
        'emoji': '🔬'
    },
    {
        'name': 'API Gateway',
        'port': 8080,
        'script': 'gateway.py',
        'env': {'GATEWAY_PORT': '8080'},
        'emoji': '🚀'
    }
]

# Store process objects
processes = []
threads = []


def kill_process_on_port(port):
    """
    Kill any process using the specified port (Windows only)
    
    Args:
        port: Port number to free up
    """
    if platform.system() != 'Windows':
        return
    
    try:
        # Find process using the port
        result = subprocess.run(
            ['netstat', '-ano'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        for line in result.stdout.split('\n'):
            if f':{port}' in line and 'LISTENING' in line:
                parts = line.split()
                if len(parts) >= 5:
                    pid = parts[-1]
                    try:
                        subprocess.run(
                            ['taskkill', '/F', '/PID', pid],
                            capture_output=True,
                            encoding='utf-8',
                            errors='replace'
                        )
                        print(f"{Colors.WARNING}⚠{Colors.ENDC}  Killed process {pid} on port {port}")
                    except:
                        pass
    except Exception as e:
        print(f"{Colors.WARNING}⚠{Colors.ENDC}  Could not kill process on port {port}: {e}")


def print_banner():
    """Print startup banner"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'=' * 70}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.OKGREEN}           NeuroAid Backend System Orchestrator{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'=' * 70}{Colors.ENDC}\n")


def print_service_info():
    """Print service information"""
    print(f"{Colors.BOLD}{Colors.OKBLUE}Starting Services:{Colors.ENDC}\n")
    for service in SERVICES:
        print(f"{service['emoji']}  {Colors.BOLD}{service['name']}{Colors.ENDC}")
        print(f"   Port: {Colors.OKCYAN}{service['port']}{Colors.ENDC}")
        print(f"   Script: {Colors.WARNING}{service['script']}{Colors.ENDC}\n")
    print(f"{Colors.BOLD}{Colors.HEADER}{'=' * 70}{Colors.ENDC}\n")


def safe_print(message):
    """
    Safely print messages with proper encoding handling
    
    Args:
        message: Message to print
    """
    try:
        print(message)
    except UnicodeEncodeError:
        # Fallback: replace problematic characters
        safe_msg = message.encode('ascii', errors='replace').decode('ascii')
        print(safe_msg)


def run_service(service):
    """
    Run a service in a subprocess
    
    Args:
        service: Service configuration dictionary
    """
    try:
        # Set up environment variables
        env = os.environ.copy()
        env.update(service['env'])
        # Force UTF-8 for child process
        env['PYTHONIOENCODING'] = 'utf-8'
        env['PYTHONUTF8'] = '1'
        
        # Determine Python executable
        python_exe = 'python' if platform.system() == 'Windows' else 'python3'
        
        # Build command
        cmd = [python_exe, '-u', service['script']]  # -u for unbuffered output
        
        safe_print(f"{Colors.OKGREEN}✓{Colors.ENDC} Starting {Colors.BOLD}{service['name']}{Colors.ENDC} on port {service['port']}...")
        
        # Start the process with UTF-8 encoding
        process = subprocess.Popen(
            cmd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='replace',  # Replace invalid characters instead of crashing
            bufsize=1,
            universal_newlines=True
        )
        
        # Store process
        processes.append({
            'name': service['name'],
            'port': service['port'],
            'process': process,
            'emoji': service['emoji']
        })
        
        # Stream output with safe printing
        try:
            for line in process.stdout:
                if line:
                    safe_print(f"[{service['emoji']} {service['name']}] {line.rstrip()}")
        except Exception as e:
            safe_print(f"{Colors.WARNING}⚠{Colors.ENDC}  Output stream error for {service['name']}: {e}")
        
        process.wait()
        
    except Exception as e:
        safe_print(f"{Colors.FAIL}✗{Colors.ENDC} Failed to start {service['name']}: {e}")


def start_all_services():
    """Start all services in separate threads"""
    # Clean up ports first
    safe_print(f"{Colors.WARNING}Cleaning up ports...{Colors.ENDC}")
    for service in SERVICES:
        kill_process_on_port(service['port'])
    time.sleep(1)
    
    # Start services (except gateway first)
    for service in SERVICES[:-1]:
        thread = Thread(target=run_service, args=(service,))
        thread.daemon = True
        thread.start()
        threads.append(thread)
        time.sleep(2)  # Give each service time to start
    
    # Start gateway last
    gateway = SERVICES[-1]
    thread = Thread(target=run_service, args=(gateway,))
    thread.daemon = True
    thread.start()
    threads.append(thread)
    
    safe_print(f"\n{Colors.BOLD}{Colors.OKGREEN}✓ All services started successfully!{Colors.ENDC}\n")
    safe_print(f"{Colors.BOLD}{Colors.OKCYAN}API Gateway:{Colors.ENDC} http://localhost:8080")
    safe_print(f"{Colors.BOLD}{Colors.OKCYAN}Health Check:{Colors.ENDC} http://localhost:8080/health\n")
    safe_print(f"{Colors.WARNING}Press CTRL+C to stop all services{Colors.ENDC}\n")
    safe_print(f"{Colors.BOLD}{Colors.HEADER}{'=' * 70}{Colors.ENDC}\n")


def signal_handler(sig, frame):
    """Handle CTRL+C gracefully"""
    safe_print(f"\n\n{Colors.WARNING}{'=' * 70}{Colors.ENDC}")
    safe_print(f"{Colors.BOLD}{Colors.WARNING}Shutting down all services...{Colors.ENDC}")
    safe_print(f"{Colors.WARNING}{'=' * 70}{Colors.ENDC}\n")
    
    # Terminate all processes
    for proc_info in processes:
        try:
            safe_print(f"{Colors.FAIL}✗{Colors.ENDC} Stopping {Colors.BOLD}{proc_info['name']}{Colors.ENDC} (port {proc_info['port']})...")
            proc_info['process'].terminate()
            try:
                proc_info['process'].wait(timeout=5)
            except subprocess.TimeoutExpired:
                safe_print(f"{Colors.WARNING}⚠{Colors.ENDC}  Force killing {proc_info['name']}...")
                proc_info['process'].kill()
        except Exception as e:
            safe_print(f"{Colors.FAIL}✗{Colors.ENDC} Error stopping {proc_info['name']}: {e}")
    
    # Clean up ports
    time.sleep(1)
    for service in SERVICES:
        kill_process_on_port(service['port'])
    
    safe_print(f"\n{Colors.BOLD}{Colors.OKGREEN}✓ All services stopped{Colors.ENDC}")
    safe_print(f"{Colors.BOLD}{Colors.HEADER}{'=' * 70}{Colors.ENDC}\n")
    sys.exit(0)


def check_ports_available():
    """Check if required ports are available"""
    unavailable_ports = []
    
    for service in SERVICES:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', service['port']))
        sock.close()
        
        if result == 0:
            unavailable_ports.append((service['name'], service['port']))
    
    if unavailable_ports:
        safe_print(f"{Colors.WARNING}⚠ Warning: The following ports are in use:{Colors.ENDC}\n")
        for name, port in unavailable_ports:
            safe_print(f"  {Colors.WARNING}• Port {port}{Colors.ENDC} - {name}")
        safe_print(f"\n{Colors.OKCYAN}Attempting to free up ports...{Colors.ENDC}\n")
        
        for name, port in unavailable_ports:
            kill_process_on_port(port)
        
        time.sleep(2)
        
        # Check again
        still_unavailable = []
        for service in SERVICES:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('localhost', service['port']))
            sock.close()
            if result == 0:
                still_unavailable.append((service['name'], service['port']))
        
        if still_unavailable:
            safe_print(f"{Colors.FAIL}✗ Error: Could not free up the following ports:{Colors.ENDC}\n")
            for name, port in still_unavailable:
                safe_print(f"  {Colors.FAIL}• Port {port}{Colors.ENDC} - {name}")
            safe_print(f"\n{Colors.WARNING}Please manually stop processes using these ports.{Colors.ENDC}\n")
            return False
    
    return True


def main():
    """Main execution function"""
    # Print banner
    print_banner()
    
    # Check if ports are available
    if not check_ports_available():
        sys.exit(1)
    
    # Print service info
    print_service_info()
    
    # Set up signal handler for CTRL+C
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start all services
    start_all_services()
    
    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
            
            # Check if any process has died
            for proc_info in processes:
                if proc_info['process'].poll() is not None:
                    safe_print(f"{Colors.FAIL}✗ {proc_info['name']} has stopped unexpectedly{Colors.ENDC}")
                    signal_handler(None, None)
    
    except KeyboardInterrupt:
        signal_handler(None, None)


if __name__ == '__main__':
    # Ensure we're in the backend directory
    if not os.path.exists('flask_server') or not os.path.exists('ai_services'):
        print(f"{Colors.FAIL}✗ Error: Please run this script from the backend directory{Colors.ENDC}")
        print(f"{Colors.WARNING}Current directory: {os.getcwd()}{Colors.ENDC}")
        sys.exit(1)
    
    main()
