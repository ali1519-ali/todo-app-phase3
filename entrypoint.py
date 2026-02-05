#!/usr/bin/env python3
import os
import sys
import logging
import subprocess

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_migrations():
    """Run database migrations"""
    logger.info("Running database migrations...")
    try:
        # Run alembic upgrade
        result = subprocess.run(['alembic', 'upgrade', 'head'],
                                cwd='/app',
                                capture_output=True,
                                text=True)
        if result.returncode != 0:
            logger.error(f"Alembic migration failed: {result.stderr}")
            # Continue anyway since this might be first deploy
        else:
            logger.info("Database migrations completed successfully")
    except Exception as e:
        logger.warning(f"Could not run migrations: {str(e)}. This might be OK for first deploy.")

def start_application():
    """Start the main application"""
    logger.info("Starting application...")

    # Set default database URL if not provided
    if 'DATABASE_URL' not in os.environ:
        os.environ['DATABASE_URL'] = 'sqlite:///./todo_chatbot.db'

    # Add backend to Python path - both /app and /app/backend
    import sys
    import os
    sys.path.insert(0, '/app')
    sys.path.insert(0, '/app/backend')

    # Set PYTHONPATH environment variable as well
    os.environ['PYTHONPATH'] = '/app:/app/backend:' + os.environ.get('PYTHONPATH', '')

    # Change to the app directory to ensure relative imports work
    os.chdir('/app')

    # Import and run the application directly using importlib to bypass caching issues
    import uvicorn
    import importlib.util

    # Load the main module directly from file
    spec = importlib.util.spec_from_file_location("main", "/app/backend/main.py")
    main_module = importlib.util.module_from_spec(spec)
    sys.modules["main"] = main_module
    spec.loader.exec_module(main_module)

    # Get the app instance
    app = main_module.app

    port = int(os.environ.get("PORT", 8000))
    logger.info(f"Starting server on port {port}")

    uvicorn.run(app, host="0.0.0.0", port=port, lifespan="on")

if __name__ == "__main__":
    logger.info("Application starting...")

    # Set database URL from environment or default
    database_url = os.environ.get('DATABASE_URL', 'sqlite:///./todo_chatbot.db')
    os.environ['DATABASE_URL'] = database_url

    # Run migrations
    run_migrations()

    # Start the application
    start_application()