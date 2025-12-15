"""
NeuroAid API Gateway
====================
Centralized entry point for all backend services.
Provides routing, logging, and proxying capabilities.
"""

import sys
import os

# Fix Windows encoding issues - MUST BE FIRST
if sys.platform == 'win32':
    import codecs
    # Force UTF-8 for stdout and stderr
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    if sys.stderr.encoding != 'utf-8':
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    os.environ['PYTHONIOENCODING'] = 'utf-8'

from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import requests
import time
from datetime import datetime
import logging
from werkzeug.exceptions import HTTPException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# CORS Configuration for LAN Access
# Allow requests from any device on the local network
CORS(app, resources={
    r"/*": {
        "origins": "*",  # Allow all origins for local network usage
        "methods": ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Accept"],
        "expose_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True,
        "max_age": 3600
    }
})

# Service configuration
# Using localhost since all services run on the same machine as the gateway
# The gateway itself listens on 0.0.0.0 for LAN access
SERVICES = {
    'main': {
        'name': 'Main Flask Server',
        'url': 'http://127.0.0.1:5000',
        'prefix': '/api/main'
    },
    'ai_chatbot': {
        'name': 'AI Chatbot Service',
        'url': 'http://127.0.0.1:5001',
        'prefix': '/api/ai/chat'
    },
    'ai_assessment': {
        'name': 'Stroke Assessment Service',
        'url': 'http://127.0.0.1:5002',
        'prefix': '/api/ai/assessment'
    },
    'ai_image': {
        'name': 'Stroke Image Analysis Service',
        'url': 'http://127.0.0.1:5003',
        'prefix': '/api/ai/image'
    }
}

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
    UNDERLINE = '\033[4m'


