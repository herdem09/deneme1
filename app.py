import os
import time
import threading
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string

app = Flask(__name__, static_url_path='/static')
CORS(app)
app.secret_key = 'herdem1940gizlianahtar'
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 dakika oturum süresi

# Sabit anahtarlar ile veri sözlüğü
data_dict = {
    "kapi": False,
    "vantilator": False,
    "pencere": False,
    "perde": False
}

# Otomatik kapi kapatma görevi
def otomatik_kapi_kapat():
    time.sleep(10)  # 10 saniye bekle
    data_dict["kapi"] = False
    print("Kapı otomatik olarak kapatıldı.")

# Kullanıcı bilgileri
KULLANICI_ADI = "herdem"
SIFRE = "1940"

# Mail göndermek için bilgiler
GONDEREN_EMAIL = "herdemerasmus@gmail.com"
ALICI_EMAIL = "hidayete369@gmail.com"
UYGULAMA_KODU = "kmop hzuo yoqp ztnr"

# Onay kodları saklamak için sözlük
onay_kodlari = {}

@app.route('/')
def ana_sayfa():
    """Ana sayfa - Giriş ekranına yönlendir"""
    if 'kullanici_adi' in session:
        return redirect(url_for('dashboard'))
    return render_template('giris.html')

@app.route('/giris', methods=['POST'])
def giris_kontrol():
    """Kullanıcı girişini kontrol et"""
    kullanici_adi = request.form.get('kullanici_adi')
    sifre = request.form.get('sifre')
    
    if kullanici_adi == KULLANICI_ADI and sifre == SIFRE:
        # Onay kodu oluştur
        onay_kodu = ''.join(random.choices(string.digits, k=6))
        onay_kodlari[kullanici_adi] = onay_kodu
        
        # E-posta gönder
        try:
            gonder_onay_maili(onay_kodu)
            return render_template('onay.html', kullanici_adi=kullanici_adi)
        except Exception as e:
            return render_template('giris.html', hata=f"E-posta gönderilirken hata oluştu: {str(e)}")
    else:
        return render_template('giris.html', hata="Kullanıcı adı veya şifre hatalı")

def gonder_onay_maili(kod):
    """Onay e-postası gönder"""
    mesaj = MIMEMultipart()
    mesaj['From'] = GONDEREN_EMAIL
    mesaj['To'] = ALICI_EMAIL
    mesaj['Subject'] = "Akıllı Ev Sistemi Giriş Onay Kodu"
    
    icerik = f"""
    Merhaba,
    
    Akıllı ev sistemine giriş için onay kodunuz: {kod}
    
    Bu kodu giriş ekranında kullanınız.
    
    İyi günler.
    """
    
    mesaj.attach(MIMEText(icerik, 'plain'))
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(GONDEREN_EMAIL, UYGULAMA_KODU)
    server.send_message(mesaj)
    server.quit()

@app.route('/onay', methods=['POST'])
def onay_kontrol():
    """Onay kodunu kontrol et"""
    kullanici_adi = request.form.get('kullanici_adi')
    onay_kodu = request.form.get('onay_kodu')
    
    if kullanici_adi in onay_kodlari and onay_kodlari[kullanici_adi] == onay_kodu:
        session['kullanici_adi'] = kullanici_adi
        del onay_kodlari[kullanici_adi]  # Kullanılmış kodu sil
        return redirect(url_for('dashboard'))
    else:
        return render_template('onay.html', kullanici_adi=kullanici_adi, hata="Geçersiz onay kodu")

@app.route('/dashboard')
def dashboard():
    """Dashboard sayfası"""
    if 'kullanici_adi' not in session:
        return redirect(url_for('ana_sayfa'))
    return render_template('dashboard.html', veriler=data_dict)

@app.route('/cikis')
def cikis():
    """Oturumu sonlandır"""
    session.pop('kullanici_adi', None)
    return redirect(url_for('ana_sayfa'))

@app.route('/api/veri', methods=['GET'])
def veri_getir():
    """Veri sözlüğünden veri getir"""
    if 'kullanici_adi' not in session:
        return jsonify({"hata": "Yetkisiz erişim"}), 401
    
    return jsonify(data_dict), 200

@app.route('/api/guncelle', methods=['POST'])
def veri_guncelle():
    """Veri sözlüğündeki değerleri güncelle"""
    if 'kullanici_adi' not in session:
        return jsonify({"hata": "Yetkisiz erişim"}), 401
    
    data = request.get_json()
    
    if not data:
        return jsonify({"hata": "Güncellenecek en az bir değer gerekli"}), 400
    
    # Değerleri güncelle
    for key, value in data.items():
        if key in data_dict:
            data_dict[key] = value
            
            # Eğer kapı açıldıysa, 10 saniye sonra otomatik kapanacak
            if key == "kapi" and value == True:
                thread = threading.Thread(target=otomatik_kapi_kapat)
                thread.daemon = True
                thread.start()
    
    return jsonify({"basari": True, "veriler": data_dict}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
