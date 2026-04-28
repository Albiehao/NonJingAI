"""
默认模型配置

该文件定义了系统支持的所有默认模型配置，包括：
- 聊天模型（LLM）
- 嵌入模型（Embedding）
- 重排序模型（Reranker）
"""

from pydantic import BaseModel, Field

class ChatModelInfo(BaseModel):
    """聊天模型配置"""
    model_id: str = Field(..., description="模型 ID")
    name:str = Field(..., description="模型名称")
    description: str = Field(..., description="模型描述")
    vision_support: bool = Field(default=False, description="是否支持视觉对话")
    supports_thinking: bool = Field(default=False, description="是否支持思考模式")
    default_thinking_effort: str = Field(default="medium", description="默认思考强度: low/medium/high/max")
    max_tokens: int | None = Field(default=None, description="最大输出token数")
    context_window: int | None = Field(default=None, description="上下文窗口大小")



class ChatModelProvider(BaseModel):
    """聊天模型提供商配置"""

    name: str = Field(..., description="提供商显示名称")
    url: str = Field(..., description="提供商文档或模型列表 URL")
    base_url: str = Field(..., description="API 基础 URL")
    default: str = Field(..., description="默认模型名称")
    env: str = Field(..., description="API Key 环境变量名")
    models: dict[str,ChatModelInfo] = Field(default_factory=dict, description="支持的模型列表")
    custom: bool = Field(default=False, description="是否为自定义供应商")



class EmbedModelInfo(BaseModel):
    """嵌入模型配置"""

    name: str = Field(..., description="模型名称")
    dimension: int = Field(..., description="向量维度")
    base_url: str = Field(..., description="API 基础 URL")
    api_key: str = Field(..., description="API Key 或环境变量名")
    model_id: str | None = Field(None, description="可选的模型 ID")


class RerankerInfo(BaseModel):
    """重排序模型配置"""

    name: str = Field(..., description="模型名称")
    base_url: str = Field(..., description="API 基础 URL")
    api_key: str = Field(..., description="API Key 或环境变量名")



# ============================================================
# 默认聊天厂商配置
# ============================================================

