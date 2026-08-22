import threading
from flask import Flask, request, jsonify
from tasks import process_print_job

app = Flask(__name__)

ATTENDEES_DB = {
    "ATT001": {"name": "Alice Johnson", "status": "NOT_CHECKED_IN", "badge_printed": False},
    "ATT002": {"name": "Bob Smith", "status": "NOT_CHECKED_IN", "badge_printed": False},
    "ATT003": {"name": "Charlie Brown", "status": "NOT_CHECKED_IN", "badge_printed": False}
}

@app.route('/scan', methods=['POST'])
def scan_attendee():
    data = request.json or {}
    attendee_id = data.get('attendee_id')

    if attendee_id not in ATTENDEES_DB:
        return jsonify({"error": "Attendee not found"}), 404

    attendee = ATTENDEES_DB[attendee_id]

    # Duplicate Scan Protection (Pivot Requirement)
    if attendee['status'] in ['PRINT_PENDING', 'CHECKED_IN']:
        return jsonify({
            "error": "DUPLICATE_SCAN",
            "message": f"Attendee {attendee_id} is already in state: {attendee['status']}"
        }), 400

    # Step A: Update status to pending immediately
    attendee['status'] = 'PRINT_PENDING'

    # Step B: Spawn background thread (Replaces Redis Queue)
    webhook_callback_url = 'http://127.0.0.1:5000/webhook/print-completed'
    thread = threading.Thread(target=process_print_job, args=(attendee_id, webhook_callback_url))
    thread.start()

    # Step C: Return immediate response to UI
    return jsonify({
        "status": "PRINT_PENDING",
        "attendee_id": attendee_id,
        "message": "Print job queued. UI showing pending state."
    }), 202

@app.route('/webhook/print-completed', methods=['POST'])
def print_completed_webhook():
    data = request.json or {}
    attendee_id = data.get('attendee_id')
    job_status = data.get('status')

    if attendee_id in ATTENDEES_DB and job_status == "SUCCESS":
        ATTENDEES_DB[attendee_id]['status'] = 'CHECKED_IN'
        ATTENDEES_DB[attendee_id]['badge_printed'] = True
        
        print(f"[WEBHOOK RECEIVER] Attendee {attendee_id} status updated to CHECKED_IN")
        return jsonify({"status": "SUCCESS", "message": "Record finalized"}), 200

    return jsonify({"error": "Invalid webhook payload"}), 400

@app.route('/attendee/<attendee_id>', methods=['GET'])
def get_attendee(attendee_id):
    attendee = ATTENDEES_DB.get(attendee_id)
    if not attendee:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"attendee_id": attendee_id, "data": attendee}), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)
   