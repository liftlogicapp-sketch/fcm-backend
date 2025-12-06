import os, json
from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, messaging

app = Flask(__name__)

# Load service account JSON from environment variable
service_account_json = os.getenv("SERVICE_ACCOUNT")
cred = credentials.Certificate(json.loads(service_account_json))
firebase_admin.initialize_app(cred)

@app.route("/health")
def health():
    return jsonify({"ok": True})

@app.route("/send-notification", methods=["POST"])
def send_notification():
    data = request.json
    topic = data.get("topic")
    title = data.get("title")
    body = data.get("body")
    extra = data.get("data", {})

    if not topic or not title or not body:
        return jsonify({"error": "topic, title, body required"}), 400

    message = messaging.Message(
        notification=messaging.Notification(title=title, body=body),
        data=extra,
        topic=topic,
    )

    try:
        response = messaging.send(message)
        return jsonify({"success": True, "id": response}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
