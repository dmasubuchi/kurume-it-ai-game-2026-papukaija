# Step 11: GOAP敵AI（目標指向行動計画）

## 学習目標

- GOAP（Goal-Oriented Action Planning）の概念を理解する
- World State と Action の設計を学ぶ
- 目標から行動列を逆算する仕組みを理解する

## 概要

GOAP は「目標状態」を定義し、そこに到達するための
「行動の列」を探索アルゴリズムで見つけます。

```
現在の状態              目標状態
┌─────────────┐        ┌─────────────┐
│ player_near │   →    │ player_dead │
│ enemy_hp=50 │        │ or escaped  │
└─────────────┘        └─────────────┘
         ↓ 探索
    ┌─────────┐
    │ Action列 │
    │ 1. Approach │
    │ 2. Attack   │
    └─────────┘
```

## World State

ゲーム状態を「真偽値の辞書」として表現します。

```python
world_state = {
    "player_near": True,      # dist <= 5
    "player_adjacent": False, # dist <= 1
    "enemy_low_hp": False,    # hp <= 30
}
```

## Action定義

各Actionは「前提条件」と「効果」を持ちます。

```python
actions = [
    Action(
        name="Approach",
        preconditions={"player_near": True},
        effects={"player_adjacent": True},
        command=lambda: f"move enemy ..."
    ),
    Action(
        name="Flee",
        preconditions={"enemy_low_hp": True},
        effects={"player_near": False},
        command=lambda: f"move enemy ..."
    ),
]
```

## 計画生成

```python
def plan(goal, world_state, actions):
    # 目標状態を満たすActionを探す
    for action in actions:
        if action.can_achieve(goal) and action.is_applicable(world_state):
            # 前提条件が満たされていれば実行
            # 満たされていなければ、前提条件を新たな目標に
            ...
```

## コマンド

| コマンド | 説明 |
|----------|------|
| `w/a/s/d` | プレイヤー移動 |
| `wait` | ターンをスキップして敵AIを観察 |
| `toggle_ai` | 敵AIのON/OFF |
| `goap` | 現在のWorld Stateとプランを表示 |
| `status` | プレイヤーと敵の状態を表示 |

## FSM/BTとの比較

| 観点 | FSM | BT | GOAP |
|------|-----|----|----- |
| 行動決定 | 現在の状態 | ツリー評価 | 目標から逆算 |
| 拡張性 | 低い | 中程度 | 高い |
| 複雑さ | 低い | 中程度 | 高い |
| 柔軟性 | 低い | 中程度 | 高い |

## やってみよう

1. `goap` で現在のWorld Stateを確認
2. `wait` で敵AIの動きを観察
3. プレイヤーを動かしてWorld Stateの変化を確認
4. ログで「どのActionが選ばれたか」を確認

## 次のステップ

ここまでは「敵AI」を学びました。
Step 12 では、ゲーム全体を制御する「Director AI」を学びます。
