import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN")  # guardalo como secret en Render
last_payment = {}

@app.route("/")
def home():
    return "Servidor Flask con Webhooks funcionando"

@app.route("/webhook", methods=["POST"])
def webhook():
    global last_payment
    data = request.get_json()

    if data and "data" in data and "id" in data["data"]:
        payment_id = data["data"]["id"]

        # Consultar estado real a la API de MercadoPago
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

@app.route("/last_payment")
def get_last_payment():
    return jsonify(last_payment)
