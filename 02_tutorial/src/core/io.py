"""
I/O層 - 副作用の境界

このモジュールはゲームの入出力を担当します。
print, input などの副作用を持つ操作はここにのみ存在します。
他のモジュール（render, update等）は純粋関数として保たれます。
"""

import os
import sys
from typing import Callable, Iterator


# ============================================
# 入力関数
# ============================================


def get_input(prompt: str = "> ") -> str:
    """
    標準入力からコマンドを取得する

    Args:
        prompt: 入力プロンプト

    Returns:
        入力された文字列（前後の空白を除去）
    """
    try:
        return input(prompt).strip()
    except EOFError:
        return "quit"
    except KeyboardInterrupt:
        print()  # 改行
        return "quit"


def create_mock_input(commands: list[str]) -> Callable[[], str]:
    """
    テスト用のモック入力関数を作成する

    Args:
        commands: 順番に返すコマンドのリスト

    Returns:
        モック入力関数

    Example:
        >>> mock = create_mock_input(["up", "down", "quit"])
        >>> mock()
        'up'
        >>> mock()
        'down'
        >>> mock()
        'quit'
    """
    iterator: Iterator[str] = iter(commands)

    def mock_input() -> str:
        try:
            return next(iterator)
        except StopIteration:
            return "quit"

    return mock_input


def create_interactive_input(
    prompt: str = "> ",
    history: list[str] | None = None,
) -> Callable[[], str]:
    """
    履歴機能付きの入力関数を作成する

    Args:
        prompt: 入力プロンプト
        history: 入力履歴を保存するリスト（Noneの場合は保存しない）

    Returns:
        入力関数
    """

    def interactive_input() -> str:
        cmd = get_input(prompt)
        if history is not None and cmd and cmd != "quit":
            history.append(cmd)
        return cmd

    return interactive_input


# ============================================
# 出力関数
# ============================================


def output(text: str) -> None:
    """
    標準出力にテキストを表示する

    Args:
        text: 表示するテキスト
    """
    print(text)


def output_error(text: str) -> None:
    """
    標準エラー出力にテキストを表示する

    Args:
        text: 表示するテキスト
    """
    print(text, file=sys.stderr)


def create_mock_output() -> tuple[Callable[[str], None], list[str]]:
    """
    テスト用のモック出力関数を作成する

    Returns:
        (モック出力関数, 出力を保存するリスト)

    Example:
        >>> mock_out, captured = create_mock_output()
        >>> mock_out("Hello")
        >>> mock_out("World")
        >>> captured
        ['Hello', 'World']
    """
    captured: list[str] = []

    def mock_output(text: str) -> None:
        captured.append(text)

    return mock_output, captured


# ============================================
# 画面制御
# ============================================


def clear_screen() -> None:
    """
    ターミナル画面をクリアする
    """
    # Windows
    if os.name == "nt":
        os.system("cls")
    # Unix/Linux/Mac
    else:
        # ANSI エスケープシーケンスを使用
        print("\033[2J\033[H", end="")


def move_cursor(x: int, y: int) -> None:
    """
    カーソルを指定位置に移動する

    Args:
        x: 列（0から始まる）
        y: 行（0から始まる）
    """
    # ANSI エスケープシーケンス（1から始まる）
    print(f"\033[{y+1};{x+1}H", end="")


def hide_cursor() -> None:
    """カーソルを非表示にする"""
    print("\033[?25l", end="")


def show_cursor() -> None:
    """カーソルを表示する"""
    print("\033[?25h", end="")


# ============================================
# ログ関数
# ============================================


def create_logger(
    prefix: str = "[LOG]",
    enabled: bool = True,
) -> Callable[[str], None]:
    """
    ロガー関数を作成する

    Args:
        prefix: ログメッセージの接頭辞
        enabled: ログ出力を有効にするかどうか

    Returns:
        ロガー関数
    """

    def log(message: str) -> None:
        if enabled:
            print(f"{prefix} {message}", file=sys.stderr)

    return log


# ============================================
# ユーティリティ
# ============================================


def confirm(prompt: str = "Continue? (y/n): ") -> bool:
    """
    確認プロンプトを表示する

    Args:
        prompt: 確認メッセージ

    Returns:
        y/yes なら True、それ以外は False
    """
    response = get_input(prompt)
    return response.lower() in ("y", "yes")
