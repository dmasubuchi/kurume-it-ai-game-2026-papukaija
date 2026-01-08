"""
OutGameモジュール

ゲーム外メニュー（SAVE管理、README表示など）
"""

from src.outgame.save_manager import SaveManager
from src.outgame.menu import OutGameMenu

__all__ = ["SaveManager", "OutGameMenu"]
