"""
AI行動定義

このファイルをカスタマイズしてAIの行動を変更できます。
A*経路探索を使用してプレイヤーを追いかけます。
"""

import random
import sys
from pathlib import Path

# srcをインポートパスに追加
_tutorial_root = Path(__file__).parent.parent.parent
if str(_tutorial_root) not in sys.path:
    sys.path.insert(0, str(_tutorial_root))

try:
    from src.core.state import Position
    from src.algorithms.pathfinding import get_next_step, create_walkability_checker
except ImportError:
    # フォールバック：A*が使えない場合はランダム移動
    Position = None
    get_next_step = None


def decide_action(entity: dict, state: dict) -> str:
    """
    エンティティの行動を決定

    Args:
        entity: 行動するエンティティ
        state: 現在のゲーム状態

    Returns:
        行動を表すDSL文字列
    """
    entity_name = entity.get("name", "enemy")
    entity_x = entity.get("x", 0)
    entity_y = entity.get("y", 0)

    # プレイヤー情報
    player = state.get("player", {})
    player_x = player.get("x", 0)
    player_y = player.get("y", 0)

    # A*が使える場合
    if Position and get_next_step:
        return _chase_with_astar(
            entity_name, entity_x, entity_y,
            player_x, player_y, state
        )

    # フォールバック：ランダム移動
    return _random_move(entity_name, entity_x, entity_y, state)


def _chase_with_astar(
    entity_name: str,
    entity_x: int,
    entity_y: int,
    player_x: int,
    player_y: int,
    state: dict,
) -> str:
    """A*でプレイヤーを追いかける"""
    width = state.get("map_width", 20)
    height = state.get("map_height", 10)

    # 障害物セットを作成（他のエンティティ）
    obstacles = set()
    for e in state.get("entities", []):
        if e.get("is_active", True):
            ex, ey = e.get("x", 0), e.get("y", 0)
            if (ex, ey) != (entity_x, entity_y):  # 自分自身は除く
                obstacles.add((ex, ey))

    is_walkable = create_walkability_checker(obstacles, width, height)

    # 次の1歩を計算
    start = Position(x=entity_x, y=entity_y)
    goal = Position(x=player_x, y=player_y)

    next_pos = get_next_step(start, goal, is_walkable, width, height)

    if next_pos:
        return f"move {entity_name} {next_pos.x} {next_pos.y}"

    # 経路がない場合はランダム移動
    return _random_move(entity_name, entity_x, entity_y, state)


def _random_move(
    entity_name: str,
    entity_x: int,
    entity_y: int,
    state: dict,
) -> str:
    """ランダムに移動"""
    width = state.get("map_width", 20)
    height = state.get("map_height", 10)

    dx = random.choice([-1, 0, 1])
    dy = random.choice([-1, 0, 1])

    new_x = max(0, min(width - 1, entity_x + dx))
    new_y = max(0, min(height - 1, entity_y + dy))

    return f"move {entity_name} {new_x} {new_y}"


def should_attack(entity: dict, state: dict) -> bool:
    """
    攻撃すべきかどうか判定

    Args:
        entity: エンティティ
        state: ゲーム状態

    Returns:
        攻撃すべきならTrue
    """
    # プレイヤーとの距離をチェック
    player = state.get("player", {})
    entity_x = entity.get("x", 0)
    entity_y = entity.get("y", 0)
    player_x = player.get("x", 0)
    player_y = player.get("y", 0)

    distance = abs(entity_x - player_x) + abs(entity_y - player_y)

    # 隣接している場合は攻撃
    return distance <= 1
