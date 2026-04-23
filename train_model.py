import os
import shutil
import random
import yaml
from ultralytics import YOLO

# 1. 设定路径
base_dir = r"E:\Logo detection\dataset"
images_final = os.path.join(base_dir, "images_final")
labels_final = os.path.join(base_dir, "labels_final")

# YOLO 标准文件夹结构
train_img = os.path.join(base_dir, "images", "train")
val_img = os.path.join(base_dir, "images", "val")
train_lbl = os.path.join(base_dir, "labels", "train")
val_lbl = os.path.join(base_dir, "labels", "val")

# 创建这些文件夹
for d in [train_img, val_img, train_lbl, val_lbl]:
    os.makedirs(d, exist_ok=True)

# 2. 自动划分数据集 (80%用来训练，20%用来做期末考试)
all_imgs = [f for f in os.listdir(images_final) if f.endswith('.jpg')]
random.shuffle(all_imgs)  # 打乱顺序

split_idx = int(len(all_imgs) * 0.8)
train_imgs = all_imgs[:split_idx]
val_imgs = all_imgs[split_idx:]


def move_files(file_list, dest_img_dir, dest_lbl_dir):
    for img_name in file_list:
        base = os.path.splitext(img_name)[0]
        txt_name = base + ".txt"

        # 复制图片和标签到 YOLO 专属目录
        shutil.copy(os.path.join(images_final, img_name), os.path.join(dest_img_dir, img_name))
        if os.path.exists(os.path.join(labels_final, txt_name)):
            shutil.copy(os.path.join(labels_final, txt_name), os.path.join(dest_lbl_dir, txt_name))


print(f"正在划分为训练集({len(train_imgs)}张) 和 验证集({len(val_imgs)}张)...")
move_files(train_imgs, train_img, train_lbl)
move_files(val_imgs, val_img, val_lbl)

# 3. 自动生成 YOLO 的“户口本”文件 (data.yaml)
yaml_path = os.path.join(base_dir, "food_logo.yaml")
yaml_content = {
    'path': base_dir,
    'train': 'images/train',
    'val': 'images/val',
    'names': {0: 'Halal', 1: 'Organic', 2: 'Recyclable'}
}
with open(yaml_path, 'w') as f:
    yaml.dump(yaml_content, f, sort_keys=False)

# ... 上面的代码都不用动 ...

print("🎉 数据集准备就绪！开始炼丹（训练）...")

# ✅ 解决 Windows 报错的终极保险栓
if __name__ == '__main__':
    # YOLO神龙必须在保险栓内召唤
    model = YOLO("yolov8n.pt")

    # 💡 额外优化：Windows 下如果你觉得电脑特别卡，可以把 workers 设置为 4 或 2
    model.train(data=yaml_path, epochs=50, imgsz=640, device=0, workers=4)