#!/usr/bin/env python3
"""
Quick start script for AI News Dashboard
"""

import http.server
import socketserver
import os
import webbrowser

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)

def main():
    # Change to project directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    PORT = 8000
    
    print("Starting AI News Dashboard Server...")
    print(f"Serving from: {os.getcwd()}")
    
    # Create server
    with socketserver.TCPServer(("localhost", PORT), DashboardHandler) as httpd:
        print(f"Server running at: http://localhost:{PORT}")
        print(f"Dashboard: http://localhost:{PORT}/")
        
        # Open browser
        try:
            webbrowser.open(f'http://localhost:{PORT}/')
        except:
            print("Could not open browser automatically")
        
        # Keep server running
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")

if __name__ == "__main__":
    main()