def log_request(method, path, service_name=None):
    """Log incoming request"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logger.info(f"{Colors.OKCYAN}[GATEWAY]{Colors.ENDC} {timestamp} - Incoming Request: {Colors.BOLD}{method}{Colors.ENDC} {path}")
    if service_name:
        logger.info(f"{Colors.OKBLUE}[GATEWAY]{Colors.ENDC} Routing to: {Colors.OKGREEN}{service_name}{Colors.ENDC}")


def log_response(status_code, time_taken):
    """Log outgoing response"""
    color = Colors.OKGREEN if 200 <= status_code < 300 else Colors.WARNING if 300 <= status_code < 400 else Colors.FAIL
    logger.info(f"{Colors.HEADER}[GATEWAY]{Colors.ENDC} Response: {color}{status_code}{Colors.ENDC} - Time: {Colors.BOLD}{time_taken:.2f}ms{Colors.ENDC}\n")


def proxy_request(service_url, path, method, headers, data=None, files=None):
    """
    Forward request to the target service
    
    Args:
        service_url: Base URL of the service
        path: Request path
        method: HTTP method
        headers: Request headers
        data: Request data (JSON or form)
        files: Request files
    
    Returns:
        Response from the target service
    """
    # Build target URL
    target_url = f"{service_url}{path}"

    # Filter headers (remove host-specific headers)
    # When sending files, also remove Content-Type to let requests set it correctly
    excluded_headers = ['host', 'connection', 'content-length']
    if files:
        excluded_headers.append('content-type')

    filtered_headers = {
        key: value for key, value in headers.items()
        if key.lower() not in excluded_headers
    }

    try:
        # Forward the request
        if method == 'GET':
            response = requests.get(
                target_url,
                headers=filtered_headers,
                params=request.args,
                timeout=30
            )
        elif method == 'POST':
            if files:
                # Let requests library handle Content-Type for multipart
                response = requests.post(
                    target_url,
                    headers=filtered_headers,
                    data=data,
                    files=files,
                    timeout=30
                )
            else:
                response = requests.post(
                    target_url,
                    headers=filtered_headers,
                    json=data,
                    timeout=30
                )
        elif method == 'PUT':
            response = requests.put(
                target_url,
                headers=filtered_headers,
                json=data,
                timeout=30
            )
        elif method == 'DELETE':
            response = requests.delete(
                target_url,
                headers=filtered_headers,
                timeout=30
            )
        elif method == 'PATCH':
            response = requests.patch(
                target_url,
                headers=filtered_headers,
                json=data,
                timeout=30
            )
        else:
            return jsonify({'error': f'Method {method} not supported'}), 405
        
        # Return the response
        return Response(
            response.content,
            status=response.status_code,
            headers=dict(response.headers)
        )
    
    except requests.exceptions.ConnectionError:
        return jsonify({
            'error': 'Service unavailable',
            'message': 'Could not connect to the target service'
        }), 503
    except requests.exceptions.Timeout:
        return jsonify({
            'error': 'Request timeout',
            'message': 'The service took too long to respond'
        }), 504
    except Exception as e:
        return jsonify({
            'error': 'Gateway error',
            'message': str(e)
        }), 500


@app.before_request
def before_request():
    """Store request start time"""
    request.start_time = time.time()


@app.after_request
def after_request(response):
    """Log response after request completion"""
    if hasattr(request, 'start_time'):
        time_taken = (time.time() - request.start_time) * 1000  # Convert to ms
        log_response(response.status_code, time_taken)
    return response


# Gateway health check
@app.route('/health', methods=['GET'])
def gateway_health():
    """Gateway health check endpoint"""
    log_request(request.method, request.path)
    
    # Check all services
    services_status = {}
    for service_key, service in SERVICES.items():
        try:
            response = requests.get(f"{service['url']}/health", timeout=2)
            services_status[service_key] = {
                'status': 'online' if response.status_code == 200 else 'error',
                'url': service['url']
            }
        except:
            services_status[service_key] = {
                'status': 'offline',
                'url': service['url']
            }
    
    return jsonify({
        'gateway': 'OK',
        'timestamp': datetime.now().isoformat(),
        'services': services_status
    }), 200


# Route: /api/main/* -> Main Flask Server (port 5000)
@app.route('/api/main/<path:subpath>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def proxy_main(subpath):
    """Proxy requests to Main Flask Server"""
    service = SERVICES['main']
    path = f"/api/{subpath}"  # Reconstruct the original path
    
    log_request(request.method, request.path, service['name'])
    
    # Get request data
    data = None
    files = None

    if request.method in ['POST', 'PUT', 'PATCH']:
        # Check Content-Type for multipart/form-data
        content_type = request.content_type or ''

        # Debug logging
        print(f'[GATEWAY DEBUG] Content-Type: {content_type}')
        print(f'[GATEWAY DEBUG] request.files: {request.files}')
        print(f'[GATEWAY DEBUG] request.form: {request.form}')
        print(f'[GATEWAY DEBUG] request.data length: {len(request.data)}')

        if 'multipart/form-data' in content_type:
            # Handle file uploads - read file data properly
            files = {}
            for key, file in request.files.items():
                # Read file content and reset stream
                file_content = file.read()
                print(f'[GATEWAY DEBUG] File {key}: {len(file_content)} bytes')
                file.stream.seek(0)  # Reset stream for potential re-reading
                files[key] = (file.filename, file_content, file.content_type)
            data = request.form.to_dict() if request.form else None
            print(f'[GATEWAY DEBUG] Files to forward: {list(files.keys())}')
        elif request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict() if request.form else None

    return proxy_request(service['url'], path, request.method, request.headers, data, files)


# Route: /api/ai/chat/* -> AI Chatbot Service (port 5001)
@app.route('/api/ai/chat', methods=['POST'])
@app.route('/api/ai/chat/<path:subpath>', methods=['GET', 'POST'])
def proxy_ai_chatbot(subpath=''):
    """Proxy requests to AI Chatbot Service (with streaming support)"""
    service = SERVICES['ai_chatbot']
    path = f"/chat" if not subpath else f"/{subpath}"

    log_request(request.method, request.path, service['name'])

    # Handle streaming endpoint differently
    if 'stream' in subpath:
        # For streaming, we need to forward the stream response
        target_url = f"{service['url']}{path}"
        data = request.get_json() if request.is_json else None

        try:
            response = requests.post(
                target_url,
                json=data,
                headers={k: v for k, v in request.headers.items()
                        if k.lower() not in ['host', 'connection', 'content-length']},
                stream=True,
                timeout=60
            )

            def generate():
                for chunk in response.iter_content(chunk_size=None, decode_unicode=False):
                    if chunk:
                        yield chunk

            return Response(
                generate(),
                status=response.status_code,
                content_type=response.headers.get('content-type', 'text/event-stream'),
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "*"
                }
            )
        except Exception as e:
            return jsonify({
                'error': 'Streaming proxy error',
                'message': str(e)
            }), 500
    else:
        # Regular non-streaming request
        data = request.get_json() if request.is_json else None
        return proxy_request(service['url'], path, request.method, request.headers, data)


# Route: /api/ai/assessment/* -> Stroke Assessment Service (port 5002)
@app.route('/api/ai/assessment', methods=['POST'])
@app.route('/api/ai/assessment/<path:subpath>', methods=['GET', 'POST'])
def proxy_ai_assessment(subpath=''):
    """Proxy requests to Stroke Assessment Service"""
    service = SERVICES['ai_assessment']
    path = f"/predict" if not subpath else f"/{subpath}"

    log_request(request.method, request.path, service['name'])

    data = request.get_json() if request.is_json else None
    return proxy_request(service['url'], path, request.method, request.headers, data)


# Route: /api/ai/image/* -> Stroke Image Analysis Service (port 5003)
@app.route('/api/ai/image', methods=['POST'])
@app.route('/api/ai/image/<path:subpath>', methods=['GET', 'POST'])
def proxy_ai_image(subpath=''):
    """Proxy requests to Stroke Image Analysis Service (with image upload support)"""
    service = SERVICES['ai_image']
    path = f"/analyze" if not subpath else f"/{subpath}"

    log_request(request.method, request.path, service['name'])

    # Handle file uploads
    target_url = f"{service['url']}{path}"

    try:
        files = None
        data = None

        if request.files:
            # Forward file uploads
            files = {key: (file.filename, file.stream, file.content_type)
                    for key, file in request.files.items()}
            data = request.form.to_dict() if request.form else None
        elif request.is_json:
            data = request.get_json()

        # Forward the request
        if request.method == 'POST':
            if files:
                response = requests.post(
                    target_url,
                    files=files,
                    data=data,
                    headers={k: v for k, v in request.headers.items()
                            if k.lower() not in ['host', 'connection', 'content-length', 'content-type']},
                    timeout=60
                )
            else:
                response = requests.post(
                    target_url,
                    json=data,
                    headers={k: v for k, v in request.headers.items()
                            if k.lower() not in ['host', 'connection', 'content-length']},
                    timeout=60
                )
        else:
            response = requests.get(
                target_url,
                headers={k: v for k, v in request.headers.items()
                        if k.lower() not in ['host', 'connection', 'content-length']},
                timeout=30
            )

        return Response(
            response.content,
            status=response.status_code,
            headers=dict(response.headers)
        )

    except Exception as e:
        return jsonify({
            'error': 'Image analysis proxy error',
            'message': str(e)
        }), 500


# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    log_request(request.method, request.path)
    return jsonify({
        'error': 'Route not found',
        'message': f'Gateway does not have a route for {request.path}',
        'available_routes': [
            '/api/main/*',
            '/api/ai/chat',
            '/api/ai/assessment'
        ]
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal gateway error',
        'message': str(error)
    }), 500


@app.errorhandler(Exception)
def handle_exception(e):
    """Handle all other exceptions"""
    if isinstance(e, HTTPException):
        return jsonify({
            'error': e.name,
            'message': e.description
        }), e.code
    
    return jsonify({
        'error': 'Unexpected error',
        'message': str(e)
    }), 500


if __name__ == '__main__':
    import socket

    # Gateway configuration
    GATEWAY_PORT = int(os.environ.get('GATEWAY_PORT', 8080))

    # Get local IP address for LAN access
    local_ip = 'localhost'
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except:
        pass

    # Print startup banner
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'=' * 60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.OKGREEN}🚀 NeuroAid API Gateway Started{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'=' * 60}{Colors.ENDC}\n")

    print(f"{Colors.BOLD}{Colors.WARNING}📱 LAN Access URLs (use on mobile devices):{Colors.ENDC}")
    print(f"{Colors.OKCYAN}   Gateway:{Colors.ENDC} {Colors.BOLD}http://{local_ip}:{GATEWAY_PORT}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}   Health:{Colors.ENDC}  {Colors.BOLD}http://{local_ip}:{GATEWAY_PORT}/health{Colors.ENDC}\n")

    print(f"{Colors.BOLD}{Colors.OKBLUE}💻 Localhost URLs (for this computer):{Colors.ENDC}")
    print(f"{Colors.OKCYAN}   Gateway:{Colors.ENDC} {Colors.BOLD}http://localhost:{GATEWAY_PORT}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}   Health:{Colors.ENDC}  {Colors.BOLD}http://localhost:{GATEWAY_PORT}/health{Colors.ENDC}\n")

    print(f"{Colors.BOLD}{Colors.OKBLUE}Service Routes:{Colors.ENDC}")
    print(f"{Colors.OKGREEN}  ✓{Colors.ENDC} /api/main/*        → Main Flask Server (port 5000)")
    print(f"{Colors.OKGREEN}  ✓{Colors.ENDC} /api/ai/chat       → AI Chatbot Service (port 5001)")
    print(f"{Colors.OKGREEN}  ✓{Colors.ENDC} /api/ai/assessment → Stroke Assessment Service (port 5002)")
    print(f"{Colors.OKGREEN}  ✓{Colors.ENDC} /api/ai/image      → Stroke Image Analysis Service (port 5003)\n")

    print(f"{Colors.BOLD}{Colors.WARNING}🔧 Configuration for Flutter App:{Colors.ENDC}")
    print(f"{Colors.OKCYAN}   Update api_constants.dart:{Colors.ENDC}")
    print(f"{Colors.BOLD}   static const String _networkIp = '{local_ip}';{Colors.ENDC}\n")

    print(f"{Colors.BOLD}{Colors.HEADER}{'=' * 60}{Colors.ENDC}\n")

    # Start the gateway
    app.run(host='0.0.0.0', port=GATEWAY_PORT, debug=False)
