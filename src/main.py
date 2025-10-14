"""
预制件核心逻辑模块

这是一个示例预制件，展示了如何创建可被 AI 调用的函数。
所有暴露给 AI 的函数都必须在此文件中定义。

你可以在 src/ 目录下创建多个模块文件，然后在此处导入使用。
"""

from .utils.math_utils import calculate_statistics


def analyze_dataset(data: list, operation: str = "statistics") -> dict:
    """
    分析数据集并返回统计结果

    Args:
        data: 数字列表
        operation: 操作类型 ("statistics", "sum", "average")

    Returns:
        包含分析结果的字典
    """
    try:
        if not data:
            return {
                "success": False,
                "error": "数据集不能为空",
                "error_code": "EMPTY_DATA"
            }

        if operation == "sum":
            result = {
                "operation": "sum",
                "value": sum(data),
                "count": len(data)
            }
        elif operation == "average":
            result = {
                "operation": "average",
                "value": sum(data) / len(data),
                "count": len(data)
            }
        elif operation == "statistics":
            stats = calculate_statistics(data)
            result = {
                "operation": "statistics",
                "statistics": stats
            }
        else:
            return {
                "success": False,
                "error": f"不支持的操作类型: {operation}",
                "error_code": "INVALID_OPERATION"
            }

        return {
            "success": True,
            "data": result
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_code": "UNEXPECTED_ERROR"
        }
