import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN")  # Token de prueba de MercadoPago
last_payment = {}

@app.route("/")
def home():
    return "Servidor Flask con Webhooks funcionando"

@app.route("/webhook", methods=["POST"])
def webhook():
    global last_payment

    # Intentamos leer JSON (pagos reales)
    data = request.get_json(silent=True)

    if data and "data" in data and "id" in data["data"]:
        payment_id = data["data"]["id"]
        # Consultar la API de MercadoPago para confirmar estado
        url = f"https://api.mercadopago.com/v1/payments/{payment_id}"
        headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            payment_info = resp.json()
            last_payment = {
                "id": payment_info.get("id"),
                "status": payment_info.get("status"),
                "amount": payment_info.get("transaction_amount"),
                "payer": payment_info.get("payer", {}).get("email")
            }
            print("✅ Pago confirmado:", last_payment, flush=True)
        return jsonify({"status": "ok"}), 200

    # Modo webhook de prueba (query params)
    payment_id = request.args.get("data.id")
    if payment_id:
        last_payment = {"id": payment_id, "status": "approved"}  # simulamos aprobado
        print("📩 Webhook de prueba recibido, payment_id:", payment_id, flush=True)
        return jsonify({"status": "ok"}), 200

    return jsonify({"status": "no data"}), 400

@app.route("/last_payment")
def get_last_payment():
    return jsonify(last_payment)
