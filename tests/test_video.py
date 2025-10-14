"""
测试视频处理功能

这个测试文件演示了如何使用真实的媒体文件进行测试。
测试数据（tests/test.mp4）被提交到仓库中，确保测试的可重现性。
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from pathlib import Path
from src.main import video_to_audio


class TestVideoToAudio:
    """视频转音频功能测试类"""

    @pytest.fixture
    def test_video_path(self):
        """测试视频文件路径"""
        return os.path.join(os.path.dirname(__file__), "test.mp4")

    @pytest.fixture
    def output_audio_path(self):
        """输出音频文件路径"""
        return os.path.join(os.path.dirname(__file__), "test_output.mp3")

    @pytest.fixture(autouse=True)
    def cleanup(self, output_audio_path):
        """测试后清理生成的文件"""
        yield
        # 清理可能生成的音频文件
        test_dir = os.path.dirname(__file__)
        patterns = ["test_output.mp3", "test.mp3", "test.wav", "test.aac"]
        for pattern in patterns:
            filepath = os.path.join(test_dir, pattern)
            if os.path.exists(filepath):
                os.remove(filepath)

    def test_video_to_audio_default(self, test_video_path):
        """测试默认参数的视频转音频"""
        if not os.path.exists(test_video_path):
            pytest.skip(f"测试视频文件不存在: {test_video_path}")

        result = video_to_audio(test_video_path)

        assert result["success"] is True
        assert "data" in result
        assert result["data"]["format"] == "mp3"
        assert os.path.exists(result["data"]["output_file"])
        assert result["data"]["duration"] > 0

    def test_video_to_audio_custom_output(self, test_video_path, output_audio_path):
        """测试自定义输出路径"""
        if not os.path.exists(test_video_path):
            pytest.skip(f"测试视频文件不存在: {test_video_path}")

        result = video_to_audio(test_video_path, output_audio_path)

        assert result["success"] is True
        assert result["data"]["output_file"] == output_audio_path
        assert os.path.exists(output_audio_path)

    def test_video_to_audio_wav_format(self, test_video_path):
        """测试 WAV 格式输出"""
        if not os.path.exists(test_video_path):
            pytest.skip(f"测试视频文件不存在: {test_video_path}")

        output_path = os.path.join(os.path.dirname(test_video_path), "test.wav")
        result = video_to_audio(test_video_path, output_path, audio_format="wav")

        assert result["success"] is True
        assert result["data"]["format"] == "wav"
        assert os.path.exists(output_path)

    def test_video_to_audio_file_not_found(self):
        """测试文件不存在的情况"""
        result = video_to_audio("nonexistent_video.mp4")

        assert result["success"] is False
        assert result["error_code"] == "FILE_NOT_FOUND"
        assert "不存在" in result["error"]

    def test_video_to_audio_invalid_format(self, test_video_path):
        """测试不支持的音频格式"""
        if not os.path.exists(test_video_path):
            pytest.skip(f"测试视频文件不存在: {test_video_path}")

        result = video_to_audio(test_video_path, audio_format="xyz")

        assert result["success"] is False
        assert result["error_code"] == "INVALID_FORMAT"
        assert "supported_formats" in result

    def test_video_file_info(self, test_video_path):
        """测试能够正确提取视频信息"""
        if not os.path.exists(test_video_path):
            pytest.skip(f"测试视频文件不存在: {test_video_path}")

        result = video_to_audio(test_video_path)

        assert result["success"] is True
        data = result["data"]
        assert "duration" in data
        assert "sample_rate" in data
        assert data["input_file"] == test_video_path

