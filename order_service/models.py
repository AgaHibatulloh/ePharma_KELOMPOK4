from database import get_db_connection

def simpan_pesanan(nama_pemesan, id_obat, jumlah, kategori):
    status = "Normal"
    jumlah = int(jumlah)
    
    # Logika anomali berdasarkan kategori obat
    if kategori.lower() == 'merah':
        if jumlah > 3:
            status = "Anomali - Jumlah melebihi batas (max 3)"
        elif jumlah < 1:
            status = "Anomali - Jumlah tidak valid"
    elif kategori.lower() == 'kuning':
        if jumlah > 5:
            status = "Anomali - Jumlah melebihi batas (max 5)"
        elif jumlah < 1:
            status = "Anomali - Jumlah tidak valid"
    elif kategori.lower() == 'hijau':
        if jumlah > 10:
            status = "Anomali - Jumlah melebihi batas (max 10)"
        elif jumlah < 1:
            status = "Anomali - Jumlah tidak valid"
    else:
        status = "Anomali - Kategori tidak valid"
    
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO pesanan (nama_pemesan, id_obat, jumlah, kategori, status) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (nama_pemesan, id_obat, jumlah, kategori, status))
    conn.commit()
    conn.close()

def get_all_pesanan():
    """
    Mengambil semua data pesanan dari database
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM pesanan ORDER BY created_at DESC"
    cursor.execute(query)
    pesanan = cursor.fetchall()
    conn.close()
    return pesanan

def tambah_pesanan(nama_pemesan, jumlah):
    """
    Menambahkan pesanan baru
    """
    # Implementasi dummy
    print(f"Menambah pesanan untuk {nama_pemesan}, jumlah: {jumlah}")
    return {"id": 3, "nama_pemesan": nama_pemesan, "jumlah": jumlah, "status": "Baru"}
