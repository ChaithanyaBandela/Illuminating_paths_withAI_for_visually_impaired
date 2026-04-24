from ultralytics import YOLO

# 1. Start with the tiny, fast YOLOv11 model
model = YOLO("yolo11n.pt") 

# 2. Train on the new 2.7k image dataset
print("🚀 Starting High-Data Training on Ryzen CPU...")
results = model.train(
    data="obstacle detection.v1i.yolov8/data.yaml", 
    epochs=30,         # 30 epochs is enough for a strong first test
    imgsz=416,         # Reduced size makes CPU training much faster
    batch=8,           # Prevents your laptop from slowing down
    device="cpu",      
    name="blind_cane_v2" 
)

print("✅ Training complete! New brain saved in runs/detect/blind_cane_v2")