DEFAULT_CHAT_MODEL_PROVIDERS: dict[str, ChatModelProvider] = {
    "openai": ChatModelProvider(
        name="OpenAI",
        url="https://platform.openai.com/docs/models",
        base_url="https://api.openai.com/v1",
        default="gpt-5-mini",
        env="OPENAI_API_KEY",
        models={
            "gpt-5.2": ChatModelInfo(
                model_id="openai/gpt-5.2",
                name="GPT-5.2",
                description="OpenAI 最新旗舰模型",
                supports_thinking=False,
                context_window=2048,
            ),
            "gpt-5-mini": ChatModelInfo(
                model_id="openai/gpt-5-mini",
                name="GPT-5 Mini",
                description="轻量级快速模型",
                supports_thinking=False,
            ),
            "gpt-5.2-pro": ChatModelInfo(
                model_id="openai/gpt-5.2-pro",
                name="GPT-5.2 Pro",
                description="专业级高性能模型",
                supports_thinking=False,
            ),
        },
    ),
    "deepseek": ChatModelProvider(
        name="DeepSeek",
        url="https://platform.deepseek.com/api-docs/zh-cn/pricing",
        base_url="https://api.deepseek.com/v1",
        default="deepseek-chat",
        env="DEEPSEEK_API_KEY",
        models={
            "deepseek-v4-flash":ChatModelInfo(
                model_id="deepseek/deepseek-v4-flash",
                name="DeepSeek-V4.0-Flash",
                description="deepseek新一代模型",
                supports_thinking=True,
                default_thinking_effort="low",
                max_tokens=64_000,
                context_window=1_000_000

            ),
            "deepseek-v4-pro": ChatModelInfo(
                model_id="deepseek/deepseek-v4-pro",
                name="DeepSeek-V4.0-Flash-Pro",
                description="deepseek新一代模型",
                supports_thinking=True,
                default_thinking_effort="low",
                max_tokens=64_000,
                context_window=1_000_000
            ),
        },
    ),
    "zhipu": ChatModelProvider(
        name="智谱AI (Zhipu)",
        url="https://open.bigmodel.cn/dev/api",
        base_url="https://open.bigmodel.cn/api/paas/v4/",
        default="glm-4.7-flash",
        env="ZHIPUAI_API_KEY",
        models={
            # 最新旗舰模型系列
            "glm-5.1": ChatModelInfo(
                model_id="zhipuai/glm-5.1",
                name="GLM-5.1",
                description="智谱最新旗舰模型，最强性能",
                supports_thinking=True,
                default_thinking_effort="high",
                max_tokens=128_000,  # 推测值，需确认
                context_window=1_000_000,  # 推测值，需确认
            ),
            "glm-5-turbo": ChatModelInfo(
                model_id="zhipuai/glm-5-turbo",
                name="GLM-5-Turbo",
                description="GLM-5极速版，更快响应速度",
                supports_thinking=True,
                default_thinking_effort="medium",
                max_tokens=128_000,
                context_window=1_000_000,
            ),
            "glm-5": ChatModelInfo(
                model_id="zhipuai/glm-5",
                name="GLM-5",
                description="GLM-5基础版",
                supports_thinking=True,
                default_thinking_effort="medium",
                max_tokens=128_000,
                context_window=1_000_000,
            ),

            # GLM-4.7 系列（最新开源系列）
            "glm-4.7-flash": ChatModelInfo(
                model_id="zhipuai/glm-4.7-flash",
                name="GLM-4.7-Flash",
                description="30B参数MoE架构，免费调用，擅长编程和智能体任务[citation:2][citation:4]",
                supports_thinking=True,
                default_thinking_effort="low",
                max_tokens=128_000,  # 官方：最大输出128K[citation:6][citation:8]
                context_window=200_000,  # 官方：上下文200K[citation:2][citation:6]
            ),
            "glm-4.7": ChatModelInfo(
                model_id="zhipuai/glm-4.7",
                name="GLM-4.7",
                description="GLM-4.7基础版，编码能力强化",
                supports_thinking=True,
                default_thinking_effort="medium",
                max_tokens=128_000,
                context_window=200_000,
            ),
            "glm-4.6": ChatModelInfo(
                model_id="zhipuai/glm-4.6",
                name="GLM-4.6",
                description="GLM-4.6版本",
                supports_thinking=False,  # 较早版本可能不支持思考模式
                max_tokens=16_000,  # 推测值
                context_window=128_000,  # 推测值
            ),

            # GLM-4.5 系列
            "glm-4.5-air": ChatModelInfo(
                model_id="zhipuai/glm-4.5-air",
                name="GLM-4.5-Air",
                description="106B总参数/12B激活参数，轻量高效[citation:3][citation:5]",
                supports_thinking=True,
                default_thinking_effort="low",
                max_tokens=96_000,  # 官方：最大输出96K[citation:8]
                context_window=128_000,  # 官方：上下文128K[citation:8]
            ),
            "glm-4.5-airx": ChatModelInfo(
                model_id="zhipuai/glm-4.5-airx",
                name="GLM-4.5-AirX",
                description="GLM-4.5-Air增强版，更高性能",
                supports_thinking=True,
                default_thinking_effort="medium",
                max_tokens=96_000,
                context_window=128_000,
            ),
            "glm-4.5-flash": ChatModelInfo(
                model_id="zhipuai/glm-4.5-flash",
                name="GLM-4.5-Flash",
                description="支持深度思考模式（即将下线）[citation:8]",
                supports_thinking=True,
                default_thinking_effort="low",
                max_tokens=96_000,  # 官方：最大输出96K[citation:8]
                context_window=128_000,  # 官方：上下文128K[citation:8]
            ),

            # GLM-4 Flash 系列（免费模型）
            "glm-4-flash-250414": ChatModelInfo(
                model_id="zhipuai/glm-4-flash-250414",
                name="GLM-4-Flash-250414",
                description="免费模型，超长上下文处理能力[citation:8]",
                supports_thinking=False,
                max_tokens=16_000,  # 官方：最大输出16K[citation:8]
                context_window=128_000,  # 官方：上下文128K[citation:8]
            ),
            "glm-4-flashx-250414": ChatModelInfo(
                model_id="zhipuai/glm-4-flashx-250414",
                name="GLM-4-FlashX-250414",
                description="GLM-4-Flash增强版，更高性能",
                supports_thinking=True,
                default_thinking_effort="low",
                max_tokens=32_000,
                context_window=200_000,
            ),
        },
    ),
    "siliconflow": ChatModelProvider(
        name="SiliconFlow",
        url="https://cloud.siliconflow.cn/models",
        base_url="https://api.siliconflow.cn/v1",
        default="Pro/deepseek-ai/DeepSeek-V3.2",
        env="SILICONFLOW_API_KEY",
        models={
            # 1. DeepSeek V3.2 - 性价比首选，稳定可靠
            "Pro/deepseek-ai/DeepSeek-V3.2": ChatModelInfo(
                model_id="Pro/deepseek-ai/DeepSeek-V3.2",
                name="DeepSeek-V3.2",
                description="旗舰全能模型，支持Vibe Coding，¥2/M输入，多轮对话稳定",
                supports_thinking=True,
                default_thinking_effort="low",
                max_tokens=8192,
                context_window=128000,
            ),
            # 2. GLM-5.1 - 智谱最新旗舰，Agent能力最强
            "Pro/zai-org/GLM-5.1": ChatModelInfo(
                model_id="Pro/zai-org/GLM-5.1",
                name="GLM-5.1",
                description="智谱旗舰，专为长时Agent任务设计，SWE-Bench Pro SOTA，可连续工作8小时",
                supports_thinking=True,
                default_thinking_effort="high",
                max_tokens=131072,
                context_window=205000,
            ),
            # 3. Kimi-K2.6 - 月之暗面最新版，长文本处理最强
            "Pro/moonshotai/Kimi-K2.6": ChatModelInfo(
                model_id="Pro/moonshotai/Kimi-K2.6",
                name="Kimi-K2.6",
                description="月之暗面最新旗舰，长文本理解与多模态能力突出，Agent场景优秀",
                supports_thinking=True,
                default_thinking_effort="medium",
                max_tokens=262144,
                context_window=262144,
            ),
            # 4. MiniMax-M2.5 - 专为Agent和编程优化
            "Pro/MiniMaxAI/MiniMax-M2.5": ChatModelInfo(
                model_id="Pro/MiniMaxAI/MiniMax-M2.5",
                name="MiniMax-M2.5",
                description="Agent专用模型，交错思维链，编程能力强，性价比高（¥2.1/M输入）",
                supports_thinking=True,
                default_thinking_effort="medium",
                max_tokens=80000,
                context_window=1000000,
            ),
            # 5. Qwen3.5-397B-A17B - 通义千问最大参数MoE
            "Qwen/Qwen3.5-397B-A17B": ChatModelInfo(
                model_id="Qwen/Qwen3.5-397B-A17B",
                name="Qwen3.5-397B",
                description="阿里通义最大参数模型（397B总参数/17B激活），输出极便宜（¥1.2/M），知识广度最大",
                supports_thinking=False,
                default_thinking_effort=None,
                max_tokens=8192,
                context_window=128000,
            ),
        },
    ),
    "dashscope": ChatModelProvider(
        name="阿里百炼 (DashScope)",
        url="https://bailian.console.aliyun.com/?switchAgent=10226727&productCode=p_efm#/model-market",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        default="qwen3.6-plus",
        env="DASHSCOPE_API_KEY",
        models={
            # ==================== 千问系列 ====================
            "qwen3.6-plus": ChatModelInfo(
                model_id="qwen3.6-plus",
                name="Qwen3.6-Plus",
                description="文本生成、深度思考、视觉理解",
                vision_support=True,
                supports_thinking=True,
                default_thinking_effort="medium",
                max_tokens=8192,
                context_window=128000,
            ),
            "qwen3.5-plus": ChatModelInfo(
                model_id="qwen3.5-plus",
                name="Qwen3.5-Plus",
                description="文本生成、深度思考、视觉理解",
                vision_support=True,
                supports_thinking=True,
                default_thinking_effort="medium",
                max_tokens=8192,
                context_window=128000,
            ),
            "qwen3-max-2026-01-23": ChatModelInfo(
                model_id="qwen3-max-2026-01-23",
                name="Qwen3-Max",
                description="文本生成、深度思考",
                vision_support=False,
                supports_thinking=True,
                default_thinking_effort="high",
                max_tokens=16384,
                context_window=256000,
            ),
            "qwen3-coder-next": ChatModelInfo(
                model_id="qwen3-coder-next",
                name="Qwen3-Coder-Next",
                description="文本生成",
                vision_support=False,
                supports_thinking=False,
                default_thinking_effort=None,
                max_tokens=16384,
                context_window=128000,
            ),
            "qwen3-coder-plus": ChatModelInfo(
                model_id="qwen3-coder-plus",
                name="Qwen3-Coder-Plus",
                description="文本生成",
                vision_support=False,
                supports_thinking=False,
                default_thinking_effort=None,
                max_tokens=8192,
                context_window=128000,
            ),

            # ==================== 智谱系列 ====================
            "glm-5": ChatModelInfo(
                model_id="glm-5",
                name="GLM-5",
                description="文本生成、深度思考",
                vision_support=False,
                supports_thinking=True,
                default_thinking_effort="high",
                max_tokens=8192,
                context_window=200000,
            ),
            "glm-4.7": ChatModelInfo(
                model_id="glm-4.7",
                name="GLM-4.7",
                description="文本生成、深度思考",
                vision_support=False,
                supports_thinking=True,
                default_thinking_effort="medium",
                max_tokens=8192,
                context_window=128000,
            ),

            # ==================== Kimi 系列 ====================
            "kimi-k2.5": ChatModelInfo(
                model_id="kimi-k2.5",
                name="Kimi-K2.5",
                description="文本生成、深度思考、视觉理解",
                vision_support=True,
                supports_thinking=True,
                default_thinking_effort="medium",
                max_tokens=8192,
                context_window=262144,
            ),

            # ==================== MiniMax 系列 ====================
            "MiniMax-M2.5": ChatModelInfo(
                model_id="MiniMax-M2.5",
                name="MiniMax-M2.5",
                description="文本生成、深度思考",
                vision_support=False,
                supports_thinking=True,
                default_thinking_effort="medium",
                max_tokens=8192,
                context_window=1000000,
            ),
        },
    ),
    "ark": ChatModelProvider(
        name="豆包（Ark）",
        url="https://console.volcengine.com/ark/region:ark+cn-beijing/model",
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        default="doubao-seed-2-0-lite-260215",
        env="ARK_API_KEY",
        models={},
    ),

    "modelscope": ChatModelProvider(
        name="ModelScope",
        url="https://www.modelscope.cn/docs/model-service/API-Inference/intro",
        base_url="https://api-inference.modelscope.cn/v1/",
        default="deepseek-ai/DeepSeek-V3.2",
        env="MODELSCOPE_ACCESS_TOKEN",
        models={},
    ),
}


