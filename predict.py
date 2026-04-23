from ultralytics import YOLO

# 1. 加载你刚刚训练出来的“最强大脑”
model = YOLO(r"E:\Logo detection\runs\detect\train3\weights\best.pt")

# 2. 对新图片进行预测，并保存画好框的结果图
# conf=0.5 表示只显示模型有 50% 以上把握的预测结果
results = model.predict(source="test.jpg", conf=0.5, save=True)

print("预测完成！快去 runs/detect/predict 文件夹里看画好框的图片吧！")