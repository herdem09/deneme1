from flask import Flask, request, jsonify

app = Flask(__name__)

# Veri saklama için dictionary
data_dict = {}

# API şifremiz
API_KEY = "herdem1940"

@app.route('/health', methods=['GET'])
def health_check():
    """Basit bir sağlık kontrolü endpoint'i"""
    return jsonify({"status": "healthy"}), 200

@app.route('/data', methods=['GET'])
def get_data():
    """Tüm veriyi veya belirli bir anahtarı getir"""
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
def add_data():
    """Dictionary'e veri ekle"""
    # Şifre kontrolü
    auth_key = request.headers.get('Authorization', '')
    if not auth_key.startswith(API_KEY):
        return jsonify({"error": "Yetkisiz erişim"}), 401
    
    # JSON verisi kontrolü
    if not request.is_json:
        return jsonify({"error": "JSON formatında veri gönderilmeli"}), 400
    
    data = request.get_json()
    
    # En az bir anahtar-değer çifti olmalı
    if not data:
        return jsonify({"error": "En az bir anahtar-değer çifti gerekli"}), 400
    
    # Veriyi dictionary'e ekle
    for key, value in data.items():
        data_dict[key] = value
    
    return jsonify({"message": "Veri başarıyla eklendi", "added": data}), 201

@app.route('/data/<key>', methods=['DELETE'])
def delete_data(key):
    """Dictionary'den veri sil"""
    # Şifre kontrolü
    auth_key = request.headers.get('Authorization', '')
    if not auth_key.startswith(API_KEY):
        return jsonify({"error": "Yetkisiz erişim"}), 401
    
    # Anahtarın varlığını kontrol et
    if key in data_dict:
        deleted_value = data_dict.pop(key)
        return jsonify({"message": f"'{key}' başarıyla silindi", "deleted_value": deleted_value}), 200
    else:
        return jsonify({"error": f"'{key}' bulunamadı"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
