import cv2
import pytesseract
import os
import time
import RPi.GPIO as GPIO
from gtts import gTTS
from picamera2 import Picamera2

# GPIO setup
BUTTON_PIN = 17  # Define the GPIO pin for button input
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize camera
camera = Picamera2()
camera.preview_configuration.main.size = (640, 480)
camera.preview_configuration.main.format = "RGB888"
camera.configure("preview")
camera.start()

def capture_image():
    """Captures an image using PiCamera and saves it."""
    image_path = "captured_text.jpg"
    camera.capture_file(image_path)
    return image_path

def extract_text(image_path):
    """Extracts text from the captured image using Tesseract OCR."""
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text.strip()

def text_to_speech(text):
    """Converts extracted text to speech using gTTS."""
    if text:
        print("Extracted Text:", text)
        tts = gTTS(text, lang='en')
        tts.save("output.mp3")
        os.system("mpg321 output.mp3")  # Play the audio output
    else:
        print("No text detected.")

def button_callback(channel):
    """Handles button press to capture and read text."""
    print("Button Pressed! Capturing image...")
    image_path = capture_image()
    text = extract_text(image_path)
    text_to_speech(text)

# Set up event detection for button press
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=300)

print("Smart Reader is running. Press the button to capture text.")
try:
    while True:
        time.sleep(0.1)  # Keep the script running
except KeyboardInterrupt:
    print("Exiting...")
    GPIO.cleanup()
