from flask import Flask, render_template, request
import serial
import pyttsx3

# Initialize Flask app
app = Flask(__name__)

# Initialize serial communication with Arduino
arduino = serial.Serial('COM5', 9600, timeout=1)  # Replace 'COM5' with your Arduino's port

# Initialize text-to-speech
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('voice', 'english')  # Set voice

# Function to send commands to Arduino
def send_command(command):
    arduino.write((command + '\n').encode())
    response = arduino.readline().decode().strip()
    print(f"Arduino Response: {response}")
    engine.say(f"Arduino says {response}")
    engine.runAndWait()
    return response

# Web routes
@app.route('/')
def home():
    return render_template('index.html')  # Main interface

@app.route('/control', methods=['POST'])
def control_locker():
    action = request.form.get('action')  # Get action from form
    if action == 'Unlock':
        engine.say("Unlocking the locker")
        engine.runAndWait()
        response = send_command("UNLOCK")
        return f"Locker Unlocked: {response}"
    elif action == 'Lock':
        engine.say("Locking the locker")
        engine.runAndWait()
        response = send_command("LOCK")
        return f"Locker Locked: {response}"
    else:
        return "Invalid Action"

if __name__ == "__main__":
    app.run(debug=True)
