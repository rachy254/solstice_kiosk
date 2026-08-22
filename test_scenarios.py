import time
import requests

BASE_URL = "http://127.0.0.1:5000"

def run_tests():
    print("\n--- TEST 1: Standard Asynchronous Flow (ATT001) ---")
    res1 = requests.post(f"{BASE_URL}/scan", json={"attendee_id": "ATT001"})
    print("Initial Scan Response (Immediate):", res1.status_code, res1.json())

    print("\n--- TEST 2: Duplicate Scan Protection (ATT001 - Immediate Rescan) ---")
    res2 = requests.post(f"{BASE_URL}/scan", json={"attendee_id": "ATT001"})
    print("Duplicate Scan Response:", res2.status_code, res2.json())

    print("\nWaiting 4 seconds for printer worker to finish processing...")
    time.sleep(4)

    print("\n--- CHECK STATUS AFTER WEBHOOK CALLBACK ---")
    check1 = requests.get(f"{BASE_URL}/attendee/ATT001")
    print("Attendee ATT001 Database Record:", check1.json())

    print("\n--- TEST 3: Duplicate Scan Protection After Checked In (ATT001) ---")
    res3 = requests.post(f"{BASE_URL}/scan", json={"attendee_id": "ATT001"})
    print("Post-Check-In Duplicate Scan Response:", res3.status_code, res3.json())

if __name__ == "__main__":
    run_tests()