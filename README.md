# Raspberry Pi Web Server with Brute Force Vulnerability

This project implements a simple Flask web server designed to demonstrate a brute-force vulnerability. It includes a login page that accepts a password. If the correct password is entered, an LED connected to the Raspberry Pi is turned on.

## Files

*   `server.py`: The main Flask application. Handles the web server, password checking, and GPIO control.
*   `templates/index.html`: The HTML template for the login page.
*   `requirements.txt`: List of Python dependencies.
*   `attack.py`: A demonstration script that bruteforces the login page using a list of common passwords.

## Setup on Raspberry Pi

1.  **Install Dependencies:**
    Open a terminal on your Raspberry Pi and run:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Connect the LED:**
    *   Connect the **positive (simpler)** leg of the LED to **GPIO Pin 18 (Physical Pin 12)**.
    *   Connect the **negative (shorter)** leg of the LED to a **GND (Ground)** pin (e.g., Physical Pin 6) via a resistor (220Ω or 330Ω is recommended).

3.  **Run the Server:**
    ```bash
    python server.py
    ```
    The server will start on port 5000. You can access it from a browser at `http://<your-pi-ip>:5000`.

## Testing the Vulnerability

1.  Keep the server running.
2.  Open another terminal window (or use your computer if connected to the same network).
3.  Run the attack script:
    ```bash
    python attack.py
    ```
    This script will try passwords from a top-10 list until it finds the correct one ("password") and turns on the LED.

## Notes

*   **Simulation Mode:** If you run `server.py` on a computer without GPIO (like Windows), it will run in "Simulation Mode" and just print messages to the console instead of controlling an actual LED.
*   **Safety:** This is a vulnerable application. Do not run this on a public network securely.
