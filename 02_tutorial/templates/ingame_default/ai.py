"""
AI行動定義

このファイルをカスタマイズしてAIの行動を変更できます。
"""

import random


def decide_action(entity: dict, state: dict) -> str:
    """
    エンティティの行動を決定

    Args:
        entity: 行動するエンティティ
        state: 現在のゲーム状態

    Returns:
        行動を表すDSL文字列
    """
    # デフォルト: ランダムに移動
    dx = random.choice([-1, 0, 1])
    dy = random.choice([-1, 0, 1])

    entity_name = entity.get("name", "enemy")
    new_x = entity.get("x", 0) + dx
    new_y = entity.get("y", 0) + dy

    return f"move {entity_name} {new_x} {new_y}"
