import os
from ultralytics import YOLO

# ------------------ Paths ------------------ #
BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
dataset_yaml = os.path.join(BASE_DIR, "dataset", "data.yaml")
teacher_weights_dir = os.path.join(BASE_DIR, "models", "teacher")
os.makedirs(teacher_weights_dir, exist_ok=True)

# ------------------ Training Config ------------------ #
# Pretrained YOLOv8 Pose model (n = nano, you can switch to s/m/l/x)
pretrained_model = "yolov8n-pose.pt"

# Training parameters
epochs = 1
batch_size = 4  # Adjust according to your GPU
img_size = 640

# Path to save best model
best_model_path = os.path.join(teacher_weights_dir, "best.pt")

# ------------------ Train ------------------ #


def train_teacher():
    # Load model
    model = YOLO(pretrained_model)

    # Train on custom dataset
    model.train(
        data=dataset_yaml,
        epochs=epochs,
        batch=batch_size,
        imgsz=img_size,
        project=os.path.join(BASE_DIR, "runs", "train_teacher"),
        name="teacher_pose",
        exist_ok=True,  # overwrite existing run
        save=True,
        save_period=1,
        workers=4,  # adjust for your system
    )

    # Save best model to teacher folder
    # Ultralytics automatically saves 'best.pt' in the run folder
    last_run_best = os.path.join(
        BASE_DIR, "runs", "train_teacher", "teacher_pose", "weights", "best.pt")
    if os.path.exists(last_run_best):
        os.replace(last_run_best, best_model_path)
        print(f"✅ Best teacher model saved at {best_model_path}")
    else:
        print("⚠️ Best model not found, check training logs.")


if __name__ == "__main__":
    train_teacher()
