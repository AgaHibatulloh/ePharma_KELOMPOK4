import mysql.connector
import os

def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASSWORD', ''),
        database=os.environ.get('DB_NAME', 'service_db')
    )

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Buat tabel jika belum ada
    # Contoh untuk inventory service:
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS kategori_obat (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nama_kategori VARCHAR(255) NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS obat (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nama_obat VARCHAR(255) NOT NULL,
            stok INT NOT NULL,
            kategori_id INT,
            FOREIGN KEY (kategori_id) REFERENCES kategori_obat(id)
        )
    ''')
    
    conn.commit()
    conn.close()
