#!/usr/bin/env python3
"""
Step 03: I/O層の動作例

I/O層の分離を体験します。
モック入力を使ったテストも行います。
"""

import sys

# src をインポートパスに追加
sys.path.insert(0, str(__file__).replace("/examples/step_03_io/main.py", ""))

from src.core.game_loop import run_game_loop
from src.core.state import GameState, create_initial_state
from src.core.io import (
    get_input,
    output,
    create_mock_input,
    create_mock_output,
    clear_screen,
)


def update(state: GameState, cmd: str) -> GameState:
    """状態を更新する"""
    moves = {
        "w": (0, -1),
        "up": (0, -1),
        "s": (0, 1),
        "down": (0, 1),
        "a": (-1, 0),
        "left": (-1, 0),
        "d": (1, 0),
        "right": (1, 0),
    }

    if cmd.lower() in moves:
        dx, dy = moves[cmd.lower()]
        new_state = state.move_player(dx, dy)
        new_state = new_state.next_turn()
        return new_state.add_log(f"Moved to ({new_state.player.pos.x}, {new_state.player.pos.y})")
    else:
        return state.add_log(f"Unknown command: {cmd}")


def render(state: GameState) -> str:
    """状態を文字列に変換する（副作用なし）"""
    lines = []
    lines.append(f"Turn: {state.turn} | Player: ({state.player.pos.x}, {state.player.pos.y})")
    lines.append("")

    # 簡易マップ（小さめ）
    for y in range(state.map_height):
        row = ""
        for x in range(state.map_width):
            if x == state.player.pos.x and y == state.player.pos.y:
                row += "@"
            else:
                row += "."
        lines.append(row)

    lines.append("")
    lines.append("Commands: w/a/s/d, quit")
    lines.append("")
    return "\n".join(lines)


def demo_interactive() -> None:
    """インタラクティブモードのデモ"""
    print("=== Interactive Mode ===")
    print("実際に入力してゲームをプレイします。")
    print("'quit' で終了します")
    print()

    initial_state = create_initial_state(map_width=10, map_height=5, player_start=(5, 2))

    final_state = run_game_loop(
        initial_state=initial_state,
        get_input=lambda: get_input("> "),
        update=update,
        render=render,
        output=output,
    )

    print(f"ゲーム終了。{final_state.turn} ターンプレイしました。")


def demo_mock() -> None:
    """モック入力を使ったテストのデモ"""
    print("=== Mock Input Test ===")
    print("プログラムで入力を自動化します。")
    print()

    # モック入力：右→右→下→終了
    mock_input = create_mock_input(["d", "d", "s", "quit"])
    mock_output, captured = create_mock_output()

    initial_state = create_initial_state(map_width=10, map_height=5, player_start=(2, 2))

    final_state = run_game_loop(
        initial_state=initial_state,
        get_input=mock_input,
        update=update,
        render=render,
        output=mock_output,  # 画面には出力しない
    )

    # 結果を表示
    print(f"Initial position: (2, 2)")
    print(f"Commands: d, d, s, quit")
    print(f"Final position: ({final_state.player.pos.x}, {final_state.player.pos.y})")
    print(f"Expected: (4, 3)")
    print()

    # テスト結果
    if final_state.player.pos.x == 4 and final_state.player.pos.y == 3:
        print("TEST PASSED: Position is correct!")
    else:
        print("TEST FAILED: Position is incorrect!")

    print()
    print(f"Captured {len(captured)} screen outputs")


def main() -> None:
    """メインエントリーポイント"""
    print("Step 03: I/O層の動作例")
    print()

    # モードを選択
    print("1. Interactive Mode（実際にプレイ）")
    print("2. Mock Test Mode（自動テスト）")
    print()

    choice = input("Select mode (1/2): ").strip()

    if choice == "1":
        demo_interactive()
    else:
        demo_mock()


if __name__ == "__main__":
    main()
