from flask import Flask, request, jsonify

app = Flask(__name__)

# Último pago aprobado
last_payment = {}

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    # Solo aceptamos pagos aprobados
    if data.get("type") == "payment":
        payment = data.get("data", {})
        status = payment.get("status")
        last_payment["status"] = status
        last_payment["id"] = payment.get("id")
    return jsonify({"ok": True}), 200

@app.route("/last_payment", methods=["GET"])
def get_last_payment():
    return jsonify(last_payment)
