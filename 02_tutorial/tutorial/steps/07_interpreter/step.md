# Step 07: DSLインタプリタ（実行器）

## 学習目標

- インタプリタの役割を理解する
- ASTを実行して状態を変更する方法を学ぶ
- 式評価（Expression Evaluation）の実装を理解する

## 概要

インタプリタは、パーサーが生成したAST（抽象構文木）を実際に実行します。
これはDSL処理の最終段階です。

```
ソースコード → Lexer → トークン → Parser → AST → Interpreter → 実行結果
```

## 仕様

`openspec/specs/dsl/interpreter/spec.md` を参照

## 実装ファイル

- `src/dsl/interpreter.py` - インタプリタ実装

## 成果物

1. `src/dsl/interpreter.py`
2. `examples/step_07_interpreter/main.py` - 動作例

## 受け入れ条件

- [ ] `execute_command()` が各コマンドを実行できる
- [ ] `evaluate()` が式を評価して値を返す
- [ ] `execute()` がプログラム全体を実行できる
- [ ] 実行時エラーが適切に処理される
- [ ] `python examples/step_07_interpreter/main.py` が動作する

## コマンド実行

```python
def execute_command(cmd: ASTNode, state: GameState) -> GameState:
    if isinstance(cmd, MoveCommand):
        return state.move_player(cmd.x, cmd.y)
    elif isinstance(cmd, SpawnCommand):
        new_entity = Entity(...)
        return state.replace(entities=state.entities + (new_entity,))
    # ...
```

## 式評価

```python
def evaluate(expr: Expression, state: GameState) -> Any:
    if isinstance(expr, NumberLiteral):
        return expr.value
    elif isinstance(expr, PropertyAccess):
        entity = resolve_identifier(expr.object, state)
        return getattr(entity, expr.property)
    elif isinstance(expr, BinaryOp):
        left = evaluate(expr.left, state)
        right = evaluate(expr.right, state)
        return apply_operator(expr.op, left, right)
    # ...
```

## 実行例

```python
from src.dsl.interpreter import interpret
from src.core.state import create_initial_state

state = create_initial_state()
result = interpret("move player 5 3", state)
print(f"Player moved to: ({result.state.player.pos.x}, {result.state.player.pos.y})")
# Output: Player moved to: (5, 3)
```

## 次のステップ

Step 08 では、A*アルゴリズムを実装してAIの経路探索を行います。
