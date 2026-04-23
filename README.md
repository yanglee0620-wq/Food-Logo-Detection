# 食品功能性标识检测系统 (Food Logo Detection)

一个基于深度学习的食品功能性标识检测系统，旨在从复杂的食品包装图像中，高效、精准地识别和定位各种功能性标识（如绿色食品、有机食品、国家地理标志等）。

本项目基于 YOLOv8n 架构构建，并在网络中引入了 CBAM (Convolutional Block Attention Module) 注意力机制，针对小目标标识进行了优化训练，兼顾了高精度与实时推理性能。

## 功能特性

- ✅ 针对食品功能性标识优化的高精度检测
- ✅ 引入 CBAM 注意力机制，提升复杂背景下的特征提取能力
- ✅ 提供数据爬取 (`spider_images.py`)、清洗与格式转换的完整数据流脚本
- ✅ 支持单张图片推理与可视化结果导出
- ✅ 开箱即用的预训练权重

## 环境要求

- Python 3.8+
- PyTorch 1.10+
- Ultralytics (YOLOv8)
- Conda/Miniconda (推荐)

## 安装指南

```bash
# 1. 克隆项目
git clone [https://github.com/你的用户名/Food-Logo-Detection.git](https://github.com/你的用户名/Food-Logo-Detection.git)
cd Food-Logo-Detection

# 2. 使用提供的 yml 文件一键创建并激活 Conda 环境
conda env create -f food_logo_env.yml
conda activate food_logo_env
```

## 快速开始 (Quick Start)

我们提供了训练好的最优权重，你可以直接运行以下代码进行快速推理验证：

```python
from ultralytics import YOLO

# 1. 加载训练好的最优模型权重
model = YOLO('weights/food_logo_best_v5.pt')

# 2. 对单张测试图片进行检测并保存可视化结果
results = model.predict(source='1.test.jpg', save=True)
```

如果你想通过已有的脚本运行：

```bash
# 确保在项目根目录下运行
python predict.py
```

## 模型说明

本项目使用 YOLOv8n-CBAM 模型结构，并在自定义的食品标识数据集上进行了 5 个版本的迭代训练与清洗：

- **模型配置文件**: `yolov8n-cbam.yaml` / `yolov8n-cbam-p2.yaml`
- **最优权重文件**: `weights/food_logo_best_v5.pt`
- **模型大小**: ~6MB (轻量化部署友好)

## 项目结构

Logo_detection/
├── weights/                  # 模型权重存放目录
│   └── food_logo_best_v5.pt  # 最佳检测权重
├── .gitignore                # Git 忽略规则
├── food_logo_env.yml         # Conda 环境配置依赖
├── yolov8n-cbam.yaml         # 改进版 YOLO 模型网络结构配置
├── app.py                    # 预留的应用部署接口脚本
├── predict.py                # 推理与预测脚本
├── train_cbam.py             # 引入注意力机制的训练脚本
├── spider_images.py          # 数据集网络爬虫脚本
├── clean_data.py             # 数据清洗与预处理脚本
├── 1.test.jpg                # 快速测试用图
└── README.md                 # 项目说明文档

## 训练你自己的模型

如果你想基于这份代码继续训练或微调模型，请执行对应的训练脚本：

```bash
python train_cbam.py
```

(注：请在运行前确保数据集路径在相关脚本或 yaml 文件中配置正确)

## 许可证

本项目采用 MIT 许可证 - 查看 LICENSE 文件了解详情。

## 联系方式

- 项目作者: 杨乐
- 项目链接: https://github.com/yanglee0620-wq/Food-Logo-Detection

## 致谢

- [Ultralytics](https://github.com/ultralytics/ultralytics) - YOLOv8 目标检测框架
- [CBAM: Convolutional Block Attention Module](https://arxiv.org/abs/1807.06521) - 核心注意力机制参考