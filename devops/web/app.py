from flask import Flask, jsonify
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        'status': 'ok',
        'message': 'Coolify Volume Bug Demo',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

@app.route('/write-test')
def write_test():
    """Write test files to static and media directories to verify volume mounting"""
    results = {}

    # Write to static directory
    try:
        static_file = '/var/www/static/test.txt'
        with open(static_file, 'w') as f:
            f.write(f'Written by web service at {datetime.now().isoformat()}\n')
        results['static'] = f'✓ Successfully wrote to {static_file}'
    except Exception as e:
        results['static'] = f'✗ Failed to write to static: {str(e)}'

    # Write to media directory
    try:
        media_file = '/var/www/media/test.txt'
        with open(media_file, 'w') as f:
            f.write(f'Written by web service at {datetime.now().isoformat()}\n')
        results['media'] = f'✓ Successfully wrote to {media_file}'
    except Exception as e:
        results['media'] = f'✗ Failed to write to media: {str(e)}'

    # List files in static directory
    try:
        static_files = os.listdir('/var/www/static')
        results['static_files'] = static_files
    except Exception as e:
        results['static_files'] = f'Error: {str(e)}'

    # List files in media directory
    try:
        media_files = os.listdir('/var/www/media')
        results['media_files'] = media_files
    except Exception as e:
        results['media_files'] = f'Error: {str(e)}'

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
