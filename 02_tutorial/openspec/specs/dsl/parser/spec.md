# DSL Parser Specification

## Overview

パーサー（構文解析器）は、トークンをAST（抽象構文木）に変換します。
これはインタプリタの2番目のステップです。

```
Tokens: [MOVE, IDENTIFIER("player"), NUMBER(5), NUMBER(3)]
AST: MoveCommand(target="player", x=5, y=3)
```

## Requirements

### Requirement: AST Node Types

ASTノードの基本型を定義する。

```python
@dataclass
class ASTNode:
    """AST基底クラス"""
    pass

@dataclass
class MoveCommand(ASTNode):
    target: str
    x: int
    y: int

@dataclass
class SpawnCommand(ASTNode):
    entity_type: str
    x: int
    y: int

@dataclass
class DestroyCommand(ASTNode):
    target: str

@dataclass
class SetCommand(ASTNode):
    target: str
    property: str
    value: any

@dataclass
class IfStatement(ASTNode):
    condition: Expression
    then_action: ASTNode
    else_action: ASTNode | None = None
```

### Requirement: Parser Function

トークンリストをASTに変換する。

```python
def parse(tokens: list[Token]) -> list[ASTNode]:
    ...
```

#### Scenario: Parse move command

```gherkin
Given tokens [MOVE, IDENTIFIER("player"), NUMBER(5), NUMBER(3)]
When parse is called
Then a MoveCommand(target="player", x=5, y=3) is returned
```

#### Scenario: Parse multiple commands

```gherkin
Given tokens for "move player 5 3\nspawn enemy 10 10"
When parse is called
Then [MoveCommand, SpawnCommand] are returned
```

### Requirement: Error Recovery

構文エラーがあっても、できるだけ多くのコマンドを解析する。

#### Scenario: Skip invalid command

```gherkin
Given tokens for "move 5 3\nmove player 10 10"
When parse is called
Then the first command is skipped (invalid)
And the second command is parsed
And an error is logged
```

## Non-Requirements

- 式の評価（インタプリタの責務）
- 変数スコープ
- 関数定義
