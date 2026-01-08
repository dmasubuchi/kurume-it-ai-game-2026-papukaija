#!/usr/bin/env python3
"""
Step 02: State管理の動作例

不変（immutable）な状態管理を体験します。
プレイヤーを移動させるシンプルなゲームです。
"""

import sys

# src をインポートパスに追加
sys.path.insert(0, str(__file__).replace("/examples/step_02_state/main.py", ""))

from src.core.game_loop import run_game_loop
from src.core.state import GameState, create_initial_state


def get_input() -> str:
    """標準入力からコマンドを取得"""
    try:
        return input("> ").strip()
    except EOFError:
        return "quit"


def update(state: GameState, cmd: str) -> GameState:
    """
    状態を更新する（新しい状態を返す）

    コマンド:
    - w/up: 上に移動
    - s/down: 下に移動
    - a/left: 左に移動
    - d/right: 右に移動
    """
    # 移動方向のマッピング
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
        new_state = new_state.add_log(f"Moved to ({new_state.player.pos.x}, {new_state.player.pos.y})")
        return new_state
    else:
        return state.add_log(f"Unknown command: {cmd}")


def render(state: GameState) -> str:
    """
    状態を文字列に変換する（副作用なし！printしない！）
    """
    lines = []

    # ヘッダー
    lines.append("=== State Management Demo ===")
    lines.append(f"Turn: {state.turn}  Score: {state.score}")
    lines.append("")

    # マップ描画
    for y in range(state.map_height):
        row = ""
        for x in range(state.map_width):
            if x == state.player.pos.x and y == state.player.pos.y:
                row += "@"  # プレイヤー
            else:
                row += "."  # 空きマス
        lines.append(row)

    lines.append("")

    # ログ
    if state.log_messages:
        lines.append("Log:")
        for msg in state.log_messages:
            lines.append(f"  {msg}")
        lines.append("")

    # コマンドヘルプ
    lines.append("Commands: w/a/s/d or up/down/left/right, quit")
    lines.append("")

    return "\n".join(lines)


def output(screen: str) -> None:
    """画面に出力する"""
    print(screen)


def main() -> None:
    """メインエントリーポイント"""
    print("Step 02: State管理の動作例")
    print("'@' がプレイヤーです。移動してみましょう。")
    print("'quit' で終了します")
    print()

    initial_state = create_initial_state(
        map_width=20,
        map_height=10,
        player_start=(10, 5),
    )

    final_state = run_game_loop(
        initial_state=initial_state,
        get_input=get_input,
        update=update,
        render=render,
        output=output,
    )

    print(f"ゲーム終了。{final_state.turn} ターンプレイしました。")


if __name__ == "__main__":
    main()
