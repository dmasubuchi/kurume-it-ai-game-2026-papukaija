# Step 09: OutGame/InGame統合

## 学習目標

- OutGame/InGameアーキテクチャを理解する
- メニューシステムの設計パターンを学ぶ
- セーブデータ管理の実装を理解する
- Stageシステムによるコンテンツ分離を学ぶ

## 概要

Step 08まででゲームのコア機能（ループ、状態管理、DSL、AI）が完成しました。
このステップでは、それらを「製品」として統合するためのOutGameシステムを実装します。

```
ゲーム全体
├── OutGame（メニュー画面）
│   ├── メインメニュー
│   ├── Stage選択
│   ├── Slot選択
│   └── セーブ管理
└── InGame（ゲーム本体）
    ├── ゲームループ
    ├── DSLインタプリタ
    └── AI処理
```

## なぜ分離が必要か

1. **責務の分離**: メニューとゲームは異なる責務を持つ
2. **テスト容易性**: 各部分を独立してテストできる
3. **拡張性**: 新しいStageを追加しやすい
4. **保守性**: バグの原因を特定しやすい

## 仕様

### OutGameMenu

- メインメニューを表示
- New Game / Continue / Manage Saves / Quit を提供
- InGameを起動するコールバックを受け取る

### SaveManager

- 3つのスロット（SAVE_A, SAVE_B, SAVE_C）を管理
- スロットの作成/削除/コピー/リセット
- Stage情報の保持

### StageManager

- `templates/stages/` からStageを探索
- Stage情報（名前、説明、コマンド）を提供

## 実装ファイル

```
src/outgame/
├── __init__.py
├── menu.py          # OutGameMenu
├── save_manager.py  # SaveManager
└── stage_manager.py # StageManager
```

## 成果物

1. `src/outgame/menu.py` - メニューシステム
2. `src/outgame/save_manager.py` - セーブ管理
3. `src/outgame/stage_manager.py` - Stage探索
4. `templates/stages/step_**/` - 各Stepに対応するStage

## 受け入れ条件

- [ ] `python -m src.outgame.menu` でメインメニューが起動
- [ ] New Gameで新しいゲームを開始できる
- [ ] Stage選択画面が表示される
- [ ] Slot選択画面が表示される
- [ ] ContinueでSAVEデータから再開できる
- [ ] Manage Savesでスロット操作ができる

## OutGameMenuの設計

```python
class OutGameMenu:
    def __init__(
        self,
        base_path: Path | None = None,
        on_play: Callable[[SlotName, Path], None] | None = None,
    ):
        self.save_manager = SaveManager(base_path)
        self.stage_manager = StageManager(base_path)
        self.on_play = on_play

    def run(self) -> None:
        """メニューループを実行"""
        while self.running:
            choice = self.show_main_menu()
            # ...処理...
```

## SaveManagerの設計

```python
@dataclass
class SlotStatus:
    name: SlotName
    exists: bool
    ready: bool
    created_at: str | None = None
    last_played: str | None = None
    turn: int = 0
    loaded_stage: str | None = None

class SaveManager:
    def setup(self, slot: SlotName, stage_id: str | None = None) -> bool:
        """Stageテンプレートからスロットを初期化"""

    def reset(self, slot: SlotName) -> bool:
        """スロットをリセット"""

    def delete(self, slot: SlotName) -> bool:
        """スロットを削除"""

    def copy(self, src: SlotName, dest: SlotName) -> bool:
        """スロットをコピー"""
```

## Stageシステムの設計方針

```
templates/
├── ingame_default/     # 共通のゲームエンジン
│   ├── game.py         # ★これは各Stageでは上書きしない
│   ├── config.py       # デフォルト設定
│   └── ai.py           # デフォルトAI
├── state_default.json  # デフォルト初期状態
└── stages/
    ├── step_01/
    │   ├── stage.json  # Stage定義
    │   ├── state.json  # 初期状態（オプション）
    │   └── ingame/     # Stage固有設定（オプション）
    │       └── config.py
    ├── step_02/
    ...
```

## stage.jsonの仕様

```json
{
  "id": "step_01",
  "name": "Step 01: Game Loop",
  "name_ja": "ゲームループの基礎",
  "description": "Learn the basic turn-based game loop pattern",
  "description_ja": "カウンターを増減させてゲームループを体験します",
  "commands": ["up", "+", "down", "-", "reset", "help", "quit"],
  "help_text": "up(+): カウンター+1, down(-): カウンター-1"
}
```

## ゲーム起動フロー

```
1. OutGameMenu.run()
2. → handle_new_game()
3.   → show_stage_selection() → StageInfo
4.   → show_slot_selection() → SlotName
5.   → SaveManager.setup(slot, stage_id)
6.   → on_play(slot, slot_path)
7.     → InGame: game.run(slot_path)
```

## 設計のポイント

### 1. 核心部分の保護

- `game.py` は `ingame_default` のみに存在
- 各Stageは `game.py` を上書きできない
- これにより「何が共通で、何が変わるか」が明確

### 2. 合成による拡張

- Stage固有の `config.py` で設定を上書き
- Stage固有の `state.json` で初期状態を変更
- 継承ではなく合成で拡張性を確保

### 3. メタデータの分離

- `meta.json`: ゲーム外情報（作成日時、プレイ時間）
- `state.json`: ゲーム内状態（プレイヤー位置、スコア）
- 責務の明確な分離

## 因数分解の視点から

このステップで学ぶ分解：

| 大きな問題 | 分解後の部品 |
|------------|--------------|
| ゲーム起動 | メニュー / セーブ管理 / Stage管理 |
| データ保存 | state.json / meta.json / log.txt |
| ゲーム設定 | 共通設定 / Stage固有設定 |

## コード例：基本的な使用法

```python
from pathlib import Path
from src.outgame.menu import OutGameMenu

# ゲームハンドラー
def on_play(slot: str, slot_path: Path) -> None:
    from templates.ingame_default import game
    game.run(slot_path)

# メニュー起動
menu = OutGameMenu(on_play=on_play)
menu.run()
```

## 次のステップ

Step 09でMVPの統合が完了しました。

次の方向性：
- Step 10+: 高度なAI（GOAP, HTN）
- Step 10+: マルチプレイヤー
- Step 10+: カスタムStageの作成演習

## 演習課題

1. 新しいStage `step_custom` を作成する
2. 独自の初期状態を設定する
3. 独自のヘルプテキストを書く
4. 「なぜそう設計したか」を説明できるようにする
