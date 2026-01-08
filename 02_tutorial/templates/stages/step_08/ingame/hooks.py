"""
ゲームフック定義

ゲームループの各フェーズで呼ばれるフック関数。
このファイルをカスタマイズしてゲームの挙動を拡張できます。
"""


def on_turn_start(state: dict) -> dict:
    """ターン開始時に呼ばれる"""
    # デフォルト: 何もしない
    return state


def on_turn_end(state: dict) -> dict:
    """ターン終了時に呼ばれる"""
    # デフォルト: ターン数をインクリメント
    state = dict(state)
    state["turn"] = state.get("turn", 0) + 1
    return state


def on_entity_spawn(state: dict, entity: dict) -> dict:
    """エンティティ生成時に呼ばれる"""
    # デフォルト: 何もしない
    return state


def on_entity_destroy(state: dict, entity: dict) -> dict:
    """エンティティ削除時に呼ばれる"""
    # デフォルト: スコア加算
    state = dict(state)
    state["score"] = state.get("score", 0) + 10
    return state
