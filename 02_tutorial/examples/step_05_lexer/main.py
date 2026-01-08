#!/usr/bin/env python3
"""
Step 05: DSLレクサーの動作例

DSLのテキストをトークンに分解する様子を体験します。
"""

import sys

# src をインポートパスに追加
sys.path.insert(0, str(__file__).replace("/examples/step_05_lexer/main.py", ""))

from src.dsl.lexer import tokenize, tokenize_with_errors, TokenType


def demo_basic() -> None:
    """基本的なトークン化のデモ"""
    print("=== Basic Tokenization ===")
    print()

    source = "move player 5 3"
    print(f"Source: {source!r}")
    print()

    tokens = tokenize(source)
    print("Tokens:")
    for token in tokens:
        print(f"  {token}")
    print()


def demo_complex() -> None:
    """複雑なDSLコードのトークン化"""
    print("=== Complex DSL ===")
    print()

    source = """
# ゲームの初期化
spawn player 10 10
spawn enemy 5 5

# プレイヤーの移動
move player 12 10

# 条件分岐
if player.hp < 50 then
    set player.state "fleeing"
"""
    print("Source:")
    print(source)
    print()

    tokens = tokenize(source)
    print("Tokens (excluding NEWLINE and COMMENT):")
    for token in tokens:
        if token.type not in (TokenType.NEWLINE, TokenType.COMMENT, TokenType.EOF):
            print(f"  Line {token.line}, Col {token.column}: {token}")
    print()


def demo_errors() -> None:
    """エラー処理のデモ"""
    print("=== Error Handling ===")
    print()

    source = "move player $ 5 @ 3"
    print(f"Source: {source!r}")
    print()

    tokens, errors = tokenize_with_errors(source)

    print("Tokens (エラーがあっても他のトークンは取得できる):")
    for token in tokens:
        if token.type != TokenType.EOF:
            print(f"  {token}")
    print()

    if errors:
        print("Errors:")
        for error in errors:
            print(f"  Line {error.line}, Col {error.column}: {error.message}")
    print()


def demo_interactive() -> None:
    """インタラクティブなトークン化"""
    print("=== Interactive Lexer ===")
    print("Enter DSL code to tokenize (empty line to quit)")
    print()

    while True:
        try:
            source = input("DSL> ").strip()
        except EOFError:
            break

        if not source:
            break

        tokens, errors = tokenize_with_errors(source)

        print("Tokens:")
        for token in tokens:
            if token.type != TokenType.EOF:
                print(f"  {token}")

        if errors:
            print("Errors:")
            for error in errors:
                print(f"  {error.message}")

        print()


def main() -> None:
    """メインエントリーポイント"""
    print("Step 05: DSLレクサーの動作例")
    print()

    print("1. Basic Demo（基本的なトークン化）")
    print("2. Complex Demo（複雑なDSL）")
    print("3. Error Demo（エラー処理）")
    print("4. Interactive（インタラクティブ）")
    print()

    choice = input("Select mode (1/2/3/4): ").strip()

    if choice == "1":
        demo_basic()
    elif choice == "2":
        demo_complex()
    elif choice == "3":
        demo_errors()
    else:
        demo_interactive()


if __name__ == "__main__":
    main()
