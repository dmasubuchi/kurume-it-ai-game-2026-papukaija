"""
ゲームループ - ゲームの心臓部

ターン制のゲームループを提供します。
1入力 = 1更新 = 1描画 のサイクルを繰り返します。
"""

from typing import Callable, TypeVar

# 汎用的なState型
T = TypeVar("T")


def run_game_loop(
    initial_state: T,
    get_input: Callable[[], str],
    update: Callable[[T, str], T],
    render: Callable[[T], str],
    output: Callable[[str], None],
    quit_commands: tuple[str, ...] = ("quit", "exit", "q"),
) -> T:
    """
    ターン制ゲームループを実行する。

    Args:
        initial_state: ゲームの初期状態
        get_input: 入力を取得する関数
        update: 状態を更新する関数（新しい状態を返す）
        render: 状態を文字列に変換する関数（副作用なし）
        output: 文字列を出力する関数
        quit_commands: ループ終了コマンド

    Returns:
        最終的なゲーム状態
    """
    state = initial_state

    while True:
        # 1. 描画（render は副作用なし）
        screen = render(state)
        output(screen)

        # 2. 入力取得
        cmd = get_input()

        # 空入力は無視
        if not cmd.strip():
            continue

        # 終了コマンドチェック
        if cmd.lower() in quit_commands:
            break

        # 3. 状態更新（update は新しい状態を返す）
        state = update(state, cmd)

    return state


def run_game_loop_with_logging(
    initial_state: T,
    get_input: Callable[[], str],
    update: Callable[[T, str], T],
    render: Callable[[T], str],
    output: Callable[[str], None],
    log: Callable[[str], None],
    quit_commands: tuple[str, ...] = ("quit", "exit", "q"),
) -> T:
    """
    ログ付きターン制ゲームループを実行する。

    Args:
        initial_state: ゲームの初期状態
        get_input: 入力を取得する関数
        update: 状態を更新する関数
        render: 状態を文字列に変換する関数
        output: 文字列を出力する関数
        log: ログ出力関数
        quit_commands: ループ終了コマンド

    Returns:
        最終的なゲーム状態
    """
    state = initial_state
    turn = 0

    log(f"[GAME] Started. Initial state: {state}")

    while True:
        turn += 1
        log(f"[TURN {turn}] Rendering...")

        # 1. 描画
        screen = render(state)
        output(screen)

        # 2. 入力取得
        log(f"[TURN {turn}] Waiting for input...")
        cmd = get_input()
        log(f"[TURN {turn}] Input: '{cmd}'")

        # 空入力は無視
        if not cmd.strip():
            log(f"[TURN {turn}] Empty input, skipping...")
            turn -= 1  # ターンカウントを戻す
            continue

        # 終了コマンドチェック
        if cmd.lower() in quit_commands:
            log(f"[GAME] Quit command received: '{cmd}'")
            break

        # 3. 状態更新
        old_state = state
        state = update(state, cmd)
        log(f"[TURN {turn}] State updated: {old_state} -> {state}")

    log(f"[GAME] Ended after {turn} turns. Final state: {state}")
    return state
