#!/usr/bin/env python3
"""
AI × Game Development Tutorial - Entry Point

久留米工業大学 2026年1月9日講義

このファイルがチュートリアルのエントリーポイントです。
OutGameメニューから開始し、SAVEスロットを選択してゲームを開始します。

Usage:
    python main.py
"""

import sys
from pathlib import Path

# srcをインポートパスに追加
sys.path.insert(0, str(Path(__file__).parent))

from src.outgame.menu import OutGameMenu
from src.outgame.save_manager import SlotName
from src.ingame.runner import run_game


def on_play(slot: SlotName, slot_path: Path) -> None:
    """
    ゲーム開始時のコールバック

    SAVEディレクトリ内のingame/game.pyを実行します。
    """
    run_game(slot_path)


def main() -> None:
    """メインエントリーポイント"""
    print()
    print("Starting AI × Game Development Tutorial...")
    print()

    menu = OutGameMenu(on_play=on_play)
    menu.run()


if __name__ == "__main__":
    main()
