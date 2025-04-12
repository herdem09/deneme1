import time
import threading
import flask
from flask import Flask, request, jsonify

app = Flask(__name__)

data_alinan = {
    "kapi_gelen": False,
    "vantilator_gelen": False,
    "pencere_gelen": False,
    "ampul_gelen": False,
    "perde_gelen": False,
    "isik_gelen": False,
    "sicaklik_gelen": 25,
    "isik_oto_gelen": True,
    "sicaklik_oto_gelen": True,
    "birinci_esik_gelen": 22,
    "ikinci_esik_gelen": 28,
}

data_son_alinan = {
    "kapi_gelen": False,
    "vantilator_gelen": False,
    "pencere_gelen": False,
    "ampul_gelen": False,
    "perde_gelen": False,
    "isik_gelen": False,
    "sicaklik_gelen": 25,
    "isik_oto_gelen": True,
    "sicaklik_oto_gelen": True,
    "birinci_esik_gelen": 22,
    "ikinci_esik_gelen": 28,
}

data_olan = {
    "kapi": False,
    "vantilator": False,
    "pencere": False,
    "ampul": False,
    "perde": False,
    "isik": True,  # True ise aydınlık, False ise karanlık
    "sicaklik": 25,
    "sicaklik_oto": True,
    "isik_oto": True,
    "birinci_esik": 22,
    "ikinci_esik": 28,
}

data_giden = {
    "kapi": False,
    "vantilator": False,
    "pencere": False,
    "ampul": False,
    "perde": False,
}

kapi_acildi = None  # Başlangıçta kapi_acildi None olarak tanımlandı


def kapi():
    if kapi_acildi is None:
        return False  # İlk defa çağrıldığında False döndürebiliriz
    simdi = time.time()
    zaman_fark = simdi - kapi_acildi
    if zaman_fark > 10:
        return False
    else:
        return True


def alinandan_olana():
    global kapi_acildi  # kapi_acildi değişkenini global olarak kullanıyoruz
    global data_son_alinan  # data_son_alinan'ı da global olarak kullanıyoruz
    global data_alinan
    
    if data_son_alinan != data_alinan:
        if data_alinan["kapi_gelen"] == True:
            kapi_acildi = time.time()  # kapi açılma zamanını kaydet
            kapi()  # kapi fonksiyonunu çağır
            data_olan["kapi"] = True
            data_giden["kapi"] = True
            data_alinan["kapi_gelen"] = False

        if data_alinan["vantilator_gelen"] == True and data_olan["sicaklik_oto"] == False:
            data_olan["vantilator"] = data_alinan["vantilator_gelen"]
            data_giden["vantilator"] = data_alinan["vantilator_gelen"]
        elif data_alinan["vantilator_gelen"] == False and data_olan["sicaklik_oto"] == False:
            data_olan["vantilator"] = data_alinan["vantilator_gelen"]
            data_giden["vantilator"] = data_alinan["vantilator_gelen"]
        else:
            data_alinan["vantilator_gelen"] = data_olan["vantilator"]

        if data_alinan["pencere_gelen"] == True and data_olan["sicaklik_oto"] == False:
            data_olan["pencere"] = data_alinan["pencere_gelen"]
            data_giden["pencere"] = data_alinan["pencere_gelen"]
        elif data_alinan["pencere_gelen"] == False and data_olan["sicaklik_oto"] == False:
            data_olan["pencere"] = data_alinan["pencere_gelen"]
            data_giden["pencere"] = data_alinan["pencere_gelen"]
        else:
            data_alinan["vantilator_gelen"] = data_olan["vantilator"]

        if data_alinan["ampul_gelen"] == True and data_olan["isik_oto"] == False:
            data_olan["ampul"] = data_alinan["ampul_gelen"]
            data_giden["ampul"] = data_alinan["ampul_gelen"]
        elif data_alinan["ampul_gelen"] == False and data_olan["isik_oto"] == False:
            data_olan["ampul"] = data_alinan["ampul_gelen"]
            data_giden["ampul"] = data_alinan["ampul_gelen"]
        else:
            data_alinan["ampul_gelen"] = data_olan["ampul"]

        if data_alinan["perde_gelen"] == True and data_olan["isik_oto"] == False:
            data_olan["perde"] = data_alinan["perde_gelen"]
            data_giden["perde"] = data_alinan["perde_gelen"]
        elif data_alinan["perde_gelen"] == False and data_olan["isik_oto"] == False:
            data_olan["perde"] = data_alinan["perde_gelen"]
            data_giden["perde"] = data_alinan["perde_gelen"]
        else:
            data_alinan["perde_gelen"] = data_olan["perde"]

        data_olan["isik"] = data_alinan["isik_gelen"]

        data_olan["sicaklik"] = data_alinan["sicaklik_gelen"]

        data_olan["isik_oto"] = data_alinan["isik_oto_gelen"]
        data_olan["sicaklik_oto"] = data_alinan["sicaklik_oto_gelen"]

        data_olan["birinci_esik"] = data_alinan["birinci_esik_gelen"]
        data_olan["ikinci_esik"] = data_alinan["ikinci_esik_gelen"]

        data_son_alinan = data_alinan.copy()  # Veriyi kopyalayarak güncelle


