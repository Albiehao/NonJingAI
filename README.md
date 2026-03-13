# 农镜 AI - 基于 YOLO 视觉感知与大模型认知的精准农业垂直平台
本项目基于 Yuxi-Know 进行二次开发与深度定制，专为智慧农业场景打造
🌱 视觉感知 (YOLO) × 🧠 认知推理 (LLM + Knowledge Graph)

![Stable](https://img.shields.io/badge/stable-v1.0.0-agriculture.svg)
![](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=ffffff)
![YOLO](https://img.shields.io/badge/Vision-YOLOv8/v10-orange?logo=opencv)
![demo](https://img.shields.io/badge/demo-00A1D6.svg?style=flat&logo=bilibili&logoColor=white)

<img src="image.png" width="300" />

图片由豆包生成
## 🚜 项目简介

**农镜 AI** 是一款面向现代农业的垂直领域人工智能平台。它创新性地将 **YOLO 系列高精度目标检测算法** 与 **大语言模型（LLM）+ 知识图谱（KG）** 相结合，构建了“眼脑协同”的智能农业系统。

- **眼（视觉层）**：利用 YOLOv8/v10 实时识别农作物病虫害、杂草、果实成熟度及生长状态。
- **脑（认知层）**：基于农业专业知识库与图谱，对视觉结果进行深度推理，生成防治方案、农事建议及产量预测。

## ✨ 核心特性

### 📷 智能视觉感知 (YOLO Powered)
- **多类别精准识别**：内置针对农业场景优化的 YOLO 模型，支持数百种病虫害、杂草及作物生长阶段识别。

### 🧠 农业知识大脑 (RAG + KG)
- **病虫害专家系统**：结合视觉识别结果，自动检索知识库，提供权威的防治建议、农药配比及施药窗口期。
- **动态知识图谱**：构建“作物 - 病害 - 环境 - 防治”关联图谱，支持多跳推理（例如：发现病斑 -> 推断病害 -> 关联近期气象 -> 推荐最佳防治方案）。
- **多模态文档解析**：支持上传农业论文、植保手册、历史农事记录（PDF/Word/图片），自动转化为可问答的知识库。

### 🤖 智能体决策 (Agentic Workflow)
- **农事规划智能体**：根据识别结果与气象数据，自动生成未来一周的灌溉、施肥、打药计划。
- **产量预估智能体**：基于果实计数与生长周期图谱，辅助预测地块产量。
- **私有化部署**：支持本地服务器部署，确保农场敏感数据（地块信息、产量数据）不出域。

## 🛠 应用场景

| 场景 | 功能描述 | 技术支撑 |
| :--- | :--- | :--- |
| **病虫害诊断** | 拍照/视频自动识别病害种类，秒级输出防治方案 | YOLO 检测 + RAG 检索 |
| **杂草管理** | 区分作物与杂草，生成变量喷药处方图 | YOLO 分割 + 决策智能体 |
| **长势监测** | 统计株数、估测叶面积指数、判断成熟度 | 目标计数 + 时序分析 |
| **农业问答助手** | 基于内部知识库的自然语言问答，解决种植难题 | LLM + 知识图谱 |

## 🚀 快速开始

### 1. 环境准备
确保已安装 Docker 及 Docker Compose。

### 2. 克隆与初始化
```bash
# 克隆项目
git clone --branch v1.0.0-nongjing https://github.com/your-repo/NongJing-AI.git
cd NongJing-AI

# 初始化脚本 (Linux/macOS)
./scripts/init.sh

# 初始化脚本 (Windows PowerShell)
.\scripts\init.ps1
```

### 3. 配置视觉模型
在 `config/vision.yaml` 中指定您的 YOLO 模型权重路径（支持 `.pt` 格式）：
```yaml
vision:
  model_path: "./models/yolo_v8_crop_pest.pt"
  confidence_threshold: 0.6
  classes: ["aphid", "rust", "powdery_mildew", "mature_fruit"]
```

### 4. 启动服务
```bash
docker compose up --build
```

启动完成后，访问 `http://localhost:5173` 即可使用平台。

## 📸 系统演示

### 视觉识别与推理联动

*(图示：系统实时识别叶片病斑，并自动调用知识库生成防治建议)*

### 知识图谱可视化

*(图示：作物 - 病害 - 农药关联图谱，辅助决策推理)*

### 智能体农事规划

*(图示：基于识别结果自动生成的周农事计划表)*

## 🏢 技术支持与服务

农镜 AI 专注于为农业科技公司、大型农场及科研机构提供定制化解决方案。

- **模型定制训练**：针对特定作物（如柑橘、水稻、玉米）定制高精度 YOLO 模型。
- **知识库构建**：协助整理地方性植保知识，构建专属农业知识图谱。
- **边缘端部署**：支持 Jetson Orin 等边缘设备部署，实现田间离线智能分析。

📧 **商务合作与技术咨询**：1185902279@qq.com
