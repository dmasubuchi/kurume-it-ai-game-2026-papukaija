# Step 06: DSLパーサー（構文解析器）

## 学習目標

- 構文解析（パージング）の概念を理解する
- AST（抽象構文木）の構造を学ぶ
- 再帰下降パーサーの実装を学ぶ

## 概要

パーサーは、トークンを「意味のある構造」に変換します。
これはインタプリタの2番目のステップです。

```
入力: [MOVE, IDENTIFIER("player"), NUMBER(5), NUMBER(3)]
出力: MoveCommand(target="player", x=5, y=3)
```

## 仕様

`openspec/specs/dsl/parser/spec.md` を参照

## 実装ファイル

- `src/dsl/parser.py` - パーサー実装

## 成果物

1. `src/dsl/parser.py`
2. `examples/step_06_parser/main.py` - 動作例

## 受け入れ条件

- [ ] ASTNodeの各種類が定義されている
- [ ] `parse()` がASTノードのリストを返す
- [ ] 構文エラーでプログラムが落ちない
- [ ] 複数コマンドをパースできる
- [ ] `python examples/step_06_parser/main.py` が動作する

## DSL構文

```
move <entity> <x> <y>
spawn <type> <x> <y>
destroy <entity>
set <entity>.<property> <value>
if <condition> then <action>
```

## コード例

```python
class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0

    def current_token(self) -> Token:
        return self.tokens[self.pos]

    def consume(self, expected: TokenType) -> Token:
        token = self.current_token()
        if token.type != expected:
            raise ParseError(f"Expected {expected}, got {token.type}")
        self.pos += 1
        return token

    def parse_move(self) -> MoveCommand:
        self.consume(TokenType.MOVE)
        target = self.consume(TokenType.IDENTIFIER).value
        x = int(self.consume(TokenType.NUMBER).value)
        y = int(self.consume(TokenType.NUMBER).value)
        return MoveCommand(target=target, x=x, y=y)
```

## 次のステップ

Step 07 以降では、インタプリタの実装とアルゴリズムの追加を行います。
MVP（Step 00〜06）が完成です！
