"""Crop Agent - 千寻有方模块

基于 deepagents 库构建的农业领域智能体，具备以下特性：
- 农作物病虫害识别与诊断
- 病因分析与防治方案制定
- 用药建议与抗性管理
- 综合防治策略与预防措施规划
"""

from .context import CropContext
from .graph import CropAgent

__all__ = [
    "CropAgent",
    "CropContext",
]

__version__ = "1.0.0"
__author__ = "QianXun Team"
__description__ = "基于 create_deep_agent 的农作物病虫害防治诊疗智能体"
