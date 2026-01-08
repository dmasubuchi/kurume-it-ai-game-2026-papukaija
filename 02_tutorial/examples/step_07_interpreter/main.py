#!/usr/bin/env python3
"""
Step 07: DSLインタプリタの動作例

DSLコマンドを実際に実行する様子を体験します。
"""

import sys
from pathlib import Path

# src をインポートパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.state import create_initial_state, GameState
from src.core.renderer import create_game_renderer
from src.dsl.interpreter import interpret, execute_command, Interpreter
from src.dsl.parser import parse


def demo_basic() -> None:
    """基本的なコマンド実行のデモ"""
    print("=== Basic Command Execution ===")
    print()

    state = create_initial_state()
    print(f"Initial player position: ({state.player.pos.x}, {state.player.pos.y})")

    # move コマンド
    result = interpret("move player 10 5", state)
    state = result.state
    print(f"After 'move player 10 5': ({state.player.pos.x}, {state.player.pos.y})")

    # spawn コマンド
    result = interpret("spawn enemy 15 5", state)
    state = result.state
    print(f"After 'spawn enemy 15 5': {len(state.entities)} entities")

    # destroy コマンド
    result = interpret("destroy enemy", state)
    state = result.state
    print(f"After 'destroy enemy': {len(state.entities)} entities, score={state.score}")

    print()


def demo_expressions() -> None:
    """式評価のデモ"""
    print("=== Expression Evaluation ===")
    print()

    state = create_initial_state()
    interpreter = Interpreter()

    # プロパティアクセス
    program = parse("player.hp")
    expr = program.statements[0] if program.statements else None
    if expr:
        # 式として評価（パーサーはIdentifierとして解釈）
        pass

    # 直接式評価をテスト
    from src.dsl.parser import PropertyAccess, BinaryOp, NumberLiteral

    # player.hp を評価
    hp_expr = PropertyAccess(object="player", property="hp")
    hp_value = interpreter.evaluate(hp_expr, state)
    print(f"player.hp = {hp_value}")

    # player.x を評価
    x_expr = PropertyAccess(object="player", property="x")
    x_value = interpreter.evaluate(x_expr, state)
    print(f"player.x = {x_value}")

    # player.hp < 50 を評価
    condition = BinaryOp(
        left=PropertyAccess(object="player", property="hp"),
        op="<",
        right=NumberLiteral(value=50),
    )
    result = interpreter.evaluate(condition, state)
    print(f"player.hp < 50 = {result}")

    # player.hp > 50 を評価
    condition2 = BinaryOp(
        left=PropertyAccess(object="player", property="hp"),
        op=">",
        right=NumberLiteral(value=50),
    )
    result2 = interpreter.evaluate(condition2, state)
    print(f"player.hp > 50 = {result2}")

    print()


def demo_conditional() -> None:
    """条件文の実行デモ"""
    print("=== Conditional Execution ===")
    print()

    state = create_initial_state()

    # if player.hp > 50 then move player 10 10
    source = "if player.hp > 50 then move player 10 10"
    print(f"Command: {source}")
    result = interpret(source, state)
    state = result.state
    print(f"Player position: ({state.player.pos.x}, {state.player.pos.y})")
    print(f"Condition was True, so player moved")

    print()

    # Reset and test false condition
    state = create_initial_state()
    source = "if player.hp < 50 then move player 15 15"
    print(f"Command: {source}")
    result = interpret(source, state)
    state = result.state
    print(f"Player position: ({state.player.pos.x}, {state.player.pos.y})")
    print(f"Condition was False, so player did not move")

    print()


def demo_program() -> None:
    """複数コマンドの実行デモ"""
    print("=== Program Execution ===")
    print()

    state = create_initial_state()
    render = create_game_renderer()

    source = """
spawn enemy 15 5
spawn enemy 10 8
move player 8 5
"""
    print("Program:")
    print(source)

    result = interpret(source, state)
    state = result.state

    print("After execution:")
    print(f"  Player: ({state.player.pos.x}, {state.player.pos.y})")
    print(f"  Entities: {len(state.entities)}")
    for e in state.entities:
        print(f"    - {e.name} at ({e.pos.x}, {e.pos.y})")

    print()
    print("Rendered:")
    print(render(state))


def demo_interactive() -> None:
    """インタラクティブな実行"""
    print("=== Interactive Interpreter ===")
    print("Enter DSL commands (empty line to quit)")
    print("Available: move, spawn, destroy, set, if...then")
    print()

    state = create_initial_state()
    render = create_game_renderer()

    while True:
        print(render(state))

        try:
            source = input("DSL> ").strip()
        except EOFError:
            break

        if not source:
            break

        result = interpret(source, state)
        state = result.state

        if result.errors:
            for error in result.errors:
                print(f"Error: {error.message}")

        if result.logs:
            for log in result.logs:
                print(f"  {log}")

        print()

    print("Goodbye!")


def main() -> None:
    """メインエントリーポイント"""
    print("Step 07: DSLインタプリタの動作例")
    print()

    print("1. Basic Demo（基本コマンド）")
    print("2. Expressions（式評価）")
    print("3. Conditional（条件文）")
    print("4. Program（複数コマンド）")
    print("5. Interactive（インタラクティブ）")
    print()

    choice = input("Select mode (1-5): ").strip()

    if choice == "1":
        demo_basic()
    elif choice == "2":
        demo_expressions()
    elif choice == "3":
        demo_conditional()
    elif choice == "4":
        demo_program()
    else:
        demo_interactive()


if __name__ == "__main__":
    main()
