"""
预制件主模块

导出所有可被 AI 调用的函数
"""

from .main import analyze_dataset, video_to_audio

__all__ = [
    'analyze_dataset',
    'video_to_audio'
]
