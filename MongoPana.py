#Menambahkan library
from flask import Flask, request, jsonify
from pymongo import MongoClient
import requests  

app = Flask(__name__)

# Koneksi MongoDB
client = MongoClient("mongodb+srv://rilcuy581:Qv8za657bbt1EQlA@cluster1.mxtme.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1")
db = client["MyDatabase"]
collection = db["MyCollection"]

# Konfigurasi Ubidots
UBIDOTS_TOKEN = "BBUS-PTOJgseWVqlyUbCPEhDa0yZP3073dl"
DEVICE_LABEL = "esp32-panavators"
UBIDOTS_URL = f"http://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_LABEL}"
UBIDOTS_HEADERS = {
    'X-Auth-Token': UBIDOTS_TOKEN,
    'Content-Type': 'application/json'
}


@app.route("/api/dht", methods=["POST"])

#Definisi untuk enerima data
def receive_data():
    #Pengecekan error
    try:
        data = request.json
        if not all(k in data for k in ("temperature", "humidity", "pir_value")):
            return jsonify({"error": "Missing data fields"}), 400

        # Simpan ke MongoDB
        collection.insert_one(data)

        # Kirim ke Ubidots
        ubidots_payload = {
            "temperature": data["temperature"],
            "humidity": data["humidity"],
            "pir_value": data["pir_value"]
        }
        
        ubidots_response = requests.post(UBIDOTS_URL, headers=UBIDOTS_HEADERS, json=ubidots_payload)
        ubidots_response.raise_for_status()  # Cek error HTTP
        
        return jsonify({
            "message": "Data saved",
            "ubidots_response": ubidots_response.json()
        }), 201

    except requests.exceptions.RequestException as e:
        return jsonify({"message": "Data saved to MongoDB", "ubidots_error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#Mengambil data dari MongoDB ke web
@app.route("/api/dht", methods=["GET"])
def get_data():
    data = list(collection.find({}, {"_id": 0}))
    return jsonify(data), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
