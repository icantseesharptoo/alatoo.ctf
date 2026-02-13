import os
import random
import time
from flask import Flask, render_template, request, session, redirect, url_for, jsonify

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

# --- CONFIGURATION ---
# Task 1: Brute Force
COMMON_PASSWORDS = [
    "123456", "password", "123456789", "12345678", "12345", 
    "111111", "1234567", "sunshine", "qwerty", "iloveyou"
]
CURRENT_TASK1_PASSWORD = None  # Will be set on startup

# Task 2: DDoS
DDOS_TARGET = 100

# Task 3: OSINT
OSINT_USER = "andrei"
OSINT_PASS = "bary1985" # Example: Dog 'Bary', Year 1985

# GPIO Configuration
LED_PINS = {
    'task1': 18,  # Pin 12
    'task2': 23,  # Pin 16
    'task3': 24   # Pin 18
}
RESET_PIN = 21   # Pin 40 (Connect Button to Pin 40 and GND)

# --- GPIO SETUP ---
def perform_reset(channel=None):
    """Callback function for Physical Reset Button"""
    print("\n[HARDWARE] Reset Button Pressed!")
    
    # 1. Reset Global State
    global CURRENT_TASK1_PASSWORD
    CURRENT_TASK1_PASSWORD = random.choice(COMMON_PASSWORDS)
    print(f"New Task 1 Password: {CURRENT_TASK1_PASSWORD}")

    # 2. Invalidate all existing sessions by rotating the Secret Key
    app.secret_key = os.urandom(24)
    print("Session Key Rotated (All users logged out)")
    
    # 3. Turn ALL LEDs ON
    if GPIO_AVAILABLE:
        for pin in LED_PINS.values():
            GPIO.output(pin, GPIO.HIGH)
    else:
        print("[SIMULATION] All LEDs reset to ON")

try:
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    
    # Setup LEDs
    for pin in LED_PINS.values():
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)
        
    GPIO.setup(RESET_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    GPIO.remove_event_detect(RESET_PIN)  # Clean up any previous event detection
    GPIO.add_event_detect(RESET_PIN, GPIO.FALLING, callback=perform_reset, bouncetime=500)
    
    GPIO_AVAILABLE = True
    print(f"GPIO initialized.")
    print(f"- LEDs on pins: {list(LED_PINS.values())}")
    print(f"- Reset Button on pin: {RESET_PIN} (Connect to GND)")
    
except (ImportError, RuntimeError) as e:
    GPIO_AVAILABLE = False
    print(f"RPi.GPIO not found. Running in SIMULATION mode. ({e})")

# Wrapper for consistency (can be called by logic or hardware)
def control_led(task_name, state):
    """Control LED. State: True for ON, False for OFF."""
    pin = LED_PINS.get(task_name)
    if not pin: return
    
    # In this logic, ON means "Task Active" (LED ON/HIGH)
    # Task Solved means "Task Inactive" (LED OFF/LOW)
    gpio_state = GPIO.HIGH if state else GPIO.LOW
    
    if GPIO_AVAILABLE:
        GPIO.output(pin, gpio_state)
    else:
        status = "ON" if state else "OFF"
        print(f"[SIMULATION] LED {task_name} (Pin {pin}) turned {status}")

# --- ROUTES ---

@app.route('/', methods=['GET', 'POST'])
def index():
    # Task 1: Brute Force Login
    error = None
    if request.method == 'POST':
        password = request.form.get('password')
        if password == CURRENT_TASK1_PASSWORD:
            session['task1_solved'] = True
            control_led('task1', False) # Turn Led 1 OFF
            return redirect(url_for('task2'))
        else:
            error = "Access Denied! Incorrect Password."
    
    return render_template('index.html', message=error, status="error" if error else "")

@app.route('/task2')
def task2():
    if not session.get('task1_solved'):
        return redirect(url_for('index'))
    
    count = session.get('ddos_count', 0)
    return render_template('task2.html', count=count)

@app.route('/api/click', methods=['POST'])
def api_click():
    if not session.get('task1_solved'):
        return jsonify({'error': 'Unauthorized'}), 403
        
    count = session.get('ddos_count', 0) + 1
    session['ddos_count'] = count
    
    completed = False
    if count >= DDOS_TARGET:
        session['task2_solved'] = True
        control_led('task2', False) # Turn Led 2 OFF
        completed = True
        
    return jsonify({'count': count, 'completed': completed})

@app.route('/task3', methods=['GET', 'POST'])
def task3():
    if not session.get('task2_solved'):
        return redirect(url_for('task2'))
        
    error = None
    if request.method == 'POST':
        username = request.form.get('username').lower()
        password = request.form.get('password').lower()
        
        if username == OSINT_USER and password == OSINT_PASS:
            session['task3_solved'] = True
            control_led('task3', False) # Turn Led 3 OFF
            return redirect(url_for('complete'))
        else:
            error = "Invalid Credentials"
            
    return render_template('task3.html', error=error)

@app.route('/complete')
def complete():
    if not session.get('task3_solved'):
        return redirect(url_for('task3'))
    return render_template('complete.html')

@app.route('/reset')
def reset():
    # Helper to reset state via Web (triggers same logic as hardware button)
    perform_reset()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Initialize Random Password
    CURRENT_TASK1_PASSWORD = random.choice(COMMON_PASSWORDS)
    print(f"--- SERVER STARTED ---")
    print(f"Task 1 Password: {CURRENT_TASK1_PASSWORD}")
    print(f"Task 3 Credentials: {OSINT_USER} / {OSINT_PASS}")
    
    try:
        # Host 0.0.0.0 makes it accessible on the local network
        app.run(host='0.0.0.0', port=5000, debug=False)
    finally:
        if GPIO_AVAILABLE:
            GPIO.cleanup()
