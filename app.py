from flask import Flask, render_template
from werkzeug.security import generate_password_hash
from flask_talisman import Talisman
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# Secure configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', os.urandom(24))
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = 1800

# Initialize Talisman with configurable HTTPS
use_ssl = os.getenv('USE_SSL', 'false').lower() == 'true'
talisman = Talisman(
    app,
    force_https=use_ssl,
    strict_transport_security=True,
    session_cookie_secure=True,
    content_security_policy={
        'default-src': "'self'",
        'img-src': '*',
        'script-src': ["'self'", "'unsafe-inline'"],
        'style-src': ["'self'", "'unsafe-inline'"]
    }
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    ssl_context = 'adhoc' if use_ssl else None
    app.run(host=host, port=port, ssl_context=ssl_context)
