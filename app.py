import os
import threading
import time
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_mail import Mail, Message
import random
import string

app = Flask(__name__, static_folder='static')
app.secret_key = "herdem1940gizlianahtar"  # Session için gerekli

# E-posta ayarları
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'herdemerasmus@gmail.com'
app.config['MAIL_PASSWORD'] = 'kmop hzuo yoqp ztnr'  # Uygulama şifresi
app.config['MAIL_DEFAULT_SENDER'] = 'herdemerasmus@gmail.com'

mail = Mail(app)

# Sabit anahtarlar ile veri sözlüğü
data_dict = {
    "kapi": False,
    "vantilator": False,
    "pencere": False,
    "perde": False
}

# Kullanıcı bilgileri
USER_CREDENTIALS = {
    "herdem": "1940"
}

# Onay kodları için depolama
verification_codes = {}

# Kapı zamanlayıcı fonksiyonu
def kapi_timer():
    time.sleep(10)
    data_dict["kapi"] = False
    print("Kapı otomatik olarak kapatıldı")

@app.route('/')
def index():
    if 'logged_in' in session and session['logged_in']:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
        # Doğrulama kodu oluştur
        verification_code = ''.join(random.choices(string.digits, k=6))
        verification_codes[username] = verification_code
        
        # E-posta gönderme
        try:
            msg = Message(
                subject='Akıllı Ev Sistemi Doğrulama Kodu',
                recipients=['hidayete369@gmail.com'],
                body=f'Merhaba {username}, doğrulama kodunuz: {verification_code}'
            )
            mail.send(msg)
            session['username'] = username
            session['waiting_verification'] = True
            return redirect(url_for('verify'))
        except Exception as e:
            return render_template('login.html', error=f"E-posta gönderilirken hata oluştu: {str(e)}")
    else:
        return render_template('login.html', error="Kullanıcı adı veya şifre hatalı!")

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = session['username']
        submitted_code = request.form.get('verification_code')
        
        if username in verification_codes and verification_codes[username] == submitted_code:
            session['logged_in'] = True
            session.pop('waiting_verification', None)
            return redirect(url_for('dashboard'))
        else:
            return render_template('verify.html', error="Doğrulama kodu hatalı!")
    
    return render_template('verify.html')

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('index'))
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/api/data', methods=['GET'])
def get_data():
    """Veri sözlüğünden veri getir"""
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({"error": "Yetkisiz erişim"}), 401
    
    return jsonify(data_dict), 200

@app.route('/api/update', methods=['POST'])
def update_data():
    """Veri sözlüğündeki değerleri güncelle"""
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({"error": "Yetkisiz erişim"}), 401
    
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Güncellenecek en az bir değer gerekli"}), 400
    
    updated = {}
    for key, value in data.items():
        if key in data_dict:
            data_dict[key] = value
            updated[key] = value
            
            # Kapı açılırsa 10 saniye sonra otomatik kapatma
            if key == "kapi" and value == True:
                timer_thread = threading.Thread(target=kapi_timer)
                timer_thread.daemon = True
                timer_thread.start()
    
    return jsonify({"success": True, "updated": updated}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
