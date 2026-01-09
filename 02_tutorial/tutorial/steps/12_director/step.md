# Step 12: Director AI（システムAI）

## 学習目標

- Director AIの概念を理解する
- Tension（緊張度）によるゲーム体験制御を学ぶ
- 敵AIとDirector AIの役割の違いを理解する

## 概要

Director AIは「ゲーム体験全体」を制御するシステムAIです。
個々のキャラクターではなく、ゲームの「難易度」や「雰囲気」を調整します。

```
┌─────────────────────────────────────────┐
│           Director AI                    │
│  ┌─────────────────────────────────┐    │
│  │ Tension: LOW → MID → HIGH      │    │
│  │                                 │    │
│  │ Rules:                          │    │
│  │  - LOW:  chase_dist=8 (余裕)   │    │
│  │  - MID:  chase_dist=5 (普通)   │    │
│  │  - HIGH: chase_dist=3 (緊迫)   │    │
│  └─────────────────────────────────┘    │
│                  ↓                       │
│            敵AIパラメータ                │
└─────────────────────────────────────────┘
```

## Tension（緊張度）

プレイヤーの状態に応じて、ゲームの難易度を動的に調整します。

| Tension | 条件 | 効果 |
|---------|------|------|
| LOW | player.hp >= 70 | chase_distance=8（敵が遠くから追いかけ始める） |
| MID | 30 < player.hp < 70 | chase_distance=5（通常） |
| HIGH | player.hp <= 30 | chase_distance=3（敵が近くでのみ追いかける） |

## Director AIの役割

| 敵AI（Step 09-11） | Director AI |
|--------------------|-------------|
| 個々のキャラクター制御 | ゲーム体験全体の制御 |
| 「どう動くか」を決める | 「敵AIのパラメータ」を決める |
| プレイヤーへの直接的な脅威 | 間接的な難易度調整 |

## コマンド

| コマンド | 説明 |
|----------|------|
| `w/a/s/d` | プレイヤー移動 |
| `wait` | ターンをスキップして観察 |
| `director` | 現在のTensionとルールを表示 |
| `toggle_director` | DirectorのON/OFF |
| `status` | プレイヤーと敵の状態を表示 |

## ログ出力例

```
[Director] Tension: MID -> chase=5
Player moved to (5, 3)
[AI] enemy MOVE (dx=1, dy=0)

... プレイヤーがダメージを受けてHP低下 ...

[Director] Tension: HIGH -> chase=3
[AI] enemy IDLE (dist=4 > chase=3)
```

Tensionが HIGH になると、敵の追跡距離が短くなり、
プレイヤーに「回復の猶予」を与えます。

## やってみよう

1. `director` でTensionを確認
2. `wait` で敵AIの動きを観察
3. プレイヤーをダメージを受ける状況に（HPを減らす）
4. Tensionの変化と敵AIの行動変化を観察
5. `toggle_director` でDirectorをOFFにして違いを確認

## 次のステップ

ここまでで、AIの各レイヤー（敵AI、Director AI）を学びました。
Step 13 では、「人間・AI・ルール」の責任分界を統合的に理解します。
