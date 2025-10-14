"""
utils 模块的单元测试

确保所有工具函数都能正常工作
"""

import sys
import os

import pytest

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.utils.math_utils import calculate_average, find_max_min, calculate_statistics


class TestMathUtils:
    """测试数学工具函数"""

    def test_calculate_average(self):
        """测试计算平均值"""
        result = calculate_average([1, 2, 3, 4, 5])
        assert result == 3.0

    def test_calculate_average_floats(self):
        """测试浮点数平均值"""
        result = calculate_average([1.5, 2.5, 3.0])
        expected = 2.333333
        assert abs(result - expected) < 0.0001

    def test_calculate_average_empty(self):
        """测试空列表"""
        with pytest.raises(ValueError):
            calculate_average([])

    def test_find_max_min(self):
        """测试查找最大最小值"""
        max_val, min_val = find_max_min([3, 1, 4, 1, 5, 9, 2, 6])
        assert max_val == 9
        assert min_val == 1

    def test_find_max_min_negative(self):
        """测试负数的最大最小值"""
        max_val, min_val = find_max_min([-5, -2, -10, -1])
        assert max_val == -1
        assert min_val == -10

    def test_find_max_min_empty(self):
        """测试空列表"""
        with pytest.raises(ValueError):
            find_max_min([])

    def test_calculate_statistics(self):
        """测试完整统计信息（含 numpy 增强功能）"""
        result = calculate_statistics([1, 2, 3, 4, 5])
        assert result["count"] == 5
        assert result["sum"] == 15
        assert result["average"] == 3.0
        assert result["max"] == 5
        assert result["min"] == 1
        # 测试 numpy 新增的统计功能
        assert "std" in result
        assert "variance" in result
        assert result["std"] > 0  # 标准差应该大于0
        assert result["variance"] > 0  # 方差应该大于0

    def test_calculate_statistics_empty(self):
        """测试空列表统计"""
        result = calculate_statistics([])
        assert result["count"] == 0
        assert result["sum"] == 0
        assert result["average"] == 0
        assert result["max"] is None
        assert result["min"] is None
        assert result["std"] is None
        assert result["variance"] is None
