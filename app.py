import requests

def veri_cek():
    try:
        # 10.0.0.175 IP adresinden veri alma
        response = requests.get("http://10.0.0.175:4999/api/durum")
        
        if response.status_code == 200:
            # JSON verisini al
            veri = response.json()
            print("Veri alındı:", veri)
            return veri
        else:
            print(f"Error: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None
