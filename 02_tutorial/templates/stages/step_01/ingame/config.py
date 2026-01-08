"""
Step 01: Game Loop - Configuration

ゲームループの基礎を学ぶステージ。
シンプルなコマンドでループの流れを体験。
"""

# ゲーム設定
GAME_TITLE = "Step 01: Game Loop"
MAP_WIDTH = 20
MAP_HEIGHT = 10
PLAYER_START_X = 10
PLAYER_START_Y = 5
PLAYER_START_HP = 100

# 表示設定
CHAR_MAPPING = {
    "wall": "#",
    "floor": ".",
    "player": "@",
    "enemy": "?",
}

# 機能フラグ
AUTO_SAVE = True
DEBUG = False

# ヘルプテキスト（Stage固有）
HELP_TEXT = """
=== Step 01: Game Loop ===
ゲームループを体験しよう！

基本コマンド:
  move player <x> <y>  - プレイヤーを移動
  status               - 状態を表示
  quit                 - 終了

例:
  move player 11 5     - 右へ1マス移動
  move player 10 4     - 上へ1マス移動

ゲームループ: Input → Update → Render
"""
