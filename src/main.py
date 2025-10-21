"""
预制件核心逻辑模块

这是一个示例预制件，展示了如何创建可被 AI 调用的函数。
所有暴露给 AI 的函数都必须在此文件中定义。

📁 文件路径约定：
- 输入文件：data/inputs/<文件名>
- 输出文件：data/outputs/<文件名>
- 所有文件参数都是列表形式（即使只有一个文件）

📖 完整开发指南请查看：PREFAB_GUIDE.md
"""

import os
from pathlib import Path
from typing import List


# 固定路径常量
DATA_INPUTS = Path("data/inputs")
DATA_OUTPUTS = Path("data/outputs")


def greet(name: str = "World") -> dict:
    """
    向用户问候

    这是一个简单的示例函数，展示了预制件函数的基本结构。

    Args:
        name: 要问候的名字，默认为 "World"

    Returns:
        包含问候结果的字典

    Examples:
        >>> greet()
        {'success': True, 'message': 'Hello, World!', 'name': 'World'}

        >>> greet(name="Alice")
        {'success': True, 'message': 'Hello, Alice!', 'name': 'Alice'}
    """
    try:
        # 参数验证
        if not name or not isinstance(name, str):
            return {
                "success": False,
                "error": "name 参数必须是非空字符串",
                "error_code": "INVALID_NAME"
            }

        # 生成问候消息
        message = f"Hello, {name}!"

        return {
            "success": True,
            "message": message,
            "name": name
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_code": "UNEXPECTED_ERROR"
        }


def echo(text: str) -> dict:
    """
    回显输入的文本

    这个函数演示了基本的输入输出处理。

    Args:
        text: 要回显的文本

    Returns:
        包含回显结果的字典
    """
    try:
        if not text:
            return {
                "success": False,
                "error": "text 参数不能为空",
                "error_code": "EMPTY_TEXT"
            }

        return {
            "success": True,
            "original": text,
            "echo": text,
            "length": len(text)
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_code": "UNEXPECTED_ERROR"
        }


def add_numbers(a: float, b: float) -> dict:
    """
    计算两个数字的和

    这个函数演示了数值计算的基本模式。

    Args:
        a: 第一个数字
        b: 第二个数字

    Returns:
        包含计算结果的字典
    """
    try:
        result = a + b
        return {
            "success": True,
            "a": a,
            "b": b,
            "sum": result
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_code": "CALCULATION_ERROR"
        }


def process_text_file(input_files: List[str], operation: str = "uppercase") -> dict:
    """
    处理文本文件（文件处理示例）

    这个函数演示了如何处理文件输入和输出。

    📁 文件约定：
    - 输入：Gateway 下载到 data/inputs/<文件名>，传入文件名列表
    - 输出：写入 data/outputs/<文件名>，返回相对路径
    - Gateway 会自动上传 data/outputs/ 中的文件并替换路径为 S3 URL

    Args:
        input_files: 输入文件名列表（只取第一个）
        operation: 操作类型（uppercase, lowercase, reverse）

    Returns:
        包含处理结果的字典
    """
    try:
        # 获取第一个输入文件
        input_filename = input_files[0]
        input_path = DATA_INPUTS / input_filename

        # 验证文件存在
        if not input_path.exists():
            return {
                "success": False,
                "error": f"输入文件不存在: {input_filename}",
                "error_code": "FILE_NOT_FOUND"
            }

        # 读取文件内容
        content = input_path.read_text(encoding="utf-8")

        # 执行操作
        if operation == "uppercase":
            result = content.upper()
        elif operation == "lowercase":
            result = content.lower()
        elif operation == "reverse":
            result = content[::-1]
        else:
            return {
                "success": False,
                "error": f"不支持的操作: {operation}",
                "error_code": "INVALID_OPERATION"
            }

        # 确保输出目录存在
        DATA_OUTPUTS.mkdir(parents=True, exist_ok=True)

        # 写入输出文件
        output_filename = f"processed_{input_filename}"
        output_path = DATA_OUTPUTS / output_filename
        output_path.write_text(result, encoding="utf-8")

        # 返回结果（相对路径，Gateway 会自动替换为 S3 URL）
        return {
            "success": True,
            "input_file": input_filename,
            "output_file": f"data/outputs/{output_filename}",
            "operation": operation,
            "original_length": len(content),
            "processed_length": len(result)
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_code": "PROCESSING_ERROR"
        }


def fetch_weather(city: str) -> dict:
    """
    获取指定城市的天气信息（示例函数，演示 secrets 的使用）

    这个函数演示了如何在预制件中使用密钥（secrets）。
    平台会自动将用户配置的密钥注入到环境变量中。

    注意：这是一个演示函数，实际不会调用真实的天气 API。

    Args:
        city: 要查询天气的城市名称

    Returns:
        包含天气信息的字典

    Examples:
        >>> fetch_weather(city="北京")
        {'success': True, 'city': '北京', 'temperature': 22.5, 'condition': '晴天'}
    """
    try:
        # 从环境变量中获取 API Key（平台会自动注入）
        api_key = os.environ.get('WEATHER_API_KEY')

        # 验证密钥是否已配置
        if not api_key:
            return {
                "success": False,
                "error": "未配置 WEATHER_API_KEY，请在平台上配置该密钥",
                "error_code": "MISSING_API_KEY"
            }

        # 验证参数
        if not city or not isinstance(city, str):
            return {
                "success": False,
                "error": "city 参数必须是非空字符串",
                "error_code": "INVALID_CITY"
            }

        # 这里是演示代码，实际应该调用真实的天气 API
        # import requests
        # response = requests.get(
        #     f"https://api.weather-provider.com/current",
        #     params={"city": city, "key": api_key}
        # )
        # data = response.json()

        # 演示：返回模拟数据
        return {
            "success": True,
            "city": city,
            "temperature": 22.5,
            "condition": "晴天",
            "note": "这是演示数据，未调用真实 API"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_code": "UNEXPECTED_ERROR"
        }
