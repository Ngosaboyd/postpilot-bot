"""
PostPilot – Automated Social Media Bot
Receives posts via WhatsApp, schedules them, and auto-publishes
to Facebook, WhatsApp Business, and Instagram.

Deploy free on Render: https://render.com
"""

import os
import logging
from flask import Flask, request, jsonify
from bot.whatsapp_receiver import handle_incoming_message
from scheduler.job_runner import start_scheduler
import threading

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger(__name__)

app = Flask(__name__)


# ── WEBHOOK: Receives WhatsApp messages from clients ──────────────────────────

@app.route("/webhook", methods=["GET"])
def verify_webhook():
    """Meta webhook verification handshake."""
    mode  = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == os.environ["WEBHOOK_VERIFY_TOKEN"]:
        log.info("Webhook verified ✓")
        return challenge, 200
    return "Forbidden", 403


@app.route("/webhook", methods=["POST"])
def receive_message():
    """Receive WhatsApp messages — clients send posts here."""
    data = request.get_json(silent=True)
    if data:
        handle_incoming_message(data)
    return jsonify({"status": "ok"}), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "running", "service": "PostPilot"}), 200


# ── START ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Start the background scheduler in a thread
    t = threading.Thread(target=start_scheduler, daemon=True)
    t.start()
    log.info("PostPilot scheduler started ✓")

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
