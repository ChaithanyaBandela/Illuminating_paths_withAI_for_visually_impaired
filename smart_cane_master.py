import cv2
import threading
import pyttsx3
from collections import Counter
from ultralytics import YOLO

MODEL_PATH = "yolo11n.pt" 


def speak(text):
    print(f"🔊 AUDIO: {text}")
    def run_speech():
        engine = pyttsx3.init()
        engine.setProperty('rate', 160) 
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=run_speech, daemon=True).start()


print("Loading AI Brain...")
model = YOLO(MODEL_PATH)
cap = cv2.VideoCapture(0)

def format_word(count, word):
    if count == 1: return f"1 {word}"
    if word.endswith('s'): return f"{count} {word}"
    return f"{count} {word}s"

speak("Smart Cane Online")

# Memory system so it only shouts once!
last_seen_objects = ""

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break

    # 1. Run AI Detection
    results = model(frame, stream=True, conf=0.45)
    current_labels = []
    
    for r in results:
        for box in r.boxes:
            lbl = model.names[int(box.cls[0])].lower()
            current_labels.append(lbl)
            
    # 2. Count the objects
    counts = Counter(current_labels)
    announcement_parts = [format_word(count, obj) for obj, count in counts.items()]
    current_state_str = ", ".join(announcement_parts)

    # 3. VISION ANNOUNCEMENT LOGIC
    if current_state_str != "":
        # Only speak if what it sees right now is DIFFERENT from the last thing it announced
        if current_state_str != last_seen_objects:
            speak(f"{current_state_str} ahead")
            last_seen_objects = current_state_str  # Update memory so it shuts up
    else:
        # If the screen is completely empty, clear the memory
        last_seen_objects = ""

    
    if current_state_str:
        cv2.putText(frame, current_state_str, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    cv2.imshow("Laptop AI Vision Test", frame)
    
    # Press 'q' to quit
 
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()