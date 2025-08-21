import os
import glob
import psycopg2
import pandas as pd
from ultralytics import YOLO

# -------------------------
# Config
# -------------------------
IMAGE_FOLDERS = [
    "F:/Intelligent_Ethiopian_Medical_Business_peplines-/data/raw/telegram_messages/data_lake/Chemed123",
    "F:/Intelligent_Ethiopian_Medical_Business_peplines-/data/raw/telegram_messages/data_lake/lobelia4cosmetics",
    "F:/Intelligent_Ethiopian_Medical_Business_peplines-/data/raw/telegram_messages/data_lake/tikvahpharma"
]

MODEL_PATH = "yolov8n.pt"  # lightweight pre-trained model
DB_CONFIG = {
    "dbname": "kara_medical_db",
    "user": "postgres",
    "password": "n5090",
    "host": "localhost",
    "port": "5432"
}

# -------------------------
# Database Helper
# -------------------------


def create_table_if_not_exists():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        CREATE SCHEMA IF NOT EXISTS analytics;
        CREATE TABLE IF NOT EXISTS analytics.fct_image_detections (
            detection_id SERIAL PRIMARY KEY,
            image_path TEXT NOT NULL,
            detected_object_class TEXT NOT NULL,
            confidence_score FLOAT NOT NULL,
            detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()


def insert_detections(records):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.executemany("""
        INSERT INTO analytics.fct_image_detections (image_path, detected_object_class, confidence_score)
        VALUES (%s, %s, %s)
    """, records)
    conn.commit()
    cur.close()
    conn.close()

# -------------------------
# Object Detection
# -------------------------


def run_yolo_on_folders():
    model = YOLO(MODEL_PATH)
    all_detections = []

    for folder in IMAGE_FOLDERS:
        for image_path in glob.glob(os.path.join(folder, "*.jpg")):  
            results = model(image_path)  # run YOLO
            for result in results:
                for box in result.boxes:
                    cls = model.names[int(box.cls[0])]
                    conf = float(box.conf[0])
                    all_detections.append((image_path, cls, conf))

    return all_detections

# -------------------------
# Main
# -------------------------


if __name__ == "__main__":
    pass
