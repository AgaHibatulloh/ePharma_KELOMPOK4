from flask import Flask
from routes import inventory_bp  # Pastikan routes.py berada dalam folder yang sama
from database import init_db

app = Flask(__name__)
app.register_blueprint(inventory_bp)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5002, debug=True)
