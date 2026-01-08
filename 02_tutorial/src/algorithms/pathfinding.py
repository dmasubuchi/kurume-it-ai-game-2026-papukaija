"""
A*経路探索アルゴリズム

グリッドマップ上で最短経路を見つけます。
AIがプレイヤーや目標に向かって移動するために使用します。

例:
    start = Position(0, 0)
    goal = Position(5, 5)
    result = find_path(start, goal, is_walkable, 20, 10)
    # result.path = (Position(0,0), Position(1,1), ..., Position(5,5))
"""

from dataclasses import dataclass
from heapq import heappush, heappop
from typing import Callable

from src.core.state import Position


# ============================================
# 結果型
# ============================================


@dataclass(frozen=True)
class PathResult:
    """経路探索の結果"""

    path: tuple[Position, ...]  # 経路（開始点から終了点まで）
    cost: float  # 総コスト
    found: bool  # 経路が見つかったか
    explored_count: int = 0  # 探索したノード数


# ============================================
# ヒューリスティック関数
# ============================================


def manhattan_distance(a: Position, b: Position) -> float:
    """マンハッタン距離（4方向移動用）"""
    return abs(a.x - b.x) + abs(a.y - b.y)


def euclidean_distance(a: Position, b: Position) -> float:
    """ユークリッド距離（8方向移動用）"""
    return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5


def chebyshev_distance(a: Position, b: Position) -> float:
    """チェビシェフ距離（8方向移動、斜め=1コスト）"""
    return max(abs(a.x - b.x), abs(a.y - b.y))


# ============================================
# 移動方向
# ============================================

# 4方向移動（上下左右）
DIRECTIONS_4 = (
    (0, -1),  # 上
    (0, 1),  # 下
    (-1, 0),  # 左
    (1, 0),  # 右
)

# 8方向移動（斜め含む）
DIRECTIONS_8 = (
    (0, -1),  # 上
    (0, 1),  # 下
    (-1, 0),  # 左
    (1, 0),  # 右
    (-1, -1),  # 左上
    (1, -1),  # 右上
    (-1, 1),  # 左下
    (1, 1),  # 右下
)


# ============================================
# A*アルゴリズム
# ============================================


def find_path(
    start: Position,
    goal: Position,
    is_walkable: Callable[[int, int], bool],
    width: int,
    height: int,
    allow_diagonal: bool = True,
    heuristic: Callable[[Position, Position], float] | None = None,
) -> PathResult:
    """
    A*アルゴリズムで最短経路を探索

    Args:
        start: 開始位置
        goal: 目標位置
        is_walkable: (x, y) が通行可能かを判定する関数
        width: マップの幅
        height: マップの高さ
        allow_diagonal: 斜め移動を許可するか
        heuristic: ヒューリスティック関数（デフォルトはマンハッタン/ユークリッド）

    Returns:
        PathResult: 経路探索の結果
    """
    # 開始=終了の場合
    if start == goal:
        return PathResult(path=(start,), cost=0.0, found=True, explored_count=0)

    # 目標が到達不可能な場合
    if not is_walkable(goal.x, goal.y):
        return PathResult(path=(), cost=0.0, found=False, explored_count=0)

    # 移動方向とヒューリスティック
    directions = DIRECTIONS_8 if allow_diagonal else DIRECTIONS_4
    if heuristic is None:
        heuristic = euclidean_distance if allow_diagonal else manhattan_distance

    # オープンリスト（優先度キュー）: (f_score, counter, position)
    # counterは同じf_scoreの場合の順序保証用
    counter = 0
    open_list: list[tuple[float, int, Position]] = []
    heappush(open_list, (0.0, counter, start))

    # 各ノードへの最小コスト
    g_score: dict[Position, float] = {start: 0.0}

    # 経路復元用の親ノード
    came_from: dict[Position, Position] = {}

    # 探索済みノード
    closed_set: set[Position] = set()

    explored_count = 0

    while open_list:
        _, _, current = heappop(open_list)

        # 既に探索済みならスキップ
        if current in closed_set:
            continue

        explored_count += 1
        closed_set.add(current)

        # 目標に到達
        if current == goal:
            path = _reconstruct_path(came_from, current)
            return PathResult(
                path=path,
                cost=g_score[current],
                found=True,
                explored_count=explored_count,
            )

        # 隣接ノードを探索
        for dx, dy in directions:
            nx, ny = current.x + dx, current.y + dy
            neighbor = Position(x=nx, y=ny)

            # 範囲外チェック
            if not (0 <= nx < width and 0 <= ny < height):
                continue

            # 通行可能チェック
            if not is_walkable(nx, ny):
                continue

            # 既に探索済みならスキップ
            if neighbor in closed_set:
                continue

            # 移動コスト（斜めは√2）
            move_cost = 1.414 if (dx != 0 and dy != 0) else 1.0
            tentative_g = g_score[current] + move_cost

            # より良い経路が見つかった場合
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor, goal)
                came_from[neighbor] = current

                counter += 1
                heappush(open_list, (f_score, counter, neighbor))

    # 経路が見つからなかった
    return PathResult(
        path=(), cost=0.0, found=False, explored_count=explored_count
    )


def _reconstruct_path(
    came_from: dict[Position, Position], current: Position
) -> tuple[Position, ...]:
    """経路を復元"""
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return tuple(reversed(path))


# ============================================
# ユーティリティ
# ============================================


def create_walkability_checker(
    obstacles: set[tuple[int, int]],
    width: int,
    height: int,
) -> Callable[[int, int], bool]:
    """
    障害物セットから通行可能判定関数を作成

    Args:
        obstacles: 障害物の座標セット
        width: マップの幅
        height: マップの高さ

    Returns:
        (x, y) が通行可能かを返す関数
    """

    def is_walkable(x: int, y: int) -> bool:
        if not (0 <= x < width and 0 <= y < height):
            return False
        return (x, y) not in obstacles

    return is_walkable


def get_next_step(
    start: Position,
    goal: Position,
    is_walkable: Callable[[int, int], bool],
    width: int,
    height: int,
) -> Position | None:
    """
    次の1歩だけを取得（AI用ユーティリティ）

    Args:
        start: 現在位置
        goal: 目標位置
        is_walkable: 通行可能判定関数
        width: マップの幅
        height: マップの高さ

    Returns:
        次に移動すべき位置（経路がない場合はNone）
    """
    result = find_path(start, goal, is_walkable, width, height)
    if result.found and len(result.path) >= 2:
        return result.path[1]
    return None
