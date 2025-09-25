from flask import Flask, request, jsonify

app = Flask(__name__)

# Estado simple en memoria (en producción usar base de datos)
ultimo_pago_aprobado = None

@app.route("/webhook", methods=["POST"])
def webhook():
    global ultimo_pago_aprobado
    data = request.json

    if data.get("type") == "payment" and data["data"]["status"] == "approved":
        ultimo_pago_aprobado = data["data"]["id"]
        print("Pago aprobado:", ultimo_pago_aprobado)

    return jsonify({"status": "ok"})

@app.route("/estado_pago", methods=["GET"])
def estado_pago():
    """Endpoint para que Tkinter consulte si hay pago aprobado"""
    global ultimo_pago_aprobado
    if ultimo_pago_aprobado:
        pago = ultimo_pago_aprobado
        ultimo_pago_aprobado = None  # limpiar después de notificar
        return jsonify({"aprobado": True, "id_pago": pago})
    return jsonify({"aprobado": False})

if __name__ == "__main__":
    app.run()
