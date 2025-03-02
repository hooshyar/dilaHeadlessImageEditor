#!/usr/bin/env python3
"""
Web routes for the Dila Headless Image Editor
Includes the playground UI for testing the API
"""

from flask import Blueprint, render_template, current_app, request

# Create blueprint
web_bp = Blueprint('web', __name__)

@web_bp.route('/')
def index():
    """Redirect to playground or show API info"""
    return render_template('index.html')

@web_bp.route('/playground')
def playground():
    """Interactive playground for testing the API"""
    config = {
        'api_url': f"{request.url_root}api",
        'default_width': current_app.config['DEFAULT_WIDTH'],
        'default_height': current_app.config['DEFAULT_HEIGHT'],
        'default_font': current_app.config['DEFAULT_FONT_FAMILY'],
        'default_font_size': current_app.config['DEFAULT_FONT_SIZE']
    }
    return render_template('playground.html', config=config) 