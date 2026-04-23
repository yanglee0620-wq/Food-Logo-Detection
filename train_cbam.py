import os
from ultralytics import YOLO

if __name__ == '__main__':
    # 1. 指定你的数据集配置文件路径
    yaml_path = r"E:\Logo detection\dataset\food_logo.yaml"

    print("🛠️ 正在构建搭载 CBAM 注意力机制的 YOLOv8 网络...")

    # 2. 【核心变化】：先加载你刚刚写好的专属网络架构文件！
    model = YOLO(r"E:\Logo detection\yolov8n-cbam.yaml")

    # 3. 【加速魔法】：把官方的 yolov8n.pt 权重“灌”进来。
    # YOLO 库非常聪明，它会把能匹配上的层（原来就有的层）的权重复制过来，
    # 而你新加的 CBAM 层则会自动随机初始化，等待训练。这比完全从头训练快无数倍！
    model.load("yolov8n.pt")

    print("🧠 V2 模型准备就绪！开始炼丹...")

    # 4. 启动训练！
    model.train(
        data=yaml_path,
        epochs=150,
        imgsz=640,
        device=0,
        workers=2,  # 【修复1】降低多线程数量，缓解 Windows 内存压力
        batch=8,  # 【修复2】RTX 3050 只有 4G 显存，把 batch 从 16 降到 8，防止 OOM
        amp=False,  # 【核心修复】强行关闭 AMP 混合精度训练，直接绕过导致闪退的元凶！
        name="train_cbam_v2"
    )