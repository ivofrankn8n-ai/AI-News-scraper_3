#!/usr/bin/env python3
"""
Simple API for AI News Dashboard
Provides endpoints for running the pipeline and serving data
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import subprocess
import threading
from urllib.parse import urlparse, parse_qs
import sys

# Add tools directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'tools'))

class DashboardAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/api/refresh':
            self.handle_refresh()
        elif path == '/api/articles':
            self.handle_articles()
        elif path.startswith('/.tmp/'):
            self.handle_static_file(path)
        else:
            self.handle_static_file(path)
    
    def do_HEAD(self):
        """Handle HEAD requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/api/refresh':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
        elif path == '/api/articles':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
        else:
            # For static files, just send headers
            file_path = os.path.join(os.path.dirname(__file__), path.lstrip('/'))
            
            if os.path.exists(file_path):
                self.send_response(200)
                # Determine content type
                if path.endswith('.css'):
                    self.send_header('Content-type', 'text/css')
                elif path.endswith('.js'):
                    self.send_header('Content-type', 'application/javascript')
                elif path.endswith('.json'):
                    self.send_header('Content-type', 'application/json')
                else:
                    self.send_header('Content-type', 'text/html')
                self.end_headers()
            else:
                self.send_error(404, "File not found")
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/api/refresh':
            self.handle_refresh()
        elif path == '/api/articles':
            self.handle_articles()
        elif path.startswith('/.tmp/'):
            self.handle_static_file(path)
        else:
            self.handle_static_file(path)
    
    def handle_refresh(self):
        """Handle refresh request - run the pipeline"""
        try:
            # Run the pipeline in a separate thread
            def run_pipeline():
                try:
                    subprocess.run([sys.executable, 'tools/run_pipeline.py'], 
                                  cwd=os.path.dirname(__file__), 
                                  check=True, 
                                  capture_output=True)
                except Exception as e:
                    print(f"Pipeline error: {e}")
            
            # Start pipeline in background
            thread = threading.Thread(target=run_pipeline)
            thread.daemon = True
            thread.start()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                'status': 'success',
                'message': 'Pipeline started successfully',
                'data': {'refresh_id': 'refresh_123'}
            }
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_error(500, f"Refresh failed: {str(e)}")
    
    def handle_articles(self):
        """Serve articles JSON"""
        try:
            articles_file = os.path.join(os.path.dirname(__file__), '.tmp', 'processed_articles.json')
            
            if not os.path.exists(articles_file):
                self.send_error(404, "Articles not found")
                return
            
            with open(articles_file, 'r', encoding='utf-8') as f:
                articles_data = json.load(f)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(articles_data).encode())
            
        except Exception as e:
            self.send_error(500, f"Error loading articles: {str(e)}")
    
    def handle_static_file(self, path):
        """Serve static files"""
        if path == '/':
            path = '/dashboard.html'
        
        file_path = os.path.join(os.path.dirname(__file__), path.lstrip('/'))
        
        if not os.path.exists(file_path):
            self.send_error(404, "File not found")
            return
        
        # Determine content type
        content_type = 'text/html'
        if path.endswith('.css'):
            content_type = 'text/css'
        elif path.endswith('.js'):
            content_type = 'application/javascript'
        elif path.endswith('.json'):
            content_type = 'application/json'
        
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            
        except Exception as e:
            self.send_error(500, f"Error reading file: {str(e)}")
    
    def log_message(self, format, *args):
        """Custom log format"""
        print(f"[API] {format % args}")

def main():
    port = 8001  # Use a different port to avoid conflicts
    server = HTTPServer(('localhost', port), DashboardAPIHandler)
    
    print(f"API server running on http://localhost:{port}")
    print("Dashboard available at: http://localhost:8001/dashboard.html")
    print("Press Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nAPI server stopped")

if __name__ == "__main__":
    main()