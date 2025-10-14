"""
预制件核心逻辑模块

这是一个示例预制件，展示了如何创建可被 AI 调用的函数。
所有暴露给 AI 的函数都必须在此文件中定义。

你可以在 src/ 目录下创建多个模块文件，然后在此处导入使用。
"""

import os
from pathlib import Path
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


def video_to_audio(video_path: str, output_path: str = None, audio_format: str = "mp3") -> dict:
    """
    将视频文件转换为音频文件

    Args:
        video_path: 输入视频文件路径
        output_path: 输出音频文件路径（可选，默认为视频同目录下的同名音频文件）
        audio_format: 音频格式 ("mp3", "wav", "aac")

    Returns:
        包含转换结果的字典
    """
    try:
        from moviepy import VideoFileClip

        # 验证视频文件存在
        if not os.path.exists(video_path):
            return {
                "success": False,
                "error": f"视频文件不存在: {video_path}",
                "error_code": "FILE_NOT_FOUND"
            }

        # 生成输出路径
        if output_path is None:
            video_file = Path(video_path)
            output_path = str(video_file.with_suffix(f'.{audio_format}'))

        # 验证音频格式
        supported_formats = ["mp3", "wav", "aac", "flac", "ogg"]
        if audio_format.lower() not in supported_formats:
            return {
                "success": False,
                "error": f"不支持的音频格式: {audio_format}",
                "error_code": "INVALID_FORMAT",
                "supported_formats": supported_formats
            }

        # 转换视频到音频
        video_clip = VideoFileClip(video_path)
        audio_clip = video_clip.audio

        if audio_clip is None:
            video_clip.close()
            return {
                "success": False,
                "error": "视频文件不包含音频轨道",
                "error_code": "NO_AUDIO_TRACK"
            }

        # 导出音频
        audio_clip.write_audiofile(output_path)

        # 获取音频信息
        duration = audio_clip.duration
        fps = audio_clip.fps

        # 清理资源
        audio_clip.close()
        video_clip.close()

        return {
            "success": True,
            "data": {
                "input_file": video_path,
                "output_file": output_path,
                "format": audio_format,
                "duration": duration,
                "sample_rate": fps
            }
        }

    except ImportError:
        return {
            "success": False,
            "error": "moviepy 库未安装",
            "error_code": "DEPENDENCY_MISSING"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_code": "CONVERSION_FAILED"
        }
