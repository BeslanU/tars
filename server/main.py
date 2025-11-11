"""
TARS - Multi-Modal Summarization Backend
Main application entry point for Flask server

This module initializes and configures the Flask application with:
- CORS support for frontend integration
- Route registration for books, videos, and audio summarization
- Error handling and logging
"""

import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from loguru import logger

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure CORS
CORS(app, resources={
    r"/api/*": {
        "origins": os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(","),
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Configure logging
logger.add(
    "logs/tars_{time}.log",
    rotation="500 MB",
    retention="7 days",
    level="INFO"
)


# ============================================================================
# Routes
# ============================================================================

@app.route("/", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "TARS Multi-Modal Summarization API",
        "version": "1.0.0"
    }), 200


@app.route("/api/health", methods=["GET"])
def api_health():
    """API health check with detailed info"""
    return jsonify({
        "status": "operational",
        "timestamp": __import__("datetime").datetime.now().isoformat(),
        "modules": {
            "books": "available",
            "videos": "in_development",
            "audio": "in_development"
        }
    }), 200


# ============================================================================
# Book Summarization Routes (Placeholder)
# ============================================================================

@app.route("/api/books/summarize", methods=["POST"])
def summarize_book():
    """
    Summarize book content from text or file upload
    
    Request body:
    - text: str (optional) - Raw text to summarize
    - file: file (optional) - .txt or .pdf file to process
    
    Response:
    {
        "tldr": "3-sentence summary",
        "key_points": ["point1", "point2", ...],
        "questions": ["Q1", "Q2", "Q3"]
    }
    """
    return jsonify({
        "error": "Endpoint not yet implemented",
        "message": "Book summarization module is under development"
    }), 501


# ============================================================================
# Error Handlers
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    logger.warning(f"404 error: {error}")
    return jsonify({
        "error": "Not Found",
        "message": "The requested resource does not exist"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"500 error: {error}")
    return jsonify({
        "error": "Internal Server Error",
        "message": "An unexpected error occurred"
    }), 500


# ============================================================================
# Application Entry Point
# ============================================================================

if __name__ == "__main__":
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Log startup
    logger.info("Starting TARS Multi-Modal Summarization Backend")
    logger.info(f"Environment: {os.getenv('FLASK_ENV', 'development')}")
    
    # Run Flask development server
    app.run(
        host=os.getenv("FLASK_HOST", "0.0.0.0"),
        port=int(os.getenv("FLASK_PORT", 5000)),
        debug=os.getenv("FLASK_DEBUG", "False") == "True"
    )
