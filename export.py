from ultralytics import YOLO

# Load your custom brain
model = YOLO(r"runs\detect\blind_cane_v2\weights\best.pt")

# Convert it to the high-speed Raspberry Pi format
model.export(format="ncnn")