from flask import Flask
from routes import order_bp
from database import init_db

app = Flask(__name__)
app.register_blueprint(order_bp)

# Inisialisasi database saat aplikasi dimulai
init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
