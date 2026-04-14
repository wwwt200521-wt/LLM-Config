# LLM-Config

本人人工智能课上的学习内容，用于管理和配置各类大语言模型（LLM）的参数与接口。

## 项目结构

```
LLM-Config/
├── config/                  # 模型配置文件
│   ├── default.yaml         # 默认配置
│   └── models/              # 各模型独立配置
├── src/                     # 核心源码
│   ├── __init__.py
│   └── llm_config.py        # LLM 配置管理模块
├── examples/                # 示例脚本
│   └── basic_usage.py
├── requirements.txt         # Python 依赖
└── README.md
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置模型

复制并修改 `config/default.yaml`：

```yaml
model:
  provider: openai
  name: gpt-4o
  api_key: YOUR_API_KEY
  temperature: 0.7
  max_tokens: 2048
```

### 3. 使用示例

```python
from src.llm_config import LLMConfig

cfg = LLMConfig("config/default.yaml")
print(cfg)
```

## 支持的模型提供商

| 提供商 | 说明 |
|--------|------|
| OpenAI | GPT-3.5 / GPT-4 系列 |
| Anthropic | Claude 系列 |
| Google | Gemini 系列 |
| Ollama | 本地开源模型 |

## 许可证

MIT
