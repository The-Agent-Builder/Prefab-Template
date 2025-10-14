"""
数学计算工具

提供各种数学计算功能
"""

from typing import List, Tuple, Union


def calculate_average(numbers: List[Union[int, float]]) -> float:
    """
    计算平均值

    Args:
        numbers: 数字列表

    Returns:
        平均值

    Raises:
        ValueError: 如果列表为空
    """
    if not numbers:
        raise ValueError("数字列表不能为空")

    return sum(numbers) / len(numbers)


def find_max_min(numbers: List[Union[int, float]]) -> Tuple[float, float]:
    """
    找出最大值和最小值

    Args:
        numbers: 数字列表

    Returns:
        (最大值, 最小值) 元组

    Raises:
        ValueError: 如果列表为空
    """
    if not numbers:
        raise ValueError("数字列表不能为空")

    return max(numbers), min(numbers)


def calculate_statistics(numbers: List[Union[int, float]]) -> dict:
    """
    计算统计信息

    Args:
        numbers: 数字列表

    Returns:
        包含统计信息的字典
    """
    if not numbers:
        return {
            "count": 0,
            "sum": 0,
            "average": 0,
            "max": None,
            "min": None
        }

    max_val, min_val = find_max_min(numbers)

    return {
        "count": len(numbers),
        "sum": sum(numbers),
        "average": calculate_average(numbers),
        "max": max_val,
        "min": min_val
    }
