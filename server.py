from flask import Flask, render_template, request

app = Flask(__name__)

# --- CONFIGURATION ---
# The correct password is one of the top 10 most common passwords.
# Top 10 list usually includes: 123456, password, 123456789, 12345678, 12345, 111111, 1234567, sunshine, qwerty, iloveyou
SECRET_PASSWORD = "password" 
LED_PIN = 18  # BCM pin 18 (physical pin 12)

# --- GPIO SETUP ---
# We wrap this in a try-except block so the code runs on non-Raspberry Pi systems
try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.output(LED_PIN, GPIO.LOW) # Ensure LED is off initially
    GPIO_AVAILABLE = True
    print(f"GPIO initialized. LED on PIN {LED_PIN}")
except (ImportError, RuntimeError):
    GPIO_AVAILABLE = False
    print("RPi.GPIO not found or not running on a Pi. Running in SIMULATION mode.")

# --- ROUTES ---
@app.route('/', methods=['GET', 'POST'])
def home():
    message = None
    status = ""
    is_success = False

    if request.method == 'POST':
        password = request.form.get('password')
        
        if password == SECRET_PASSWORD:
            message = "Access Granted! LED turned ON."
            status = "success"
            is_success = True
            if GPIO_AVAILABLE:
                GPIO.output(LED_PIN, GPIO.HIGH)
            else:
                print(f"[SIMULATION] LED ON (Pin {LED_PIN})")
        else:
            message = "Access Denied! Incorrect Password."
            status = "error"
            if GPIO_AVAILABLE:
                GPIO.output(LED_PIN, GPIO.LOW) # Ensure it stays off
            else:
                print(f"[SIMULATION] LED OFF (Pin {LED_PIN})")

    return render_template('index.html', message=message, status=status, success=is_success)

@app.route('/reset')
def reset():
    # Helper route to turn off the LED effortlessly
    if GPIO_AVAILABLE:
        GPIO.output(LED_PIN, GPIO.LOW)
    else:
        print(f"[SIMULATION] LED OFF (Pin {LED_PIN})")
    return "LED Reset"

if __name__ == '__main__':
    try:
        # Host 0.0.0.0 makes it accessible on the local network
        print("Starting server on port 5000...")
        app.run(host='0.0.0.0', port=5000, debug=False)
    except Exception as e:
        print(f"Error starting server: {e}")
    finally:
        if GPIO_AVAILABLE:
            GPIO.cleanup()
