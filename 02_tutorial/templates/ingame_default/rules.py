"""
ゲームルール定義

このファイルをカスタマイズしてゲームルールを変更できます。
"""


def can_move(state: dict, x: int, y: int) -> bool:
    """指定座標に移動できるか判定"""
    # デフォルト: 0-19の範囲内なら移動可能
    return 0 <= x < 20 and 0 <= y < 20


def calculate_damage(attacker: dict, defender: dict) -> int:
    """ダメージ計算"""
    # デフォルト: 固定10ダメージ
    return 10


def is_game_over(state: dict) -> bool:
    """ゲーム終了判定"""
    player = state.get("player", {})
    return player.get("hp", 0) <= 0
