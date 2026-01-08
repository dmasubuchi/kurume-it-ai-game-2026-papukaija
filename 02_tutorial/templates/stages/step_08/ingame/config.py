"""
ゲーム設定

このファイルを編集してゲームの設定を変更できます。
"""

# マップサイズ
MAP_WIDTH = 20
MAP_HEIGHT = 10

# プレイヤー初期位置
PLAYER_START_X = 5
PLAYER_START_Y = 5

# プレイヤー初期HP
PLAYER_START_HP = 100

# エンティティ表示文字
CHAR_MAPPING = {
    "player": "@",
    "enemy": "E",
    "item": "!",
    "wall": "#",
}

# ゲームタイトル
GAME_TITLE = "AI × Game Tutorial"

# 自動保存（毎ターン）
AUTO_SAVE = True

# AIターン有効
AI_ENABLED = True

# デバッグモード
DEBUG = False
