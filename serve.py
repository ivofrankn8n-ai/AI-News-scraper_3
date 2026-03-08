#!/usr/bin/env python3
"""
Simple HTTP server for AI News Dashboard
"""

import http.server
import socketserver
import os
import webbrowser
from datetime import datetime
import sys

PORT = 8000

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)
    
    def log_message(self, format, *args):
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {format % args}")

def main():
    # Change to project directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print(f"Starting server in: {os.getcwd()}")
    print(f"Files in directory: {os.listdir('.')}")
    
    try:
        # Use ThreadingTCPServer for better handling
        with socketserver.ThreadingTCPServer(("localhost", PORT), DashboardHandler) as httpd:
            print(f"AI News Dashboard server started at http://localhost:{PORT}")
            print("Open your browser and navigate to the URL above")
            print("Press Ctrl+C to stop the server")
            
            # Open browser automatically
            try:
                webbrowser.open(f'http://localhost:{PORT}/')
            except Exception as e:
                print(f"Browser opening failed: {e}")
            
            # Set timeout to prevent hanging
            httpd.timeout = 1
            
            try:
                while True:
                    httpd.handle_request()
            except KeyboardInterrupt:
                print("\nServer stopped")
                
    except Exception as e:
        print(f"Server error: {e}")
        print("Trying alternative approach...")
        
        # Fallback to simple server
        os.system(f"python -m http.server {PORT} --bind localhost --directory .")

if __name__ == "__main__":
    main()