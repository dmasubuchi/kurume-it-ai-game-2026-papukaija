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


def on_play(slot: SlotName, slot_path: Path) -> None:
    """
    ゲーム開始時のコールバック

    ここでInGameを起動する。
    現在はプレースホルダー実装。
    """
    print(f"\n=== SAVE_{slot} を読み込みました ===")
    print(f"Path: {slot_path}")
    print()
    print("InGame はまだ実装されていません。")
    print("examples/ の各ステップを試してみてください：")
    print()
    print("  python examples/step_00_hello/main.py")
    print("  python examples/step_01_game_loop/main.py")
    print("  python examples/step_02_state/main.py")
    print("  python examples/step_03_io/main.py")
    print("  python examples/step_04_renderer/main.py")
    print("  python examples/step_05_lexer/main.py")
    print("  python examples/step_06_parser/main.py")
    print()
    input("Press Enter to return to menu...")


def main() -> None:
    """メインエントリーポイント"""
    print()
    print("Starting AI × Game Development Tutorial...")
    print()

    menu = OutGameMenu(on_play=on_play)
    menu.run()


if __name__ == "__main__":
    main()
