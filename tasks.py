import time
import requests

def process_print_job(attendee_id, webhook_url):
    """Simulates hardware printing time and triggers an async webhook callback."""
    print(f"[PRINTER] Starting badge print job for Attendee: {attendee_id}...")
    
    # Simulate hardware print delay (3 seconds)
    time.sleep(3)
    
    print(f"[PRINTER] Print completed for {attendee_id}. Triggering webhook callback...")
    
    payload = {
        "attendee_id": attendee_id,
        "status": "SUCCESS",
        "message": "Badge printed successfully"
    }
    
    try:
        response = requests.post(webhook_url, json=payload)
        print(f"[PRINTER] Webhook acknowledged with HTTP {response.status_code}")
    except Exception as e:
        print(f"[PRINTER ERROR] Failed to send webhook: {e}")