#!/usr/bin/env python3
"""
Dila Headless Image Editor - Main Application
"""

import os
import signal
import logging
from flask import Flask, request, current_app
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from app.utils.cleanup import cleanup_old_images

logger = logging.getLogger(__name__)

def create_app(config_object=None):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Load configuration
    if config_object:
        app.config.from_object(config_object)
    else:
        # Default configuration
        app.config.from_pyfile('../config.py')
    
    # Load timeout settings from environment
    app.config['REQUEST_TIMEOUT'] = int(os.environ.get('REQUEST_TIMEOUT', 60))
    app.config['TASK_TIMEOUT'] = int(os.environ.get('TASK_TIMEOUT', 300))
    
    # Ensure output directories exist
    os.makedirs(app.config['OUTPUT_DIR'], exist_ok=True)
    os.makedirs(app.config['OUTPUT_IMAGES_DIR'], exist_ok=True)
    os.makedirs(app.config['OUTPUT_TEMP_DIR'], exist_ok=True)
    
    # Register blueprints
    from app.api.routes import api_bp
    from app.web.routes import web_bp
    
    app.register_blueprint(api_bp)
    app.register_blueprint(web_bp)
    
    # Add request timeout monitoring
    @app.before_request
    def setup_request_timer():
        request.start_time = os.times().user
        
    @app.after_request
    def check_request_timeout(response):
        if hasattr(request, 'start_time'):
            elapsed = os.times().user - request.start_time
            if elapsed > app.config['REQUEST_TIMEOUT']:
                logger.warning(f"Request took {elapsed:.2f}s, exceeding timeout of {app.config['REQUEST_TIMEOUT']}s")
        return response
    
    # Set up image cleanup scheduler with timeout limits
    executors = {
        'default': ThreadPoolExecutor(max_workers=2)
    }
    job_defaults = {
        'coalesce': True,
        'max_instances': 1,
        'misfire_grace_time': 60,
        'timeout': app.config['TASK_TIMEOUT']  # Set timeout for background tasks
    }
    
    scheduler = BackgroundScheduler(executors=executors, job_defaults=job_defaults)
    scheduler.add_job(
        func=lambda: cleanup_old_images(app.config['OUTPUT_DIR'], app.config['IMAGE_MAX_AGE']),
        trigger='interval',
        minutes=5,  # Run cleanup every 5 minutes
        id='cleanup_images'
    )
    scheduler.start()
    
    app.scheduler = scheduler  # Store scheduler instance in app for later reference
    
    # Log startup configuration
    logger.info(f"App configured with REQUEST_TIMEOUT={app.config['REQUEST_TIMEOUT']}s, "
                f"TASK_TIMEOUT={app.config['TASK_TIMEOUT']}s")
    
    return app 