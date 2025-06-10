import mysql.connector
import os

def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASSWORD', 'root'),
        database=os.environ.get('DB_NAME', 'health_history_db')
    )

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Buat tabel health_history
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS health_history (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nama VARCHAR(255) NOT NULL,
            status ENUM('sakit', 'perawatan', 'sehat') NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close() 