# ============================================================
# 默认嵌入模型配置
# ============================================================

DEFAULT_EMBED_MODELS: dict[str, EmbedModelInfo] = {
    "siliconflow/BAAI/bge-m3": EmbedModelInfo(
        model_id="siliconflow/BAAI/bge-m3",
        name="BAAI/bge-m3",
        dimension=1024,
        base_url="https://api.siliconflow.cn/v1/embeddings",
        api_key="SILICONFLOW_API_KEY",
    ),
    "siliconflow/Pro/BAAI/bge-m3": EmbedModelInfo(
        model_id="siliconflow/Pro/BAAI/bge-m3",
        name="Pro/BAAI/bge-m3",
        dimension=1024,
        base_url="https://api.siliconflow.cn/v1/embeddings",
        api_key="SILICONFLOW_API_KEY",
    ),
    "siliconflow/Qwen/Qwen3-Embedding-0.6B": EmbedModelInfo(
        model_id="siliconflow/Qwen/Qwen3-Embedding-0.6B",
        name="Qwen/Qwen3-Embedding-0.6B",
        dimension=1024,
        base_url="https://api.siliconflow.cn/v1/embeddings",
        api_key="SILICONFLOW_API_KEY",
    ),
    "vllm/Qwen/Qwen3-Embedding-0.6B": EmbedModelInfo(
        model_id="vllm/Qwen/Qwen3-Embedding-0.6B",
        name="Qwen3-Embedding-0.6B",
        dimension=1024,
        base_url="http://localhost:8000/v1/embeddings",
        api_key="no_api_key",
    ),
    "ollama/nomic-embed-text": EmbedModelInfo(
        model_id="ollama/nomic-embed-text",
        name="nomic-embed-text",
        dimension=768,
        base_url="http://localhost:11434/api/embed",
        api_key="no_api_key",
    ),
    "ollama/bge-m3": EmbedModelInfo(
        model_id="ollama/bge-m3",
        name="bge-m3",
        dimension=1024,
        base_url="http://localhost:11434/api/embed",
        api_key="no_api_key",
    ),
    "dashscope/text-embedding-v4": EmbedModelInfo(
        model_id="dashscope/text-embedding-v4",
        name="text-embedding-v4",
        dimension=1024,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1/embeddings",
        api_key="DASHSCOPE_API_KEY",
    ),
}


