from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("Webhook recibido:", data)

    # Solo como ejemplo: confirmar que es un pago aprobado
    if data and "type" in data and data["type"] == "payment":
        print("🔔 Notificación de pago recibida")
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)  # Render usa un puerto dinámico, mejor usar gunicorn

