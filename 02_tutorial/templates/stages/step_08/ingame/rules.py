"""
ゲームルール定義

このファイルをカスタマイズしてゲームルールを変更できます。
"""

from typing import Any


def can_move(state: dict, x: int, y: int) -> bool:
    """
    指定座標に移動できるか判定

    Args:
        state: ゲーム状態（辞書形式）
        x: 移動先X座標
        y: 移動先Y座標

    Returns:
        移動可能ならTrue
    """
    # マップ範囲チェック
    width = state.get("map_width", 20)
    height = state.get("map_height", 10)

    if not (0 <= x < width and 0 <= y < height):
        return False

    # 他のエンティティとの衝突チェック
    for entity in state.get("entities", []):
        if entity.get("x") == x and entity.get("y") == y:
            if entity.get("is_active", True):
                return False

    return True


def calculate_damage(attacker: dict, defender: dict) -> int:
    """
    ダメージ計算

    Args:
        attacker: 攻撃者データ
        defender: 防御者データ

    Returns:
        ダメージ量
    """
    # 基本ダメージ
    base_damage = 10

    # 攻撃者のHPが高いほどダメージ増加（オプション）
    attacker_hp = attacker.get("hp", 100)
    bonus = attacker_hp // 50

    return base_damage + bonus


def is_game_over(state: dict) -> bool:
    """
    ゲーム終了判定

    Args:
        state: ゲーム状態

    Returns:
        ゲーム終了ならTrue
    """
    player = state.get("player", {})

    # プレイヤーのHPが0以下
    if player.get("hp", 100) <= 0:
        return True

    # 特定のスコアに到達（オプション）
    # if state.get("score", 0) >= 1000:
    #     return True

    return False


def get_score_for_kill(entity: dict) -> int:
    """
    エンティティ撃破時のスコア

    Args:
        entity: 撃破したエンティティ

    Returns:
        獲得スコア
    """
    entity_type = entity.get("name", "").lower()

    scores = {
        "goblin": 10,
        "orc": 20,
        "dragon": 100,
        "enemy": 10,  # デフォルト
    }

    return scores.get(entity_type, 10)
