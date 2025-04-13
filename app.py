import os
import time
import threading
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
from flask_mail import Mail, Message
import random
import string

app = Flask(__name__, static_url_path='/static')
CORS(app)
app.secret_key = 'herdem1940gizlianahtar'

# Mail yapılandırması
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'herdemerasmus@gmail.com'
app.config['MAIL_PASSWORD'] = 'kmop hzuo yoqp ztnr'  # Uygulama şifresi
app.config['MAIL_DEFAULT_SENDER'] = 'herdemerasmus@gmail.com'

mail = Mail(app)

# Kullanıcı bilgileri
KULLANICI_ADI = "herdem"
SIFRE = "1940"
ONAY_MAIL_ALICISI = "hidayete369@gmail.com"

# Sabit anahtarlar ile veri sözlüğü
data_dict = {
    "kapi": False,
    "vantilator": False,
    "pencere": False,
    "perde": False,
    "isik": False
}

# Onay kodları için depolama
onay_kodlari = {}

# Kapı otomatik kapatma işlevini kontrol eden fonksiyon
def kapi_otomatik_kapat():
    time.sleep(10)  # 10 saniye bekle
    data_dict["kapi"] = False
    print("Kapı otomatik olarak kapatıldı")

@app.route('/')
def ana_sayfa():
    if session.get('giris_yapildi', False):
        return redirect(url_for('dashboard'))
    return render_template('giris.html')

@app.route('/login', methods=['POST'])
def giris():
    kullanici_adi = request.form.get('kullanici_adi')
    sifre = request.form.get('sifre')
    
    if kullanici_adi == KULLANICI_ADI and sifre == SIFRE:
        # Rastgele onay kodu oluştur
        onay_kodu = ''.join(random.choices(string.digits, k=6))
        onay_kodlari[kullanici_adi] = onay_kodu
        
        # Onay E-postası gönder
        try:
            msg = Message(
                subject="Akıllı Ev Sistemi - Giriş Onay Kodu",
                recipients=[ONAY_MAIL_ALICISI],
                body=f"Merhaba! Akıllı ev sisteminize giriş için onay kodunuz: {onay_kodu}"
            )
            mail.send(msg)
            session['bekleyen_kullanici'] = kullanici_adi
            return render_template('onay_kodu.html')
        except Exception as e:
            return render_template('giris.html', hata="E-posta gönderimi sırasında bir hata oluştu.")
    else:
        return render_template('giris.html', hata="Kullanıcı adı veya şifre hatalı!")

@app.route('/dogrula', methods=['POST'])
def onay_kodu_dogrula():
    giris_kodu = request.form.get('onay_kodu')
    kullanici_adi = session.get('bekleyen_kullanici')
    
    if kullanici_adi and giris_kodu == onay_kodlari.get(kullanici_adi):
        session['giris_yapildi'] = True
        return redirect(url_for('dashboard'))
    else:
        return render_template('onay_kodu.html', hata="Onay kodu hatalı!")

@app.route('/dashboard')
def dashboard():
    if not session.get('giris_yapildi', False):
        return redirect(url_for('ana_sayfa'))
    return render_template('dashboard.html')

@app.route('/cikis')
def cikis():
    session.clear()
    return redirect(url_for('ana_sayfa'))

@app.route('/api/data', methods=['GET'])
def get_data():
    """Veri sözlüğünden veri getir"""
    if not session.get('giris_yapildi', False):
        return jsonify({"error": "Yetkisiz erişim"}), 401
    
    return jsonify(data_dict), 200

@app.route('/api/data', methods=['POST'])
def update_data():
    """Veri sözlüğündeki değerleri güncelle"""
    if not session.get('giris_yapildi', False):
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
            
            # Kapı açıldıysa 10 saniye sonra otomatik kapat
            if key == "kapi" and value == True:
                thread = threading.Thread(target=kapi_otomatik_kapat)
                thread.daemon = True
                thread.start()
    
    return jsonify({"success": True, "updated": updated}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
