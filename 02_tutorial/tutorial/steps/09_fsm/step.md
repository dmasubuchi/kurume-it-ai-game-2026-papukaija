# Step 09: FSM敵AI（有限状態機械）

## 学習目標

- FSM（Finite State Machine）の概念を理解する
- 状態（State）と遷移（Transition）の設計を学ぶ
- 敵AIがDSL命令を生成する仕組みを理解する

## 概要

FSM（有限状態機械）は、AIの行動を「状態」と「遷移条件」で表現する手法です。

```
     ┌────────────────────────────────────┐
     │                                    │
     v     dist <= 5         dist > 5     │
  ┌──────┐ ─────────> ┌───────┐ ─────────>┘
  │ IDLE │            │ CHASE │
  └──────┘ <───────── └───────┘
     │     dist > 5       │
     │                    │ hp <= 30
     │                    v
     │               ┌───────┐
     └───────────────│ FLEE  │
         hp > 30     └───────┘
```

## 状態定義

| 状態 | 条件 | 行動 |
|------|------|------|
| IDLE | プレイヤーが遠い | 何もしない |
| CHASE | プレイヤーが近い & HP高い | プレイヤーに接近 |
| FLEE | HP低い | プレイヤーから逃走 |

## 遷移条件

```python
CHASE_DISTANCE = 5  # この距離以下でCHASEに遷移
FLEE_HP = 30        # このHP以下でFLEEに遷移

def decide_state(current_state, distance, hp):
    if hp <= FLEE_HP:
        return "FLEE"
    if distance <= CHASE_DISTANCE:
        return "CHASE"
    return "IDLE"
```

## コマンド

| コマンド | 説明 |
|----------|------|
| `w/a/s/d` | プレイヤー移動 |
| `wait` | ターンをスキップして敵AIを観察 |
| `toggle_ai` | 敵AIのON/OFF |
| `ai` | FSMの現在状態と遷移条件を表示 |
| `status` | プレイヤーと敵の状態を表示 |

## 核心: AIはDSL命令を生成する

FSMは直接ゲーム状態を変更しません。
代わりに、DSL命令（`move enemy dx dy`）を生成します。

```python
def fsm_generate_command(state, enemy) -> str:
    fsm_state = decide_state(...)

    if fsm_state == "CHASE":
        dx, dy = direction_toward_player(enemy, player)
        return f"move enemy {dx} {dy}"

    if fsm_state == "FLEE":
        dx, dy = direction_away_from_player(enemy, player)
        return f"move enemy {dx} {dy}"

    return ""  # IDLE: 何もしない
```

## やってみよう

1. `wait` で敵AIの動きを観察
2. `ai` でFSM状態を確認
3. プレイヤーを近づけて IDLE→CHASE の遷移を観察
4. `toggle_ai` でAIをOFFにして違いを確認

## 次のステップ

FSMはシンプルですが、状態が増えると複雑になります。
Step 10 では、より柔軟な Behavior Tree を学びます。
