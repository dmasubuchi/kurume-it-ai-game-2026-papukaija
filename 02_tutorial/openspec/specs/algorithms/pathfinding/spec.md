# A* Pathfinding Specification

## Overview

A*アルゴリズムを使用して、グリッドマップ上の最短経路を探索します。
AIエンティティがプレイヤーや目標に向かって移動するために使用します。

```
開始: Position(0, 0)
目標: Position(5, 5)
結果: [Position(0,0), Position(1,1), ..., Position(5,5)]
```

## Requirements

### Requirement: Basic Pathfinding

開始位置から目標位置への最短経路を見つける。

```python
def find_path(
    start: Position,
    goal: Position,
    is_walkable: Callable[[int, int], bool],
    width: int,
    height: int,
) -> PathResult:
    ...
```

#### Scenario: Find path in open grid

```gherkin
Given a 10x10 grid with no obstacles
And start at (0, 0) and goal at (5, 5)
When find_path is called
Then a path is found
And the path starts at (0, 0) and ends at (5, 5)
```

#### Scenario: Path around obstacle

```gherkin
Given a grid with obstacle at (2, 2)
And start at (0, 0) and goal at (4, 4)
When find_path is called
Then a path is found
And the path does not include (2, 2)
```

#### Scenario: No path available

```gherkin
Given a grid where goal is surrounded by obstacles
When find_path is called
Then found is False
And path is empty
```

### Requirement: Movement Directions

4方向または8方向の移動をサポートする。

#### Scenario: 4-direction movement

```gherkin
Given allow_diagonal = False
When find_path is called
Then the path only uses up/down/left/right moves
```

#### Scenario: 8-direction movement

```gherkin
Given allow_diagonal = True
When find_path is called
Then the path may use diagonal moves
And diagonal moves have cost √2
```

### Requirement: Heuristic Functions

複数のヒューリスティック関数をサポートする。

- `manhattan_distance`: 4方向移動に最適
- `euclidean_distance`: 8方向移動に最適
- `chebyshev_distance`: 斜め移動コスト1の場合

### Requirement: AI Helper

AIが次の1歩だけを取得できるユーティリティ。

```python
def get_next_step(start, goal, is_walkable, width, height) -> Position | None:
    ...
```

#### Scenario: Get next step

```gherkin
Given a path exists from (0, 0) to (5, 5)
When get_next_step is called
Then the second position of the full path is returned
```

## Non-Requirements

- 動的な障害物更新
- 複数エージェントの衝突回避
- 階層的経路探索（HPA*）
