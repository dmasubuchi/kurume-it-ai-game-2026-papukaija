# Step 02: State管理

## 学習目標

- ゲーム状態（State）の設計を理解する
- 不変（immutable）データ構造の利点を学ぶ
- dataclassを使った状態管理を実装する

## 概要

Stateはゲーム世界の「今この瞬間」を表すデータです。
プレイヤーの位置、敵の位置、スコアなど、全てがStateに含まれます。

**重要な原則:**
- State は「唯一の真実」（Single Source of Truth）
- State は不変（frozen dataclass）
- 更新は新しいStateを返す

## 仕様

`openspec/specs/core/state-management/spec.md` を参照

## 実装ファイル

- `src/core/state.py` - GameState定義

## 成果物

1. `src/core/state.py`
2. `examples/step_02_state/main.py` - 動作例

## 受け入れ条件

- [ ] GameState は frozen dataclass
- [ ] `replace()` メソッドで新しいStateを生成できる
- [ ] 元のStateは変更されない
- [ ] `python examples/step_02_state/main.py` が動作する

## コード例

```python
@dataclass(frozen=True)
class GameState:
    player_x: int = 0
    player_y: int = 0
    turn: int = 0

# 不変なので直接変更は不可
state = GameState()
# state.player_x = 5  # Error!

# replace で新しいStateを作成
new_state = state.replace(player_x=5)
print(state.player_x)      # 0（元のまま）
print(new_state.player_x)  # 5
```

## 次のステップ

Step 03 では入力処理（I/O）を学びます。
