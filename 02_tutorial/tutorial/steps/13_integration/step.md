# Step 13: Human x AI x Rules（責任分界）

## 学習目標

- 人間・AI・ルールの責任分界を理解する
- DSLによる「検証可能な命令」の重要性を理解する
- ゲーム開発における各レイヤーの役割を理解する

## 概要

このStepでは、ゲームにおける3つのレイヤーの責任分界を学びます。

```
┌──────────────────────────────────────────────┐
│                   Human                       │
│  「何をしたいか」を入力                       │
│  - w/a/s/d で移動                             │
│  - dsl move player 1 0 で直接DSL入力          │
└─────────────────────┬────────────────────────┘
                      ↓
┌──────────────────────────────────────────────┐
│                    AI                         │
│  「どう動くか」を決定し、DSL命令を生成        │
│  - FSM/BT/GOAP が move enemy dx dy を生成    │
│  - Director が敵AIパラメータを調整           │
└─────────────────────┬────────────────────────┘
                      ↓
┌──────────────────────────────────────────────┐
│                  Rules                        │
│  DSL命令を「検証」し「実行」する              │
│  - move の移動可能性をチェック                │
│  - 壁への移動は拒否                           │
│  - 状態を更新                                 │
└──────────────────────────────────────────────┘
```

## なぜDSLを通すのか

AIが直接状態を変更すると、問題が発生します：

```python
# 悪い例: AIが直接状態を変更
def ai_move(state, enemy):
    enemy.pos.x += 1  # 壁チェックなし！バグの温床
    return state

# 良い例: AIはDSL命令を生成、Rulesが検証・実行
def ai_generate_command(state, enemy):
    return "move enemy 1 0"  # 移動「したい」という意図のみ

def rules_execute(command, state):
    # 移動可能かチェック
    if is_walkable(target_pos):
        return state.move_entity(...)
    return state  # 不正な移動は無視
```

## 責任分界の利点

| レイヤー | 責任 | テスト方法 |
|----------|------|------------|
| Human | 入力を与える | 手動テスト |
| AI | 意図を決定する | AIロジックの単体テスト |
| Rules | 検証・実行する | インタプリタの単体テスト |

## コマンド

| コマンド | 説明 |
|----------|------|
| `w/a/s/d` | プレイヤー移動（ショートカット） |
| `dsl <cmd>` | DSLコマンドを直接実行 |
| `ai on/off` | AIの有効/無効切替 |
| `validate` | 直近のDSL命令の検証結果を表示 |
| `status` | 現在の状態を表示 |

## Input Mode

このStepでは MIXED モードを使用します。

| Mode | 説明 | 使用Step |
|------|------|----------|
| GAME | w/a/s/d のみ | Step 08-12 |
| DSL | DSLコマンドのみ | Step 05-07 |
| MIXED | 両方使用可能 | Step 13 |

## ログ出力例

```
CMD> dsl move player 1 0
[Human] Input: dsl move player 1 0 -> DSL: move player 1 0
[AI] Proposed: move enemy 0 -1

CMD> validate
Last DSL: move player 1 0
Result: Valid

CMD> ai off
AI disabled.

CMD> w
[Human] Input: w -> DSL: move player 0 -1
(AI is disabled, no proposal)
```

## やってみよう

1. `dsl move player 1 0` でDSL直接入力を試す
2. `validate` で検証結果を確認
3. `ai on/off` でAIの有効/無効を切り替え
4. AIからの提案（Proposed）を観察
5. 不正なDSL（`dsl move player 100 0`）を試して拒否されることを確認

## まとめ

```
Human → 意図を入力
  ↓
AI → 意図をDSL命令に変換（または提案）
  ↓
Rules → DSL命令を検証・実行
  ↓
State → 不変データとして更新
```

この分離により：
- AIのバグがルール違反を起こさない
- 各レイヤーを独立してテストできる
- デバッグが容易になる
