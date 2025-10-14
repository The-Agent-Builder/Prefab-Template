"""
main.py 的单元测试

确保所有预制件函数都能正常工作
"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src import analyze_dataset


class TestAnalyzeDataset:
    """测试 analyze_dataset 函数"""

    def test_statistics_operation(self):
        """测试统计操作"""
        result = analyze_dataset([1, 2, 3, 4, 5], "statistics")
        assert result["success"] is True
        assert "data" in result
        assert result["data"]["operation"] == "statistics"
        assert result["data"]["statistics"]["count"] == 5
        assert result["data"]["statistics"]["average"] == 3.0
        assert result["data"]["statistics"]["max"] == 5
        assert result["data"]["statistics"]["min"] == 1

    def test_sum_operation(self):
        """测试求和操作"""
        result = analyze_dataset([10, 20, 30], "sum")
        assert result["success"] is True
        assert result["data"]["operation"] == "sum"
        assert result["data"]["value"] == 60
        assert result["data"]["count"] == 3

    def test_average_operation(self):
        """测试平均值操作"""
        result = analyze_dataset([2, 4, 6], "average")
        assert result["success"] is True
        assert result["data"]["operation"] == "average"
        assert result["data"]["value"] == 4.0
        assert result["data"]["count"] == 3

    def test_default_operation(self):
        """测试默认操作（statistics）"""
        result = analyze_dataset([1, 2, 3])
        assert result["success"] is True
        assert result["data"]["operation"] == "statistics"

    def test_empty_data(self):
        """测试空数据集"""
        result = analyze_dataset([])
        assert result["success"] is False
        assert result["error"] == "数据集不能为空"
        assert result["error_code"] == "EMPTY_DATA"

    def test_invalid_operation(self):
        """测试无效操作类型"""
        result = analyze_dataset([1, 2, 3], "invalid_op")
        assert result["success"] is False
        assert "不支持的操作类型" in result["error"]
        assert result["error_code"] == "INVALID_OPERATION"

    def test_negative_numbers(self):
        """测试负数"""
        result = analyze_dataset([-5, -2, 0, 3, 7], "statistics")
        assert result["success"] is True
        assert result["data"]["statistics"]["sum"] == 3
        assert result["data"]["statistics"]["average"] == 0.6

    def test_float_numbers(self):
        """测试浮点数"""
        result = analyze_dataset([1.5, 2.5, 3.5], "average")
        assert result["success"] is True
        assert result["data"]["value"] == 2.5
