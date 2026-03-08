#!/usr/bin/env python3
"""
Simple test server for AI News Dashboard
"""

import http.server
import socketserver
import threading
import time
import sys
import os

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)

def start_server():
    """Start the HTTP server"""
    try:
        with socketserver.TCPServer(("localhost", 8001), DashboardHandler) as httpd:
            print("AI News Dashboard server started!")
            print("Dashboard available at: http://localhost:8001/")
            print("Press Ctrl+C to stop the server")
            httpd.serve_forever()
    except Exception as e:
        print(f"Server error: {e}")

if __name__ == "__main__":
    print("Starting AI News Dashboard server...")
    print(f"Working directory: {os.getcwd()}")
    print(f"Files available: {os.listdir('.')}")
    
    # Start server in main thread (blocking)
    start_server()