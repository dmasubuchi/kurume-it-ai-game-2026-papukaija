# DSL Lexer Specification

## Overview

レクサー（字句解析器）は、テキストをトークンに分解します。
これはインタプリタの最初のステップです。

```
"move player 5 3" → [MOVE, PLAYER, 5, 3]
```

## Requirements

### Requirement: Token Types

基本的なトークン型を定義する。

```python
class TokenType(Enum):
    # キーワード
    MOVE = "move"
    SPAWN = "spawn"
    DESTROY = "destroy"
    IF = "if"
    THEN = "then"

    # リテラル
    NUMBER = "NUMBER"
    STRING = "STRING"
    IDENTIFIER = "IDENTIFIER"

    # 記号
    LPAREN = "("
    RPAREN = ")"
    COMMA = ","
    COLON = ":"

    # 特殊
    EOF = "EOF"
    NEWLINE = "NEWLINE"
```

### Requirement: Token Structure

トークンは位置情報を持つ。

```python
@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int
```

### Requirement: Lexer Function

文字列をトークンのリストに変換する。

```python
def tokenize(source: str) -> list[Token]:
    ...
```

#### Scenario: Simple command

```gherkin
Given source "move player 5 3"
When tokenize is called
Then 5 tokens are returned: [MOVE, IDENTIFIER("player"), NUMBER(5), NUMBER(3), EOF]
```

#### Scenario: Multiple lines

```gherkin
Given source:
  """
  move player 5 3
  spawn enemy 10 10
  """
When tokenize is called
Then tokens include NEWLINE between commands
```

### Requirement: Error Handling

不正な入力はスキップしてログに記録する（エラーで落ちない）。

#### Scenario: Unknown character

```gherkin
Given source "move player $ 5"
When tokenize is called
Then "$" is skipped
And a warning is logged
And other tokens are returned
```

## Non-Requirements

- Unicode識別子（ASCIIのみ）
- 文字列リテラルのエスケープ
