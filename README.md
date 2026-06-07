# 禾影千寻

基于大模型、知识图谱与视觉识别的智能分析平台，融合 RAG、知识图谱、YOLO 图像识别与 Agent 推理能力，技术栈为 LangGraph v1 + Vue.js + FastAPI + LightRAG。

<img src="image.png" width="320" alt="禾影千寻预览图" />

## 系统架构

![img.png](img.png)![禾影千寻系统架构图](docs/images/heyin-qianxun-architecture.png)

## 项目简介

禾影千寻面向企业知识管理、图谱构建、视觉识别和智能分析场景，提供从文档接入、知识检索、图像识别到推理决策的一体化能力。

当前仓库通过 Docker Compose 管理开发环境，前后端默认开启热重载，适合本地联调和二次开发。

## 核心能力

- 文档知识库：支持文档导入、解析、切分、向量化与检索
- 知识图谱：基于 Neo4j 构建实体与关系图谱
- 智能问答：结合 RAG、图谱和外部工具增强问答效果
- YOLO 识别：对上传图片进行目标识别并输出标注结果
- 思考模式：支持对兼容模型开启思考模式，并配置思考强度
- 智能体编排：基于 LangGraph 构建多步骤 Agent 工作流
- 私有化部署：前后端与依赖服务统一由 Docker Compose 编排，适合内网或本地部署

## 技术栈

- 前端：Vue.js
- 后端：FastAPI
- Agent 编排：LangGraph v1
- RAG：LightRAG
- 图数据库：Neo4j
- 向量数据库：Milvus
- 关系数据库：PostgreSQL
- 对象存储：MinIO

## 主要功能

### 知识库问答

- 支持接入文档型知识库
- 支持文档解析、切分、向量检索和问答联动
- 可结合外部搜索与图谱结果生成回答

### 知识图谱分析

- 支持实体与关系存储
- 可通过图谱查询补充问答上下文
- 适合做领域知识关联分析和辅助决策

### YOLO 图像识别

平台内置独立的 `yoloapi` 服务，支持对图片执行目标识别。当前识别流程包括：

- 从对象存储读取图片
- 使用 YOLO 模型执行检测
- 返回识别类别、置信度和边界框坐标
- 自动生成带标注框的结果图片并回传链接

适合用于病害识别、目标检测、现场巡检、样本识别等场景。

### 思考模式

智能体支持为兼容模型开启思考模式，并可配置思考强度：

- `low`
- `medium`
- `high`
- `xhigh`

该模式适合多步骤推理、工具调用、复杂问答和链路较长的分析任务。对不支持思考模式的模型不会强制启用。

### Agent 工作流

- 支持基于 LangGraph 的多步骤执行
- 支持工具调用、附件处理、上下文持久化
- 支持结合知识库、图谱、搜索、天气、计算和 YOLO 工具协同工作

## 目录结构

```text
.
├─server/              # FastAPI 入口与服务端代码
├─src/                 # Python 核心业务模块
├─web/                 # Vue 前端
├─docs/                # VitePress 文档
├─docker/              # Dockerfile 与相关配置
├─models/              # 本地模型目录
├─saves/               # 上传文件与运行数据
├─scripts/             # 辅助脚本
└─test/                # 测试代码
```

## 快速开始

### 1. 环境准备

确保本机已安装：

- Docker
- Docker Compose

### 2. 初始化配置

复制环境变量模板并按需填写：

```bash
cp .env.template .env
```

至少建议检查以下配置：

- `SILICONFLOW_API_KEY`
- `TAVILY_API_KEY`
- `YUXI_SUPER_ADMIN_NAME`
- `YUXI_SUPER_ADMIN_PASSWORD`
- `MODEL_DIR`
- `SAVE_DIR`

### 3. 启动开发环境

```bash
docker compose up -d
```

服务启动后可访问：

- 前端：http://localhost:5173
- 后端 API：http://localhost:5050
- Neo4j：http://localhost:7474
- MinIO Console：http://localhost:9001

## 开发方式

本项目推荐直接在运行中的容器内调试。代码改动后不需要手动重启 `api-dev` 和 `web-dev`，服务会自动热更新。

常用命令：

```bash
docker ps
docker logs api-dev --tail 100
make lint
make format
docker compose exec api uv run python test/your_script.py
```

后端接口调试可使用 `.env` 中的 `YUXI_SUPER_ADMIN_NAME` / `YUXI_SUPER_ADMIN_PASSWORD`。

## 主要服务

默认开发编排包含以下核心服务：

- `api`: FastAPI 后端，端口 `5050`
- `web`: Vue 前端，端口 `5173`
- `postgres`: PostgreSQL，端口 `5432`
- `graph`: Neo4j，端口 `7474` / `7687`
- `milvus`: 向量数据库，端口 `19530`
- `minio`: 对象存储，端口 `9000` / `9001`

`mineru-vllm-server`、`mineru-api`、`paddlex` 等服务通过 profile 提供，可按需启用。
