"""基本使用示例：加载默认配置并打印。

运行前请先安装包：
    pip install -e .
"""

from pathlib import Path

from src.llm_config import LLMConfig


def main() -> None:
    config_path = Path(__file__).parent.parent / "config" / "default.yaml"
    cfg = LLMConfig(config_path)

    print("=== LLM 配置 ===")
    print(cfg)
    print()
    print("详细参数：")
    for key, value in cfg.to_dict().items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
