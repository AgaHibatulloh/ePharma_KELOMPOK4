import google.generativeai as genai
import os
import traceback

# Debug API Key (jangan lupa ganti ini ke environment variable di produksi!)
genai_api_key = "AIzaSyDOUCIHbXbVz5j7QT9VNMQiWTYi7YplEa4"
print("[DEBUG] Mengatur API Key...")
genai.configure(api_key=genai_api_key)

def konsultasi_ai_gemini(keluhan):
    print("[DEBUG] Mulai fungsi konsultasi_ai_gemini")
    prompt = f"""
    Keluhan: {keluhan}

    Jawablah dengan format ringkas seperti ini:
    - Diagnosis Kemungkinan Utama:
    - Obat yang Dapat Diberikan (opsional, jika sesuai dan tidak berbahaya):
    - Saran Lanjut: (misalnya periksa ke dokter, cek lab, dll)
    
    Jangan beri penjelasan terlalu panjang. Batasi maksimal 5-6 baris. Jangan beri disclaimer panjang.
    """
    
    try:
        # Initialize model
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Generate content
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        print("[ERROR] Terjadi Exception:")
        traceback.print_exc()
        return f"Traceback:\n{traceback.format_exc()}"