from ultralytics import YOLO

# Load a trained model (see Drive folder)
model = YOLO(r"DRIVE_FOLDER\1_trained_models\attempt_2\best.pt")

# Get predictions from YOLO model
predictions = model.predict(r"DRIVE_FOLDER\1_obb_attempt\test\images", save=True, imgsz=1500,
                            conf=0.01, iou=0.5,
                            line_width=2
                            , save_txt=True, save_conf=True,
                            show_conf=True
                            )
