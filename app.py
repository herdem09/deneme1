import os
import time
import threading
from flask import Flask, request, jsonify, render_template, send_from_directory

app = Flask(__name__, static_folder='static', template_folder='templates')

# Sabit anahtarlar ile veri sözlüğü
data_dict = {
    "kapi": False,
    "vantilator": False,
    "pencere": False,
    "perde": False
}

# API şifremiz
API_KEY = "herdem1940"

# Kullanıcı bilgileri
KULLANICI_ADI = "herdem"
SIFRE = "1940"

# E-posta doğrulama kodu
DOGRULAMA_KODU = "kmop hzuo yoqp ztnr"

# Kapı otomatik kapanma fonksiyonu
def kapi_otomatik_kapat():
    time.sleep(10)  # 10 saniye bekle
    data_dict["kapi"] = False
    print("Kapı otomatik olarak kapatıldı.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/giris', methods=['POST'])
def giris():
    data = request.get_json()
    kullanici_adi = data.get('kullanici_adi')
    sifre = data.get('sifre')
    
    if kullanici_adi == KULLANICI_ADI and sifre == SIFRE:
        return jsonify({"success": True}), 200
    else:
        return jsonify({"success": False, "mesaj": "Kullanıcı adı veya şifre hatalı!"}), 401

@app.route('/dogrula', methods=['POST'])
def dogrula():
    data = request.get_json()
    kod = data.get('kod')
    
    if kod == DOGRULAMA_KODU:
        return jsonify({"success": True}), 200
    else:
        return jsonify({"success": False, "mesaj": "Doğrulama kodu hatalı!"}), 401

@app.route('/data', methods=['GET'])
def get_data():
    """Veri sözlüğünden veri getir"""
    # Şifre kontrolü
    auth_key = request.headers.get('Authorization', '')
    if not auth_key.startswith(API_KEY):
        return jsonify({"error": "Yetkisiz erişim"}), 401
    
    # Belirli bir veriyi getirme
    key = request.args.get('key')
    if key:
        if key in data_dict:
            return jsonify({key: data_dict[key]}), 200
        else:
            return jsonify({"error": f"'{key}' bulunamadı"}), 404
    
    # Tüm veriyi getirme
    return jsonify(data_dict), 200

@app.route('/data', methods=['POST'])
def update_data():
    """Veri sözlüğündeki değerleri güncelle"""
    # Şifre kontrolü
    auth_key = request.headers.get('Authorization', '')
    if not auth_key.startswith(API_KEY):
        return jsonify({"error": "Yetkisiz erişim"}), 401
    
    # JSON verisi kontrolü
    if not request.is_json:
        return jsonify({"error": "JSON formatında veri gönderilmeli"}), 400
    
    data = request.get_json()
    
    # İstek boş olmamalı
    if not data:
        return jsonify({"error": "Güncellenecek en az bir değer gerekli"}), 400
    
    # Sadece mevcut anahtarları güncelle
    updated = {}
    
    for key, value in data.items():
        if key in data_dict:
            data_dict[key] = value
            updated[key] = value
            
            # Kapı açıldıysa 10 saniye sonra otomatik kapanma işlemi
            if key == "kapi" and value == True:
                kapi_thread = threading.Thread(target=kapi_otomatik_kapat)
                kapi_thread.daemon = True
                kapi_thread.start()
    
    return jsonify({"success": True, "updated": updated}), 200

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    # Klasörleri oluştur
    os.makedirs('static', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
