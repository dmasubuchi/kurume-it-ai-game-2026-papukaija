#!/usr/bin/env python3
"""
Step 04: TextGridレンダラーの動作例

TextGridを使ったグリッド描画を体験します。
副作用なしのレンダリングを実践します。
"""

import sys
from dataclasses import replace

# src をインポートパスに追加
sys.path.insert(0, str(__file__).replace("/examples/step_04_renderer/main.py", ""))

from src.core.game_loop import run_game_loop
from src.core.state import GameState, Entity, Position, create_initial_state
from src.core.io import get_input, output
from src.core.renderer import TextGrid, add_border, create_game_renderer


def demo_textgrid() -> None:
    """TextGridの基本的な使い方をデモ"""
    print("=== TextGrid Demo ===")
    print()

    # グリッドを作成
    grid = TextGrid(width=15, height=8, fill=".")

    # 文字を配置
    grid.set(7, 4, "@")  # プレイヤー
    grid.set(3, 2, "E")  # 敵1
    grid.set(11, 5, "E")  # 敵2
    grid.set(6, 1, "!")  # アイテム

    # テキストを描画
    grid.draw_text(1, 0, "GAME")

    print("Basic grid:")
    print(grid.render())
    print()

    # 枠を追加
    bordered = add_border(grid)
    print("With border:")
    print(bordered.render())
    print()


def demo_game_renderer() -> None:
    """ゲームレンダラーのデモ"""
    print("=== Game Renderer Demo ===")
    print()

    # 初期状態を作成
    state = create_initial_state(map_width=15, map_height=8, player_start=(7, 4))

    # 敵を追加
    enemies = (
        Entity(id="enemy", name="Goblin", pos=Position(3, 2)),
        Entity(id="enemy", name="Orc", pos=Position(11, 5)),
    )
    state = state.replace(entities=enemies)

    # レンダラーを作成
    render = create_game_renderer(show_status=True, show_log=True)

    # 状態を描画
    print("Initial state:")
    print(render(state))

    # プレイヤーを移動
    state = state.move_player(1, 0).next_turn().add_log("Moved right")
    state = state.move_player(1, 0).next_turn().add_log("Moved right again")

    print("After moving:")
    print(render(state))


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
        new_state = state.move_player(dx, dy).next_turn()
        return new_state.add_log(f"Moved to ({new_state.player.pos.x}, {new_state.player.pos.y})")
    return state


def demo_interactive() -> None:
    """インタラクティブなゲームのデモ"""
    print("=== Interactive Game ===")
    print("Controls: w/a/s/d or up/down/left/right")
    print("Type 'quit' to exit")
    print()

    # 初期状態
    state = create_initial_state(map_width=20, map_height=10, player_start=(10, 5))

    # 敵を配置
    enemies = (
        Entity(id="enemy", name="Goblin A", pos=Position(5, 3)),
        Entity(id="enemy", name="Goblin B", pos=Position(15, 7)),
        Entity(id="item", name="Potion", pos=Position(3, 8)),
    )
    state = state.replace(entities=enemies)

    # カスタムレンダラー
    render = create_game_renderer(
        char_mapping={
            "player": "@",
            "enemy": "G",
            "item": "!",
        },
        show_status=True,
        show_log=True,
    )

    # ゲームループ実行
    final_state = run_game_loop(
        initial_state=state,
        get_input=lambda: get_input("Command> "),
        update=update,
        render=render,
        output=output,
    )

    print(f"Game ended after {final_state.turn} turns.")


def main() -> None:
    """メインエントリーポイント"""
    print("Step 04: TextGridレンダラーの動作例")
    print()

    print("1. TextGrid Demo（基本機能）")
    print("2. Game Renderer Demo（ゲーム描画）")
    print("3. Interactive Game（実際にプレイ）")
    print()

    choice = input("Select mode (1/2/3): ").strip()

    if choice == "1":
        demo_textgrid()
    elif choice == "2":
        demo_game_renderer()
    else:
        demo_interactive()


if __name__ == "__main__":
    main()
