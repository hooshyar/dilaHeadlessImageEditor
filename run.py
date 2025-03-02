#!/usr/bin/env python3
"""
Run script for Dila Headless Image Editor
"""

import os
import sys
import logging
import argparse
import signal
from app import create_app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("app.log")
    ]
)

logger = logging.getLogger(__name__)

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Dila Headless Image Editor')
    parser.add_argument('--host', default=None, help='Host to bind to')
    parser.add_argument('--port', type=int, default=None, help='Port to bind to')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--request-timeout', type=int, default=60, 
                      help='Maximum request processing time in seconds')
    parser.add_argument('--task-timeout', type=int, default=300, 
                      help='Maximum background task time in seconds')
    return parser.parse_args()

def setup_timeouts(request_timeout, task_timeout):
    """Configure timeouts for the application"""
    logger.info(f"Setting request timeout to {request_timeout}s and task timeout to {task_timeout}s")
    
    # Store timeouts in environment for app-wide access
    os.environ['REQUEST_TIMEOUT'] = str(request_timeout)
    os.environ['TASK_TIMEOUT'] = str(task_timeout)
    
    # Set up process-level timeout (for development server)
    def timeout_handler(signum, frame):
        logger.error("Process timed out - operation took too long")
        raise TimeoutError("Operation timed out")
    
    # Register signal handler for SIGALRM
    signal.signal(signal.SIGALRM, timeout_handler)

def main():
    """Run the application"""
    args = parse_args()
    
    # Set environment variables from arguments if provided
    if args.host:
        os.environ['HOST'] = args.host
    if args.port:
        os.environ['PORT'] = str(args.port)
    if args.debug:
        os.environ['DEBUG'] = 'true'
    
    # Setup timeouts
    setup_timeouts(args.request_timeout, args.task_timeout)
    
    # Create and run the app
    app = create_app()
    host = app.config.get('HOST', '0.0.0.0')
    port = app.config.get('PORT', 5001)
    debug = app.config.get('DEBUG', False)
    
    logger.info(f"Starting Dila Headless Image Editor on {host}:{port} (debug={debug})")
    app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    main() 