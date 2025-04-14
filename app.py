import os
import time
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from functools import wraps

app = Flask(__name__, static_url_path='/static')
app.secret_key = "herdemsecretkey123"  # Session için gerekli

# Sabit kullanıcı bilgileri
KULLANICI_ADI = "herdem"
SIFRE = "1940"
UYGULAMA_KODU = "kmop hzuo yoqp ztnr"

# E-posta ayarları
GONDEREN_EMAIL = "herdemerasmus@gmail.com"
ALICI_EMAIL = "hidayete369@gmail.com"

# Sabit anahtarlar ile veri sözlüğü
data_dict = {
    "kapi": False,
    "vantilator": False,
    "pencere": False,
    "perde": False
}

# Doğrulama kodları için geçici depolama
onay_kodlari = {}

# Oturum gerektiren sayfalar için dekoratör
def oturum_gerekli(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'giris_yapildi' not in session or not session['giris_yapildi']:
            return redirect(url_for('giris_sayfasi'))
        return f(*args, **kwargs)
    return decorated_function

# Kapı otomatik kapanma işlevi
def kapi_otomatik_kapat():
    time.sleep(10)  # 10 saniye bekle
    data_dict["kapi"] = False
    print("Kapı otomatik olarak kapatıldı")

@app.route('/')
def giris_sayfasi():
    """Giriş sayfasını göster"""
    return render_template('giris.html')

@app.route('/giris', methods=['POST'])
def giris_kontrol():
    """Kullanıcı girişini kontrol et"""
    kullanici_adi = request.form.get('kullanici_adi')
    sifre = request.form.get('sifre')
    
    if kullanici_adi == KULLANICI_ADI and sifre == SIFRE:
        # Doğrulama kodu oluştur ve e-posta gönder
        import random
        dogrulama_kodu = str(random.randint(100000, 999999))
        session['dogrulama_kodu'] = dogrulama_kodu
        
        # E-posta gönderme
        baslik = "Giriş Doğrulama Kodu"
        icerik = f"Merhaba {kullanici_adi},\n\nGiriş doğrulama kodunuz: {dogrulama_kodu}\n\nUygulama kodu: {UYGULAMA_KODU}"
        
        try:
            email_gonder(GONDEREN_EMAIL, ALICI_EMAIL, baslik, icerik)
            return render_template('dogrulama.html')
        except Exception as e:
            return render_template('giris.html', hata=f"E-posta gönderme hatası: {str(e)}")
    else:
        return render_template('giris.html', hata="Kullanıcı adı veya şifre hatalı!")

def email_gonder(gonderen, alici, baslik, icerik):
    """Basit e-posta gönderme simülasyonu"""
    # Gerçek bir uygulamada SMTP sunucusu ile e-posta gönderilir
    # Bu örnek için sadece simülasyon yapıyoruz
    print(f"E-posta gönderildi:")
    print(f"Kimden: {gonderen}")
    print(f"Kime: {alici}")
    print(f"Konu: {baslik}")
    print(f"İçerik: {icerik}")
    
    # Gerçek e-posta göndermek için yorum satırlarını kaldırın:
    """
    mesaj = MIMEMultipart()
    mesaj['From'] = gonderen
    mesaj['To'] = alici
    mesaj['Subject'] = baslik
    mesaj.attach(MIMEText(icerik, 'plain'))
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(gonderen, 'uygulama_sifresi')  # Gmail için uygulama şifresi gerekir
        server.send_message(mesaj)
    """
    return True

@app.route('/dogrulama', methods=['POST'])
def dogrulama_kontrol():
    """Doğrulama kodunu kontrol et"""
    dogrulama_kodu = request.form.get('dogrulama_kodu')
    
    if dogrulama_kodu == session.get('dogrulama_kodu'):
        session['giris_yapildi'] = True
        return redirect(url_for('dashboard'))
    else:
        return render_template('dogrulama.html', hata="Doğrulama kodu hatalı!")


@app.route('/dashboard')
@oturum_gerekli
def dashboard():
    """Dashboard sayfasını göster"""
    return render_template('dashboard.html', data=data_dict)

@app.route('/veri', methods=['GET'])
@oturum_gerekli
def veri_getir():
    """AJAX ile veri alımı için endpoint"""
    return jsonify(data_dict)

@app.route('/guncelle', methods=['POST'])
@oturum_gerekli
def veri_guncelle():
    """AJAX ile veri güncelleme için endpoint"""
    yeni_data = request.get_json()
    
    # Değerleri güncelle
    for key, value in yeni_data.items():
        if key in data_dict:
            data_dict[key] = value
            
            # Kapı açıldıysa, 10 saniye sonra otomatik kapanma için thread başlat
            if key == "kapi" and value == True:
                threading.Thread(target=kapi_otomatik_kapat).start()
    
    return jsonify({"success": True, "data": data_dict})

@app.route('/cikis')
def cikis():
    """Kullanıcı çıkışı"""
    session.clear()
    return redirect(url_for('giris_sayfasi'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
