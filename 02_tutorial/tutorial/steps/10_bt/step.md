# Step 10: BT敵AI（Behavior Tree）

## 学習目標

- Behavior Tree（BT）の概念を理解する
- Selector/Sequence/Condition/Action の役割を学ぶ
- FSMとの違いを理解する

## 概要

Behavior Tree は、AIの意思決定をツリー構造で表現します。
各ノードは SUCCESS/FAILURE/RUNNING を返し、親ノードが結果を評価します。

```
Root (Selector)
  |
  +-- FleeSequence (Sequence)
  |     |-- IsLowHP (Condition)
  |     +-- Flee (Action)
  |
  +-- ChaseSequence (Sequence)
  |     |-- IsPlayerClose (Condition)
  |     +-- Chase (Action)
  |
  +-- Idle (Action)
```

## ノードの種類

| ノード | 動作 |
|--------|------|
| **Selector** | 子を順番に評価し、最初の SUCCESS を返す |
| **Sequence** | 子を順番に評価し、全て SUCCESS なら成功 |
| **Condition** | 条件をチェックして SUCCESS/FAILURE を返す |
| **Action** | 実際の行動（MOVE命令を生成） |

## 評価の流れ

```
1. Root(Selector) が FleeSequence を評価
2. FleeSequence(Sequence) が IsLowHP を評価
   - IsLowHP: hp <= 30 ? SUCCESS : FAILURE
3. IsLowHP が FAILURE なら FleeSequence は FAILURE
4. Selector は次の ChaseSequence を評価
5. ChaseSequence(Sequence) が IsPlayerClose を評価
   - IsPlayerClose: dist <= 5 ? SUCCESS : FAILURE
6. IsPlayerClose が SUCCESS なら Chase を実行
7. Chase が "move enemy dx dy" を生成
```

## コマンド

| コマンド | 説明 |
|----------|------|
| `w/a/s/d` | プレイヤー移動 |
| `wait` | ターンをスキップして敵AIを観察 |
| `toggle_ai` | 敵AIのON/OFF |
| `bt` | BTツリー構造と現在の評価を表示 |
| `status` | プレイヤーと敵の状態を表示 |

## FSMとの比較

| 観点 | FSM | Behavior Tree |
|------|-----|---------------|
| 構造 | 状態と遷移 | ツリーノード |
| 拡張性 | 状態追加が大変 | ノード追加が容易 |
| 可読性 | 図で分かりやすい | 階層が深くなると複雑 |
| 優先度 | 明示的に管理 | ツリー構造で自然に表現 |

## やってみよう

1. `bt` でツリー構造を確認
2. `wait` で敵AIの動きを観察
3. ログで「どのブランチが選ばれたか」を確認
4. プレイヤーを動かしてAIの反応を観察

## 次のステップ

BTはツリー構造で優先度を表現できますが、
「目標から逆算して行動を決める」ことはできません。
Step 11 では、目標指向の GOAP を学びます。
