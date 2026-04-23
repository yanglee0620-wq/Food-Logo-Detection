import os
from ultralytics import YOLO

if __name__ == '__main__':
    yaml_path = r"E:\Logo detection\dataset\food_logo.yaml"
    print("🚀 正在构建 终极版：CBAM + 4头小目标检测 网络...")
    model = YOLO(r"E:\Logo detection\yolov8n-cbam-p2.yaml")
    model.load("yolov8n.pt")

    print("🔥 V3 终极模型准备就绪！开始炼丹...")
    model.train(
        data=yaml_path,
        epochs=150,
        imgsz=640,
        device=0,
        workers=2,
        batch=8,
        amp=False,
        name="train_final_v5_clean"  # 换个新名字保存这次干净的训练结果
    )