#!/usr/bin/env python3

import os
import sys

def main():
    # Add the backend directory to Python path
    sys.path.insert(0, '/app/backend')

    # Set environment variable to help with imports
    os.environ['PYTHONPATH'] = '/app/backend'

    # Set default database URL to SQLite for local development/testing
    if 'DATABASE_URL' not in os.environ:
        os.environ['DATABASE_URL'] = 'sqlite:///./todo_chatbot.db'

    # Import and run the application directly
    import uvicorn
    from backend.main import app

    # Get the port from environment
    port = int(os.environ.get("PORT", 8000))
    print(f"PORT environment variable value: {os.environ.get('PORT')}")
    print(f"Using port: {port}")

    # Run the app
    uvicorn.run(app, host="0.0.0.0", port=port, lifespan="on", reload=False)

if __name__ == "__main__":
    main()