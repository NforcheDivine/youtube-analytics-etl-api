#!/usr/bin/env python3
"""
YouTube Analytics API Runner
"""

import uvicorn

if __name__ == "__main__":
    print("🚀 Starting YouTube Analytics API Server...")
    print("📊 API Documentation: http://localhost:8000/docs")
    print("🌐 Health Check: http://localhost:8000/health")
    print("🛑 Press Ctrl+C to stop the server\n")

    uvicorn.run(
        "api:app",  # Import string instead of object
        host="0.0.0.0",
        port=8000,
        reload=False  # Disable reload for now
    )