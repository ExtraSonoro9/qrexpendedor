from flask import Flask, request

app = Flask(__name__)
_motor_callback = None

def set_motor_callback(callback):
    global _motor_callback
    _motor_callback = callback

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("Webhook recibido:", data)
    if data.get("type") == "payment" and data["data"]["status"] == "approved":
        if _motor_callback:
            _motor_callback()
    return "OK", 200

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)



