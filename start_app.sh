#!/bin/sh

# Set database URL if not provided
export DATABASE_URL=${DATABASE_URL:-"sqlite:///./todo_chatbot.db"}

# Start the main application using the entrypoint
exec python /app/entrypoint.py