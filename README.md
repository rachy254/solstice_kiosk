# Solstice Events Co. - Asynchronous Kiosk Badge Printing System (The Pivot)

An event-driven, non-blocking check-in kiosk system built for **Solstice Events Co.** to replace deprecated synchronous badge-printing REST endpoints. 

This project implements an **Asynchronous Architecture** utilizing **Python (Flask)**, multi-threaded background workers, and **Webhook Callbacks**.

---

## 🏛️ System Architecture

1. **Client Scan Trigger:** Kiosk staff scans an attendee's QR code via `POST /scan`.
2. **Duplicate Protection Check:** The system verifies the attendee's current state (`NOT_CHECKED_IN`, `PRINT_PENDING`, or `CHECKED_IN`). Duplicate requests are rejected immediately with HTTP 400.
3. **Async Offloading:** Valid requests update the local attendee status to `PRINT_PENDING` and spawn an asynchronous background thread to execute the badge generation job.
4. **Immediate UI Response:** The client receives an instant HTTP 202 (`PRINT_PENDING`) response, keeping the UI thread active and non-blocking.
5. **Background Processing & Webhook Callback:** The background worker simulates hardware badge printing and POSTs a completion payload to the `/webhook/print-completed` endpoint upon completion.
6. **State Finalization:** The webhook receiver updates the database state to `CHECKED_IN` and sets `badge_printed = True`.

---

## 🛠️ Technology Stack

* **Language:** Python 3.x
* **Framework:** Flask
* **Concurrency:** Python `threading` / Asynchronous Background Workers
* **HTTP Client:** Requests

---

## 🚀 Setup & Installation

### 1. Prerequisites
Ensure you have Python 3.x and Git installed on your system.

### 2. Environment Setup
Clone the repository and install the required dependencies:

```bash
git clone [https://github.com/rachy254/solstice_kiosk_pivot.git](https://github.com/rachy254/solstice_kiosk_pivot.git)
cd solstice_kiosk_pivot
pip install flask requests

⚡ Running the Application
 * Launch the Flask Server:
   python app.py

   (The server will start on http://127.0.0.1:5000)
 * Execute Automated Tests:
   Open a separate terminal window and run:
   python test_scenarios.py

🧪 Automated Test Suite
An automated test script (test_scenarios.py) is included to verify all client acceptance criteria.
Test Coverage:
 * Scenario 1: Standard Asynchronous Flow (Instant HTTP 202 response + background webhook execution).
 * Scenario 2: Immediate Duplicate Scan Guard (Blocks re-scans with HTTP 400 while status is PRINT_PENDING).
 * Scenario 3: Post-Check-In Duplicate Guard (Blocks re-scans with HTTP 400 after state becomes CHECKED_IN).
📊 REST API Reference
| Endpoint | Method | Payload | Status Code | Description |
|---|---|---|---|---|
| /scan | POST | {"attendee_id": "ATT001"} | 202 Accepted | Queues badge print job & sets state to PRINT_PENDING. |
| /webhook/print-completed | POST | {"attendee_id": "ATT001", "status": "SUCCESS"} | 200 OK | Webhook callback received from worker; updates state to CHECKED_IN. |
| /attendee/<id> | GET | None | 200 OK | Returns current database state for an attendee. |
