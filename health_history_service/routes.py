from flask import Blueprint, jsonify, request, render_template
from database import get_db_connection

health_history_bp = Blueprint('health_history', __name__)

@health_history_bp.route('/')
def index():
    return render_template('index.html')

@health_history_bp.route('/api/health-history', methods=['GET'])
def get_health_history():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM health_history ORDER BY created_at DESC')
    history = cursor.fetchall()
    conn.close()
    return jsonify(history)

@health_history_bp.route('/api/health-history', methods=['POST'])
def add_health_history():
    data = request.get_json()
    
    if not data or 'nama' not in data or 'status' not in data:
        return jsonify({'error': 'Nama dan status harus diisi'}), 400
    
    if data['status'] not in ['sakit', 'perawatan', 'sehat']:
        return jsonify({'error': 'Status tidak valid. Gunakan: sakit, perawatan, atau sehat'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO health_history (nama, status) VALUES (%s, %s)"
    cursor.execute(query, (data['nama'], data['status']))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Data berhasil ditambahkan'}), 201

@health_history_bp.route('/api/health-history/<int:id>', methods=['GET'])
def get_health_history_by_id(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM health_history WHERE id = %s', (id,))
    history = cursor.fetchone()
    conn.close()
    
    if not history:
        return jsonify({'error': 'Data tidak ditemukan'}), 404
    
    return jsonify(history)

@health_history_bp.route('/api/health-history/nama/<string:nama>', methods=['GET'])
def get_health_history_by_name(nama):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM health_history WHERE nama = %s ORDER BY created_at DESC', (nama,))
    history = cursor.fetchall()
    conn.close()
    
    if not history:
        return jsonify({'error': 'Data tidak ditemukan'}), 404
    
    return jsonify(history) 