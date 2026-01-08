#!/usr/bin/env python3
"""
Step 06: DSLパーサーの動作例

トークンをAST（抽象構文木）に変換する様子を体験します。
"""

import sys

# src をインポートパスに追加
sys.path.insert(0, str(__file__).replace("/examples/step_06_parser/main.py", ""))

from src.dsl.parser import (
    parse,
    parse_with_errors,
    MoveCommand,
    SpawnCommand,
    DestroyCommand,
    SetCommand,
    IfStatement,
)


def demo_basic() -> None:
    """基本的なパースのデモ"""
    print("=== Basic Parsing ===")
    print()

    source = "move player 5 3"
    print(f"Source: {source!r}")
    print()

    program = parse(source)
    print("AST:")
    for stmt in program.statements:
        print(f"  {stmt}")
    print()


def demo_multiple() -> None:
    """複数コマンドのパース"""
    print("=== Multiple Commands ===")
    print()

    source = """
move player 10 10
spawn enemy 5 5
spawn enemy 15 5
destroy enemy
set player.hp 100
"""
    print("Source:")
    print(source)

    program = parse(source)
    print("AST:")
    for i, stmt in enumerate(program.statements):
        print(f"  {i+1}. {stmt}")
    print()


def demo_conditional() -> None:
    """条件文のパース"""
    print("=== Conditional Statements ===")
    print()

    source = "if player.hp < 50 then set player.state fleeing"
    print(f"Source: {source!r}")
    print()

    program = parse(source)
    print("AST:")
    for stmt in program.statements:
        print(f"  {stmt}")
        if isinstance(stmt, IfStatement):
            print(f"    Condition: {stmt.condition}")
            print(f"    Then: {stmt.then_action}")
    print()


def demo_errors() -> None:
    """エラー処理のデモ"""
    print("=== Error Handling ===")
    print()

    source = """
move player 5 3
spawn 10 10
move enemy 15 15
"""
    print("Source:")
    print(source)

    program, errors = parse_with_errors(source)

    print("Parsed statements (valid ones):")
    for stmt in program.statements:
        if not isinstance(stmt, type(None)):
            print(f"  {stmt}")

    if errors:
        print()
        print("Errors:")
        for error in errors:
            print(f"  Line {error.line}, Col {error.column}: {error.message}")
    print()


def demo_interactive() -> None:
    """インタラクティブなパース"""
    print("=== Interactive Parser ===")
    print("Enter DSL code to parse (empty line to quit)")
    print("Available commands: move, spawn, destroy, set, if...then")
    print()

    while True:
        try:
            source = input("DSL> ").strip()
        except EOFError:
            break

        if not source:
            break

        program, errors = parse_with_errors(source)

        print("AST:")
        for stmt in program.statements:
            print(f"  {stmt}")

        if errors:
            print("Errors:")
            for error in errors:
                print(f"  {error.message}")

        print()


def demo_complete() -> None:
    """完全なゲームシナリオのパース"""
    print("=== Complete Game Scenario ===")
    print()

    source = """
# ゲーム初期化
spawn player 10 10
spawn enemy 5 5 "Goblin"
spawn enemy 15 5 "Orc"

# プレイヤーの移動
move player 12 10

# 敵との遭遇判定
if player.hp < 50 then set player.state fleeing

# 敵の削除
destroy enemy
"""
    print("Source:")
    print(source)

    program, errors = parse_with_errors(source)

    print("Parsed AST:")
    print("-" * 40)
    for i, stmt in enumerate(program.statements):
        print(f"{i+1:2}. {type(stmt).__name__}")
        if isinstance(stmt, MoveCommand):
            print(f"    target={stmt.target}, x={stmt.x}, y={stmt.y}")
        elif isinstance(stmt, SpawnCommand):
            print(f"    type={stmt.entity_type}, pos=({stmt.x},{stmt.y}), name={stmt.name!r}")
        elif isinstance(stmt, DestroyCommand):
            print(f"    target={stmt.target}")
        elif isinstance(stmt, SetCommand):
            print(f"    {stmt.target}.{stmt.property} = {stmt.value}")
        elif isinstance(stmt, IfStatement):
            print(f"    condition: {stmt.condition}")
            print(f"    then: {stmt.then_action}")

    if errors:
        print()
        print("Errors:")
        for error in errors:
            print(f"  {error.message}")

    print()


def main() -> None:
    """メインエントリーポイント"""
    print("Step 06: DSLパーサーの動作例")
    print()

    print("1. Basic Demo（基本パース）")
    print("2. Multiple Commands（複数コマンド）")
    print("3. Conditional（条件文）")
    print("4. Error Demo（エラー処理）")
    print("5. Complete Scenario（完全シナリオ）")
    print("6. Interactive（インタラクティブ）")
    print()

    choice = input("Select mode (1-6): ").strip()

    if choice == "1":
        demo_basic()
    elif choice == "2":
        demo_multiple()
    elif choice == "3":
        demo_conditional()
    elif choice == "4":
        demo_errors()
    elif choice == "5":
        demo_complete()
    else:
        demo_interactive()


if __name__ == "__main__":
    main()
