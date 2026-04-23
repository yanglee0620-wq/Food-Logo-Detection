import os
import cv2

# 你存放图片的根目录
base_dir = "E:\\Logo detection\\raw_images_baidu"  # 如果你用的必应，改成 "raw_images"

deleted_count = 0

# 遍历所有类别文件夹
for category in os.listdir(base_dir):
    folder_path = os.path.join(base_dir, category)
    if not os.path.isdir(folder_path):
        continue

    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)

        # 1. 删除太小的文件 (小于 15KB 通常是废图或清晰度极低的缩略图)
        if os.path.getsize(filepath) < 15 * 1024:
            os.remove(filepath)
            print(f"删除过小文件: {filename}")
            deleted_count += 1
            continue

        # 2. 删除 OpenCV 无法读取的损坏图片
        try:
            img = cv2.imread(filepath)
            if img is None:
                os.remove(filepath)
                print(f"删除损坏文件: {filename}")
                deleted_count += 1
        except Exception as e:
            os.remove(filepath)
            print(f"删除异常文件: {filename}")
            deleted_count += 1

print(f"🎉 自动清理完成！共帮你删除了 {deleted_count} 张无效图片。")