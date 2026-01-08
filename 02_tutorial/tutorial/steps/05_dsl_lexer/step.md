# Step 05: DSLレクサー（字句解析器）

## 学習目標

- 字句解析（レキシング）の概念を理解する
- トークン化の実装を学ぶ
- DSL設計の基礎を学ぶ

## 概要

レクサーは、テキストを「トークン」に分解します。
これはインタプリタの最初のステップです。

```
入力: "move player 5 3"
出力: [MOVE, IDENTIFIER("player"), NUMBER(5), NUMBER(3)]
```

トークン化により：
- 空白を除去
- 数値を認識
- キーワードを識別
- 位置情報を付加

## 仕様

`openspec/specs/dsl/lexer/spec.md` を参照

## 実装ファイル

- `src/dsl/lexer.py` - レクサー実装

## 成果物

1. `src/dsl/lexer.py`
2. `examples/step_05_lexer/main.py` - 動作例

## 受け入れ条件

- [ ] TokenType列挙体が定義されている
- [ ] Tokenクラスが位置情報を持つ
- [ ] `tokenize()` がトークンリストを返す
- [ ] 不正な入力でエラーにならない
- [ ] `python examples/step_05_lexer/main.py` が動作する

## DSL構文（このチュートリアルで使用）

```
# コメント
move <entity> <x> <y>     # エンティティを移動
spawn <type> <x> <y>      # エンティティを生成
destroy <entity>          # エンティティを削除
if <condition> then <action>  # 条件分岐
```

## コード例

```python
def tokenize(source: str) -> list[Token]:
    tokens = []
    pos = 0
    line = 1
    column = 1

    while pos < len(source):
        char = source[pos]

        # 空白をスキップ
        if char.isspace():
            if char == '\n':
                tokens.append(Token(TokenType.NEWLINE, '\\n', line, column))
                line += 1
                column = 1
            else:
                column += 1
            pos += 1
            continue

        # 数値
        if char.isdigit():
            start = pos
            while pos < len(source) and source[pos].isdigit():
                pos += 1
            tokens.append(Token(TokenType.NUMBER, source[start:pos], line, column))
            column += pos - start
            continue

        # 識別子/キーワード
        if char.isalpha():
            ...
```

## 次のステップ

Step 06 ではパーサー（構文解析器）を実装します。
