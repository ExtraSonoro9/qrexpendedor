from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

ACCESS_TOKEN = "APP_USR-877458804311630-092416-287a1adc56b6c7e14a1bde943097959a-1081932903"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.args  # Mercado Pago envía info por query params
    payment_id = data.get("data.id")
    order_id = data.get("data.id")
    external_ref = data.get("data.external_reference")
    tipo = data.get("type")

    print("Webhook recibido:", data)

    if tipo == "order" and order_id:
        # Consultar la orden para ver pagos
        url = f"https://api.mercadopago.com/checkout/orders/{order_id}"
        headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
        resp = requests.get(url, headers=headers)
        order = resp.json()

        # Revisar pagos asociados
        payments = order.get("payments", [])
        for p in payments:
            if p.get("status") == "approved":
                print(f"Pago aprobado para la orden {external_ref} ✅")
                break

    elif tipo.startswith("payment") and payment_id:
        # Si recibimos directamente un payment id
        url = f"https://api.mercadopago.com/v1/payments/{payment_id}"
        headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
        resp = requests.get(url, headers=headers)
        payment = resp.json()

        if payment.get("status") == "approved":
            print(f"Pago aprobado para el pago {payment_id} ✅")

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
