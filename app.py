from flask import Flask, render_template_string
import requests

app = Flask(__name__)

SERVER_IP = "http://10.0.0.175:5000/api/durum"

HTML = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Blender.com - Durum</title>
</head>
<body>
    <h1>Akıllı Ev Durumu</h1>
    {% if data %}
        <h2>Alınan</h2>
        <pre>{{ data['alinan'] | tojson(indent=2) }}</pre>

        <h2>Olan</h2>
        <pre>{{ data['olan'] | tojson(indent=2) }}</pre>

        <h2>Giden</h2>
        <pre>{{ data['giden'] | tojson(indent=2) }}</pre>
    {% else %}
        <p>Veri alınamadı...</p>
    {% endif %}
</body>
</html>
"""

@app.route("/")
def home():
    try:
        response = requests.get(SERVER_IP, timeout=5)
        data = response.json()
    except Exception as e:
        print("Hata:", e)
        data = None
    return render_template_string(HTML, data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
