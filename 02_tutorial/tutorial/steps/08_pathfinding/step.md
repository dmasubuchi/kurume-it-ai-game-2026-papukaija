# Step 08: A*経路探索アルゴリズム

## 学習目標

- A*アルゴリズムの仕組みを理解する
- ヒューリスティック関数の役割を学ぶ
- AIの移動に経路探索を適用する方法を理解する

## 概要

A*（エースター）は、グラフ探索アルゴリズムの一種です。
開始点から目標点への最短経路を効率的に見つけます。

```
f(n) = g(n) + h(n)

f(n): ノードnの評価値
g(n): 開始点からnまでの実コスト
h(n): nから目標までの推定コスト（ヒューリスティック）
```

## 仕様

`openspec/specs/algorithms/pathfinding/spec.md` を参照

## 実装ファイル

- `src/algorithms/pathfinding.py` - A*実装

## 成果物

1. `src/algorithms/pathfinding.py`
2. `examples/step_08_pathfinding/main.py` - 動作例

## 受け入れ条件

- [ ] `find_path()` が最短経路を返す
- [ ] 障害物を回避できる
- [ ] 4方向/8方向移動をサポート
- [ ] 経路が見つからない場合は `found=False`
- [ ] `python examples/step_08_pathfinding/main.py` が動作する

## アルゴリズムの流れ

1. オープンリスト（優先度キュー）に開始点を追加
2. オープンリストが空になるまで繰り返し:
   a. f値が最小のノードを取り出す
   b. 目標に到達したら経路を返す
   c. 隣接ノードを調べ、より良い経路があれば更新
3. 経路が見つからなければ空を返す

## コード例

```python
from src.algorithms.pathfinding import find_path, get_next_step
from src.core.state import Position

# 障害物なしの経路探索
def is_walkable(x, y):
    return True

result = find_path(
    start=Position(0, 0),
    goal=Position(5, 5),
    is_walkable=is_walkable,
    width=10,
    height=10,
)

print(f"Found: {result.found}")
print(f"Path length: {len(result.path)}")
print(f"Cost: {result.cost}")
```

## AI への適用

```python
# 敵がプレイヤーを追いかける
enemy_pos = enemy.pos
player_pos = player.pos

next_pos = get_next_step(
    start=enemy_pos,
    goal=player_pos,
    is_walkable=is_walkable,
    width=state.map_width,
    height=state.map_height,
)

if next_pos:
    enemy = enemy.move_to(next_pos.x, next_pos.y)
```

## 次のステップ

これでMVP（Step 00〜08）が完成です！
InGame本体を実装して、すべてを統合します。
