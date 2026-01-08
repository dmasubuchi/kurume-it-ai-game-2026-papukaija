# DSL Interpreter Specification

## Overview

インタプリタ（実行器）は、ASTを実際に実行してGameStateを変更します。
これはインタプリタの3番目のステップです。

```
AST: MoveCommand(target="player", x=5, y=3)
実行: state.move_player(5, 3) → 新しいGameState
```

## Requirements

### Requirement: Command Execution

各種コマンドASTノードを実行してGameStateを変更する。

```python
def execute_command(cmd: ASTNode, state: GameState) -> GameState:
    ...
```

#### Scenario: Execute move command

```gherkin
Given a MoveCommand(target="player", x=5, y=3)
And a GameState with player at (0, 0)
When execute_command is called
Then the new state has player at (5, 3)
```

#### Scenario: Execute spawn command

```gherkin
Given a SpawnCommand(entity_type="enemy", x=10, y=10, name="Goblin")
And a GameState with empty entities
When execute_command is called
Then the new state has one entity at (10, 10)
And the entity name is "Goblin"
```

#### Scenario: Execute destroy command

```gherkin
Given a DestroyCommand(target="enemy")
And a GameState with an enemy entity
When execute_command is called
Then the new state has no enemy entity
And score increases by 10
```

### Requirement: Expression Evaluation

式を評価して値を返す。

```python
def evaluate(expr: Expression, state: GameState) -> Any:
    ...
```

#### Scenario: Evaluate property access

```gherkin
Given a PropertyAccess(object="player", property="hp")
And a GameState with player.hp = 100
When evaluate is called
Then 100 is returned
```

#### Scenario: Evaluate binary operation

```gherkin
Given a BinaryOp(left=player.hp, op="<", right=50)
And a GameState with player.hp = 30
When evaluate is called
Then True is returned
```

### Requirement: Conditional Execution

条件文を評価し、適切なブランチを実行する。

#### Scenario: Execute if-then when condition is true

```gherkin
Given an IfStatement with condition player.hp < 50
And a GameState with player.hp = 30
When execute_command is called
Then the then_action is executed
```

#### Scenario: Execute if-else when condition is false

```gherkin
Given an IfStatement with condition player.hp < 50 and else_action
And a GameState with player.hp = 80
When execute_command is called
Then the else_action is executed
```

### Requirement: Program Execution

プログラム全体（複数文）を順次実行する。

```python
def execute(program: Program, state: GameState) -> ExecutionResult:
    ...
```

#### Scenario: Execute multiple commands

```gherkin
Given a Program with [MoveCommand, SpawnCommand, DestroyCommand]
When execute is called
Then all commands are executed in order
And the final state reflects all changes
```

### Requirement: Error Handling

実行時エラーを適切に処理し、ログに記録する。

#### Scenario: Unknown entity reference

```gherkin
Given a MoveCommand with target="unknown_entity"
When execute_command is called
Then an error is logged
And the state is unchanged
```

## Non-Requirements

- 最適化（インライン化、定数畳み込み等）
- デバッガ機能
- ステップ実行
