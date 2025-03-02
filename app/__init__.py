#!/usr/bin/env python3
"""
Dila Headless Image Editor - Main Application
"""

import os
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from app.utils.cleanup import cleanup_old_images

def create_app(config_object=None):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Load configuration
    if config_object:
        app.config.from_object(config_object)
    else:
        # Default configuration
        app.config.from_pyfile('../config.py')
    
    # Ensure output directories exist
    os.makedirs(app.config['OUTPUT_DIR'], exist_ok=True)
    os.makedirs(app.config['OUTPUT_IMAGES_DIR'], exist_ok=True)
    os.makedirs(app.config['OUTPUT_TEMP_DIR'], exist_ok=True)
    
    # Register blueprints
    from app.api.routes import api_bp
    from app.web.routes import web_bp
    
    app.register_blueprint(api_bp)
    app.register_blueprint(web_bp)
    
    # Set up image cleanup scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=lambda: cleanup_old_images(app.config['OUTPUT_DIR'], app.config['IMAGE_MAX_AGE']),
        trigger='interval',
        minutes=5  # Run cleanup every 5 minutes
    )
    scheduler.start()
    
    return app 