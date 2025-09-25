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

    # Primero intentamos leer JSON
    data = request.get_json(silent=True)

    if not data:
        # Si no hay JSON, revisamos query params (modo prueba)
        payment_id = request.args.get("data.id")
        if payment_id:
            last_payment = {"id": payment_id, "status": "approved"}  # simulamos aprobado
            print("📩 Webhook de prueba recibido, payment_id:", payment_id, flush=True)
            return jsonify({"status": "ok"}), 200
        else:
            return jsonify({"status": "no data"}), 400

    # Si hay JSON normal (pagos reales)
    if "data" in data and "id" in data["data"]:
        payment_id = data["data"]["id"]
        # Aquí llamás a la API de MercadoPago para confirmar
        # ...
    return jsonify({"status": "ok"}), 200


@app.route("/last_payment")
def get_last_payment():
    return jsonify(last_payment)