def otomasyon():
    if data_olan["sicaklik_oto"] == True:
        if data_olan["sicaklik"] > data_olan["ikinci_esik"]:
            data_olan["vantilator"] = True
            data_olan["pencere"] = True
            data_giden["vantilator"] = True
            data_giden["pencere"] = True
        elif data_olan["sicaklik"] > data_olan["birinci_esik"]:
            data_olan["vantilator"] = False
            data_olan["pencere"] = True
            data_giden["vantilator"] = False
            data_giden["pencere"] = True
        elif data_olan["sicaklik"] <= data_olan["birinci_esik"]:
            data_olan["vantilator"] = False
            data_olan["pencere"] = False
            data_giden["vantilator"] = False
            data_giden["pencere"] = False

    if data_olan["isik_oto"] == True:
        if data_olan["isik"] == False:
            data_olan["perde"] = False
            data_giden["perde"] = False
            data_olan["ampul"] = False
            data_giden["ampul"] = False
        else:
            data_olan["perde"] = True
            data_giden["perde"] = True
            data_olan["ampul"] = True
            data_giden["ampul"] = True


# Ana sayfa
@app.route('/')
def index():
    return "Akıllı Ev Kontrol Sistemi"


# API endpoint'i - veri alma
@app.route('/api/alinan', methods=['POST'])
def veri_al():
    global data_alinan
    gelen_veri = request.get_json()

    if gelen_veri:
        # Gelen verileri data_alinan'a ekle
        for key, value in gelen_veri.items():
            if key in data_alinan:
                data_alinan[key] = value

    # İşlemleri gerçekleştir
    alinandan_olana()
    otomasyon()
    data_olan["kapi"] = kapi()
    data_giden["kapi"] = kapi()

    return jsonify({"status": "success", "message": "Veriler alındı"})


# Mevcut durumu görüntüleme
@app.route('/api/durum', methods=['GET'])
def durum_getir():
    return jsonify({
        "alinan": data_alinan,
        "olan": data_olan,
        "giden": data_giden
    })


# Ana işlevlerin yönetimini sağlayan arka plan işlevi
def arka_plan_islevi():
    while True:
        try:
            alinandan_olana()
            otomasyon()
            data_olan["kapi"] = kapi()
            data_giden["kapi"] = kapi()
            time.sleep(1)
        except Exception as e:
            print(f"Arka plan işlevi hatası: {e}")
            time.sleep(5)  # Hata durumunda biraz bekle ve tekrar dene


# Arka plan thread'ini başlat
background_thread = None

def start_background_thread():
    global background_thread
    if background_thread is None or not background_thread.is_alive():
        background_thread = threading.Thread(target=arka_plan_islevi)
        background_thread.daemon = True
        background_thread.start()

# Uygulama başlangıcında arka plan thread'ini başlat
start_background_thread()

if __name__ == '__main__':
    # Portu Render'ın gerektirdiği şekilde ayarla
    import os
    port = int(os.environ.get('PORT', 10000))
    
    # Flask sunucusunu başlat
    app.run(debug=False, host='0.0.0.0', port=port)
