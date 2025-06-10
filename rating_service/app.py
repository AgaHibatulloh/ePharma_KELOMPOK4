from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import time
from sqlalchemy.exc import OperationalError
import google.generativeai as genai

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{os.environ.get('DB_USER', 'root')}:{os.environ.get('DB_PASSWORD', 'root')}@{os.environ.get('DB_HOST', 'rating-db')}/{os.environ.get('DB_NAME', 'rating_db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Konfigurasi Gemini
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'AIzaSyDOUCIHbXbVz5j7QT9VNMQiWTYi7YplEa4')
print("[DEBUG] Mengatur API Key Gemini...")
genai.configure(api_key=GEMINI_API_KEY)

def init_db():
    max_retries = 5
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            with app.app_context():
                db.create_all()
            print("Database initialized successfully!")
            return
        except OperationalError as e:
            if attempt < max_retries - 1:
                print(f"Database connection failed. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Failed to connect to database after multiple attempts.")
                raise e

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)

@app.route('/api/rating', methods=['POST'])
def add_rating():
    data = request.json
    new_rating = Rating(rating=data['rating'], description=data['description'])
    db.session.add(new_rating)
    db.session.commit()
    return jsonify({'message': 'Rating added successfully'}), 201

@app.route('/api/rating', methods=['GET'])
def get_ratings():
    ratings = Rating.query.all()
    return jsonify([{'id': r.id, 'rating': r.rating, 'description': r.description} for r in ratings])

@app.route('/api/rating/<int:id>', methods=['GET'])
def get_rating(id):
    rating = Rating.query.get_or_404(id)
    return jsonify({'id': rating.id, 'rating': rating.rating, 'description': rating.description})

@app.route('/api/rating/<int:id>', methods=['PUT'])
def update_rating(id):
    rating = Rating.query.get_or_404(id)
    data = request.json
    rating.rating = data['rating']
    rating.description = data['description']
    db.session.commit()
    return jsonify({'message': 'Rating updated successfully'})

@app.route('/api/rating/<int:id>', methods=['DELETE'])
def delete_rating(id):
    rating = Rating.query.get_or_404(id)
    db.session.delete(rating)
    db.session.commit()
    return jsonify({'message': 'Rating deleted successfully'})

@app.route('/api/recommendation', methods=['GET'])
def get_recommendation():
    # Contoh rekomendasi buku kesehatan (bisa diganti dengan logika yang lebih kompleks)
    books = [
        {'title': 'Buku Kesehatan 1', 'author': 'Penulis 1'},
        {'title': 'Buku Kesehatan 2', 'author': 'Penulis 2'},
        {'title': 'Buku Kesehatan 3', 'author': 'Penulis 3'}
    ]
    return jsonify(books)

@app.route('/api/gemini/recommend', methods=['POST'])
def get_gemini_recommendation():
    try:
        print("[DEBUG] ====== MULAI REQUEST GEMINI ======")
        print("[DEBUG] Headers:", dict(request.headers))
        print("[DEBUG] Raw data:", request.get_data())
        
        data = request.get_json()
        print("[DEBUG] Parsed JSON data:", data)
        
        if not data or 'prompt' not in data:
            print("[ERROR] Data request tidak valid")
            return jsonify({
                'error': 'Data request tidak valid',
                'details': 'Prompt tidak ditemukan dalam request'
            }), 400

        title = data.get('prompt', '')
        print(f"[DEBUG] Memproses judul buku: {title}")
        
        # Inisialisasi model Gemini
        print("[DEBUG] Mencoba menginisialisasi model Gemini...")
        model = genai.GenerativeModel('gemini-2.0-flash')
        print("[DEBUG] Model Gemini berhasil diinisialisasi")
        
        # Generate rekomendasi
        prompt = f"""Berikan rekomendasi singkat (1-2 kalimat) untuk buku dengan judul "{title}". 
        Fokus pada aspek kesehatan jika buku tersebut berhubungan dengan kesehatan. 
        Jika tidak berhubungan dengan kesehatan, berikan rekomendasi yang jujur."""
        
        print("[DEBUG] Prompt yang akan dikirim:", prompt)
        print("[DEBUG] Mengirim prompt ke Gemini...")
        
        # Tambahkan retry logic
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                response = model.generate_content(prompt)
                print("[DEBUG] Response dari Gemini:", response.text)
                return jsonify({
                    'recommendation': response.text
                })
            except Exception as e:
                print(f"[ERROR] Attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    print(f"[DEBUG] Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    raise e
                    
    except Exception as e:
        print(f"[ERROR] ====== ERROR DALAM GEMINI RECOMMENDATION ======")
        print(f"[ERROR] Error message: {str(e)}")
        import traceback
        print(f"[ERROR] Traceback: {traceback.format_exc()}")
        return jsonify({
            'error': 'Gagal mendapatkan rekomendasi',
            'details': str(e)
        }), 500

@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not Found', 'message': 'The requested URL was not found on the server.'}), 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000) 