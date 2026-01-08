#!/usr/bin/env python3
"""
Step 01: ゲームループの動作例

最小限のターン制ゲームループを体験します。
カウンターを増減させる簡単なゲームです。
"""

import sys
from dataclasses import dataclass

# src をインポートパスに追加
sys.path.insert(0, str(__file__).replace("/examples/step_01_game_loop/main.py", ""))

from src.core.game_loop import run_game_loop


@dataclass(frozen=True)
class CounterState:
    """カウンターの状態（不変）"""

    count: int = 0


def get_input() -> str:
    """標準入力からコマンドを取得"""
    try:
        return input("> ").strip()
    except EOFError:
        return "quit"


def update(state: CounterState, cmd: str) -> CounterState:
    """
    状態を更新する（新しい状態を返す）

    コマンド:
    - "up" または "+": カウントを増やす
    - "down" または "-": カウントを減らす
    - "reset": カウントを0にする
    """
    if cmd in ("up", "+"):
        return CounterState(count=state.count + 1)
    elif cmd in ("down", "-"):
        return CounterState(count=state.count - 1)
    elif cmd == "reset":
        return CounterState(count=0)
    else:
        # 不明なコマンドは無視（状態を変更しない）
        return state


def render(state: CounterState) -> str:
    """
    状態を文字列に変換する（副作用なし！printしない！）
    """
    lines = [
        "",
        "=== Counter Game ===",
        f"Count: {state.count}",
        "",
        "Commands: up(+), down(-), reset, quit",
        "",
    ]
    return "\n".join(lines)


def output(screen: str) -> None:
    """画面に出力する（副作用はここだけ）"""
    print(screen)


def main() -> None:
    """メインエントリーポイント"""
    print("Step 01: ゲームループの動作例")
    print("'quit' で終了します")
    print()

    initial_state = CounterState(count=0)

    final_state = run_game_loop(
        initial_state=initial_state,
        get_input=get_input,
        update=update,
        render=render,
        output=output,
    )

    print(f"ゲーム終了。最終カウント: {final_state.count}")


if __name__ == "__main__":
    main()
