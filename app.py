from flask import Flask, render_template
from werkzeug.security import generate_password_hash
from flask_talisman import Talisman
import os

app = Flask(__name__)
# Secure configuration
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = 1800

# Initialize Talisman
talisman = Talisman(
    app,
    force_https=not app.config.get('TESTING', False),
    strict_transport_security=True,
    session_cookie_secure=True,
    content_security_policy={
        'default-src': "'self'",
        'img-src': "'self' data:",
        'script-src': "'self'"
    }
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')
