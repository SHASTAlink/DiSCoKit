"""
Flask application factory for experimental chat interface.
"""

import os
from functools import lru_cache
from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import dotenv
import openai

# Load environment variables
dotenv.load_dotenv()

# Initialize extensions
db = SQLAlchemy()

#limiter = Limiter(
#    key_func=get_remote_address,
#    default_limits=["200 per day", "50 per hour"],
#    storage_uri="memory://",
#)


@lru_cache(maxsize=1)
def get_azure_client():
    """
    Get cached Azure OpenAI client (singleton).
    
    Creates client once and caches for lifetime of process.
    Environment variables are validated on app startup.
    
    Returns:
        Cached AzureOpenAI client instance
    """
    return openai.AzureOpenAI(
        api_version=os.environ["MODEL_API_VERSION"],
        azure_endpoint=os.environ["MODEL_ENDPOINT"],
        api_key=os.environ["MODEL_SUBSCRIPTION_KEY"],
    )


def create_app(config_name=None):
    """Application factory pattern."""
    app = Flask(__name__)
    
    # Validate required environment variables on startup
    # Note: Model parameters (temperature, max_completion_tokens) are now configured
    # in experimental_conditions.json under study_metadata.default_model_params
    required_env_vars = [
        'MODEL_ENDPOINT',
        'MODEL_DEPLOYMENT',
        'MODEL_API_VERSION',
        'MODEL_SUBSCRIPTION_KEY',
        'MODEL_MAX_RETRIES',
        'MODEL_RETRY_DELAY'
    ]
    
    missing_vars = [var for var in required_env_vars if var not in os.environ]
    if missing_vars:
        raise RuntimeError(
            f"Missing required environment variables: {', '.join(missing_vars)}\n"
            f"Please check your .env file and ensure all required variables are set."
        )
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database configuration
    db_path = os.environ.get('DATABASE_URL')
    if not db_path:
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = f'sqlite:///{project_dir}/data/chat_experiment.db'
        print(f"💾 Database location: {project_dir}/data/chat_experiment.db")
    else:
        print(f"💾 Database location (from .env): {db_path}")
    
    app.config['SQLALCHEMY_DATABASE_URI'] = db_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 3600,
    }
    
    # Initialize extensions with app
    db.init_app(app)

    #limiter.init_app(app)
    
    # Security headers for iframe embedding control
    @app.after_request
    def set_security_headers(response):
        """
        Set security headers to control iframe embedding.
        
        Controls which websites can embed the chat interface in an iframe.
        Configured via ALLOWED_FRAME_ANCESTORS environment variable.
        
        Examples:
            # Allow only Qualtrics:
            ALLOWED_FRAME_ANCESTORS=yourschool.qualtrics.com
            
            # Allow multiple domains:
            ALLOWED_FRAME_ANCESTORS=domain1.com,domain2.com
            
            # Development mode (allow all):
            Leave ALLOWED_FRAME_ANCESTORS unset or blank
        """
        # Get allowed frame ancestors from environment (optional)
        allowed_ancestors = os.environ.get('ALLOWED_FRAME_ANCESTORS', '')
        
        if allowed_ancestors:
            # Restrict embedding to specified domains
            # Multiple domains can be comma-separated
            domains = [domain.strip() for domain in allowed_ancestors.split(',')]
            
            # Ensure domains have https:// prefix
            formatted_domains = []
            for domain in domains:
                if domain.startswith('http://') or domain.startswith('https://'):
                    formatted_domains.append(domain)
                else:
                    formatted_domains.append(f'https://{domain}')
            
            # Build CSP header
            ancestors = ' '.join(formatted_domains)
            response.headers['Content-Security-Policy'] = f"frame-ancestors 'self' {ancestors}"
            
            # Optional: Log during development to verify configuration
            # print(f"🔒 Frame embedding restricted to: self, {ancestors}")
        else:
            # Development mode - allow all embedding
            # No CSP header = browser allows embedding from any domain
            pass
        
        return response
    
    # Register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    # Create database tables (safe for multi-worker environments)
    with app.app_context():
        # Ensure database directory exists (idempotent - safe if already exists)
        if db_path.startswith('sqlite:///'):
            # Handle both sqlite:/// (relative) and sqlite://// (absolute)
            path_part = db_path.replace('sqlite:///', '')
            db_dir = Path(path_part).parent
            db_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            db.create_all()
        except Exception as e:
            # Tables may already exist from another worker - this is fine
            app.logger.debug(f"Database initialization: {e}")
    
    return app