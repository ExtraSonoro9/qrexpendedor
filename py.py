# servidor_simulado.py
from flask import Flask, request
import threading

app = Flask(__name__)

# Función que simula activar motor en tu app Python
def activar_motor_callback():
    print("💰 Pago aprobado → Activando motor (simulado)")

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("Webhook recibido:", data)

    if data.get("type") == "payment" and data["data"]["status"] == "approved":
        # Llamamos a la función de la app
        activar_motor_callback()
    return "OK", 200

def start_server():
    app.run(host="0.0.0.0", port=5000)

# Correr el servidor en un hilo separado para que no bloquee Tkinterfgfgdhgdg



