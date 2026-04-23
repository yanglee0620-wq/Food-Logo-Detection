import streamlit as st
import cv2
from PIL import Image
import numpy as np
from ultralytics import YOLO

# 1. 页面基本设置
st.set_page_config(page_title="食品 Logo 检测系统", page_icon="🍔", layout="wide")
st.title("🍔 食品功能性 Logo 实时检测系统 (V4 终极版)")
st.write("支持上传静态图片或开启电脑摄像头，实时追踪并捕捉食品包装上的微小标志。")

# 2. 侧边栏：模型与参数配置
st.sidebar.header("⚙️ 部署设置")

# ⚠️ 重点：这里默认使用了你刚刚导出的速度极快的 ONNX 模型！
model_path = st.sidebar.text_input("模型权重路径", r"E:\Logo detection\runs\detect\train_final_v4\weights\best.onnx")
conf_threshold = st.sidebar.slider("置信度阈值 (动态调节精度与漏检)", min_value=0.05, max_value=1.0, value=0.1,
                                   step=0.05)


@st.cache_resource
def load_model(path):
    return YOLO(path)


try:
    model = load_model(model_path)
    st.sidebar.success("✅ ONNX 极速推理引擎启动成功！")
except Exception as e:
    st.sidebar.error(f"❌ 模型加载失败，请检查路径是否正确。\n{e}")
    st.stop()

# 3. 核心功能切换区 (分栏布局)
tab1, tab2 = st.tabs(["📸 摄像头实时检测 (答辩演示)", "📁 静态图片上传分析"])

# ================= 标签页 1: 实时摄像头检测 =================
with tab1:
    st.markdown("### 🔴 实时视频流追踪")
    st.write("请准备好带有清真、有机或可回收标志的食品包装（或用手机显示图片对着屏幕），然后点击下方开关。")

    run_camera = st.checkbox("🚀 点击此处：开启 / 关闭 摄像头")

    # 占位符，用来高速刷新画面
    FRAME_WINDOW = st.image([])

    if run_camera:
        # 打开默认摄像头 (如果是笔记本自带摄像头通常是 0)
        cap = cv2.VideoCapture(0)

        while run_camera:
            ret, frame = cap.read()
            if not ret:
                st.error("无法获取摄像头画面，请检查设备连接或权限。")
                break

            # 使用 ONNX 模型进行极速预测
            results = model.predict(frame, conf=conf_threshold, verbose=False)
            res_plotted = results[0].plot()

            # 将 BGR (OpenCV格式) 转为 RGB (网页显示格式)
            res_rgb = cv2.cvtColor(res_plotted, cv2.COLOR_BGR2RGB)

            # 实时更新网页画面
            FRAME_WINDOW.image(res_rgb)

        cap.release()
    else:
        st.info("💡 摄像头已关闭。在答辩时开启此功能，并拿着零食在镜头前晃动，可展现极速追踪效果。")

# ================= 标签页 2: 原有的静态图片检测 =================
with tab2:
    uploaded_file = st.file_uploader("请选择一张图片上传...", type=["jpg", "jpeg", "png", "webp"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        img_array = np.array(image)
        if len(img_array.shape) == 3 and img_array.shape[-1] == 4:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)

        col1, col2 = st.columns(2)
        with col1:
            st.image(image, caption="原始输入图像", use_column_width=True)

        with col2:
            with st.spinner("正在进行多尺度特征推理..."):
                results = model.predict(source=img_array, conf=conf_threshold, verbose=False)
                res = results[0]
                res_rgb = cv2.cvtColor(res.plot(), cv2.COLOR_BGR2RGB)
                st.image(res_rgb, caption=f"AI 检测结果 (耗时: {res.speed['inference']:.1f}ms)", use_column_width=True)

        # 详细数据
        boxes = res.boxes
        if len(boxes) > 0:
            st.success(f"🎉 成功锁定 {len(boxes)} 个微小 Logo！")
            for i, box in enumerate(boxes):
                cls_id = int(box.cls[0].item())
                st.write(f"- **{model.names[cls_id]}** | 置信度: {box.conf[0].item() * 100:.1f}%")
        else:
            st.warning("⚠️ 未检测到目标，请尝试在左侧调低置信度阈值。")