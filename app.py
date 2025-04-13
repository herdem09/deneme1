# app.py
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Sabit anahtarlar ile veri sözlüğü
data_dict = {
    "kapi": None,
    "isik": None,
    "pencere": None,
    "perde": None,
    "vantilator": None
}

# API şifremiz
API_KEY = "herdem1940"

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
    
    return jsonify({"success": True, "updated": updated}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
