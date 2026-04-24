import cv2
from ultralytics import YOLO
import time
import win32com.client
from collections import Counter

# 1. Setup AI
MODEL_PATH = r"C:\Users\Eakan\OneDrive\Desktop\blindv2\runs\detect\blind_cane_v2\weights\best.pt"
model = YOLO(MODEL_PATH)

# 2. Setup DIRECT Windows Audio
speaker = win32com.client.Dispatch("SAPI.SpVoice")

def speak(text):
    print(f"🔊 SHOUTING: {text}")
    speaker.Speak(text, 1) # '1' keeps it running smoothly in the background


speak("Smart counting online") 

cap = cv2.VideoCapture(0)
last_state_str = ""
last_shout = 0

# Helper function to make words plural (so it doesn't say "2 human")
def format_word(count, word):
    if count == 1:
        return f"1 {word}"
    if word.endswith('s'): # E.g., if it's already "stairs"
        return f"{count} {word}"
    return f"{count} {word}s"

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break

    # Run detection (Using 0.45 to keep the boxes stable)
    results = model(frame, stream=True, conf=0.45)
    
    current_labels = []
    
    for r in results:
        for box in r.boxes:
            lbl = model.names[int(box.cls[0])].lower()
            current_labels.append(lbl)
            
            # Draw the box 
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, lbl, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
    
    # 1. Count what is on the screen right now
    # counts will become: {'human': 2, 'chair': 1}
    counts = Counter(current_labels)
    
    # 2. Build the sentence
    announcement_parts = []
    for obj, count in counts.items():
        announcement_parts.append(format_word(count, obj))
    
    # Example: "2 humans, 1 chair"
    current_state_str = ", ".join(announcement_parts)

    # 3. Compare it to the last thing we shouted
    if current_state_str != last_state_str:
        if current_state_str != "": 
            # The scene changed and there are objects! 
            # Wait 2 seconds between shouts so it doesn't stutter if boxes flicker
            if time.time() - last_shout > 2:
                speak(f"{current_state_str} ahead")
                last_state_str = current_state_str # Save this to memory
                last_shout = time.time()
        else:
            # Everything left the screen. Reset memory silently so it's ready for the next object.
            last_state_str = ""

    cv2.imshow("Smart Counting Audio", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()