# ============================================================
# 默认重排序模型配置
# ============================================================

DEFAULT_RERANKERS: dict[str, RerankerInfo] = {
    "siliconflow/BAAI/bge-reranker-v2-m3": RerankerInfo(
        name="BAAI/bge-reranker-v2-m3",
        base_url="https://api.siliconflow.cn/v1/rerank",
        api_key="SILICONFLOW_API_KEY",
    ),
    "siliconflow/Pro/BAAI/bge-reranker-v2-m3": RerankerInfo(
        name="Pro/BAAI/bge-reranker-v2-m3",
        base_url="https://api.siliconflow.cn/v1/rerank",
        api_key="SILICONFLOW_API_KEY",
    ),
    "dashscope/gte-rerank-v2": RerankerInfo(
        name="gte-rerank-v2",
        base_url="https://dashscope.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank",
        api_key="DASHSCOPE_API_KEY",
    ),
    "dashscope/qwen3-rerank": RerankerInfo(
        name="qwen3-rerank",
        base_url="https://dashscope.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank",
        api_key="DASHSCOPE_API_KEY",
    ),
    "vllm/BAAI/bge-reranker-v2-m3": RerankerInfo(
        name="BAAI/bge-reranker-v2-m3",
        base_url="http://localhost:8000/v1/rerank",
        api_key="no_api_key",
    ),
}
