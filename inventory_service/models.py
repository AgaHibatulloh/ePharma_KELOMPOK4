from database import get_db_connection

def tambah_kategori(nama_kategori):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO kategori_obat (nama_kategori) VALUES (%s)"
    cursor.execute(query, (nama_kategori,))
    conn.commit()
    conn.close()

def tambah_obat(nama, stok, kategori_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = "INSERT INTO obat (nama_obat, stok, kategori_id) VALUES (%s, %s, %s)"
        cursor.execute(query, (nama, stok, kategori_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def get_all_obat():
    """
    Mengambil daftar semua obat dari database beserta kategorinya
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT o.*, k.nama_kategori 
        FROM obat o 
        JOIN kategori_obat k ON o.kategori_id = k.id
    """
    cursor.execute(query)
    obat = cursor.fetchall()
    cursor.close()
    conn.close()
    return obat

def get_all_kategori():
    """
    Mengambil semua kategori obat dari database
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM kategori_obat")
    kategori = cursor.fetchall()
    cursor.close()
    conn.close()
    return kategori

def get_kategori():
    """
    Alias untuk get_all_kategori (untuk kompatibilitas)
    """
    return get_all_kategori()

def get_obat_by_id(id):
    """
    Mengambil data obat berdasarkan ID
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT o.*, k.nama_kategori 
        FROM obat o 
        JOIN kategori_obat k ON o.kategori_id = k.id 
        WHERE o.id = %s
    """
    cursor.execute(query, (id,))
    obat = cursor.fetchone()
    cursor.close()
    conn.close()
    return obat

def update_obat(id, nama_obat, stok, kategori_id):
    """
    Memperbarui data obat
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = "UPDATE obat SET nama_obat = %s, stok = %s, kategori_id = %s WHERE id = %s"
        cursor.execute(query, (nama_obat, stok, kategori_id, id))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def delete_obat(id):
    """
    Menghapus obat dari database
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = "DELETE FROM obat WHERE id = %s"
        cursor.execute(query, (id,))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()
