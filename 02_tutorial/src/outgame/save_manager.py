"""
SAVEスロット管理

SAVE_A, SAVE_B, SAVE_C の3スロットを管理する。
各スロットには:
- state.json: ゲーム状態
- meta.json: メタデータ（作成日時、プレイ時間等）
- log.txt: ゲームログ
- ingame/: カスタムゲームロジック
"""

import json
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Literal


SlotName = Literal["A", "B", "C"]
SLOTS: tuple[SlotName, ...] = ("A", "B", "C")


@dataclass
class SlotStatus:
    """スロットの状態"""

    name: SlotName
    exists: bool
    ready: bool
    created_at: str | None = None
    last_played: str | None = None
    turn: int = 0
    loaded_stage: str | None = None  # ロードされたStage ID


class SaveManager:
    """SAVE管理クラス"""

    def __init__(self, base_path: Path | None = None) -> None:
        """
        Args:
            base_path: SAVEディレクトリの親パス（デフォルトは02_tutorial/）
        """
        if base_path is None:
            # このファイルから02_tutorial/を見つける
            base_path = Path(__file__).parent.parent.parent
        self.base_path = Path(base_path)
        self.saves_path = self.base_path / "saves"
        self.templates_path = self.base_path / "templates"

    def get_slot_path(self, slot: SlotName) -> Path:
        """スロットのパスを取得"""
        return self.saves_path / f"SAVE_{slot}"

    def get_slot_status(self, slot: SlotName) -> SlotStatus:
        """スロットの状態を取得"""
        slot_path = self.get_slot_path(slot)

        if not slot_path.exists():
            return SlotStatus(name=slot, exists=False, ready=False)

        meta_path = slot_path / "meta.json"
        state_path = slot_path / "state.json"

        # ready = state.json と meta.json が両方存在
        ready = meta_path.exists() and state_path.exists()

        created_at = None
        last_played = None
        turn = 0
        loaded_stage = None

        if meta_path.exists():
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
                created_at = meta.get("created_at")
                last_played = meta.get("last_played")
                turn = meta.get("turn", 0)
                loaded_stage = meta.get("loaded_stage")
            except (json.JSONDecodeError, KeyError):
                pass

        return SlotStatus(
            name=slot,
            exists=True,
            ready=ready,
            created_at=created_at,
            last_played=last_played,
            turn=turn,
            loaded_stage=loaded_stage,
        )

    def status(self) -> list[SlotStatus]:
        """全スロットの状態を取得"""
        return [self.get_slot_status(slot) for slot in SLOTS]

    def setup(self, slot: SlotName, stage_id: str | None = None) -> bool:
        """
        スロットをテンプレートから初期化

        Args:
            slot: スロット名
            stage_id: Stage ID（例: "step_01"）。指定時はStageテンプレートを使用。

        設計方針:
            1. まず ingame_default をベースとしてコピー（game.py含む核心部分）
            2. Stage固有ファイル（state.json, ingame/config.py等）で上書き
            3. game.py は ingame_default のものを必ず使用（Stageは上書き不可）

        Returns:
            成功したらTrue
        """
        slot_path = self.get_slot_path(slot)

        # 既に存在する場合は失敗
        if slot_path.exists() and any(slot_path.iterdir()):
            return False

        # ディレクトリ作成
        slot_path.mkdir(parents=True, exist_ok=True)

        # Step 1: ingame_default をベースとしてコピー（核心部分）
        ingame_default = self.templates_path / "ingame_default"
        ingame_dest = slot_path / "ingame"
        if ingame_default.exists():
            shutil.copytree(ingame_default, ingame_dest)

        # Step 2: state.json をデフォルトからコピー
        state_default = self.templates_path / "state_default.json"
        if state_default.exists():
            shutil.copy(state_default, slot_path / "state.json")

        # Step 3: Stage固有ファイルで上書き（指定時のみ）
        if stage_id:
            stage_path = self.templates_path / "stages" / stage_id

            if stage_path.exists():
                # Stage固有のstate.jsonがあれば上書き
                stage_state = stage_path / "state.json"
                if stage_state.exists():
                    shutil.copy(stage_state, slot_path / "state.json")

                # Stage固有のingame/ファイルで上書き（game.py以外）
                stage_ingame = stage_path / "ingame"
                if stage_ingame.exists():
                    for file in stage_ingame.iterdir():
                        # game.py はスキップ（核心部分は上書きしない）
                        if file.name == "game.py":
                            continue
                        dest_file = ingame_dest / file.name
                        if file.is_file():
                            shutil.copy(file, dest_file)
                        elif file.is_dir():
                            if dest_file.exists():
                                shutil.rmtree(dest_file)
                            shutil.copytree(file, dest_file)

        # meta.json を作成（stage.json の情報も含む）
        now = datetime.now().isoformat()
        meta = {
            "created_at": now,
            "last_played": now,
            "turn": 0,
            "slot": slot,
            "loaded_stage": stage_id,
        }

        # stage.json があれば情報を追加
        if stage_id:
            stage_json_path = self.templates_path / "stages" / stage_id / "stage.json"
            if stage_json_path.exists():
                try:
                    stage_info = json.loads(stage_json_path.read_text(encoding="utf-8"))
                    meta["stage_name"] = stage_info.get("name", stage_id)
                    meta["stage_name_ja"] = stage_info.get("name_ja", "")
                    meta["stage_description_ja"] = stage_info.get("description_ja", "")
                    meta["stage_commands"] = stage_info.get("commands", [])
                    meta["stage_help_text"] = stage_info.get("help_text", "")
                    meta["stage_mode"] = stage_info.get("mode", "INTERPRETER")
                    meta["stage_goal"] = stage_info.get("goal", "")
                    meta["stage_examples"] = stage_info.get("examples", [])
                    meta["stage_try_first"] = stage_info.get("try_first", "")
                except json.JSONDecodeError:
                    pass

        (slot_path / "meta.json").write_text(
            json.dumps(meta, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        # log.txt を作成
        stage_name = meta.get("stage_name") or stage_id or "default"
        (slot_path / "log.txt").write_text(
            f"[{now}] SAVE_{slot} initialized with stage: {stage_name}\n",
            encoding="utf-8",
        )

        return True

    def reset(self, slot: SlotName, stage_id: str | None = None) -> bool:
        """
        スロットをテンプレート状態にリセット

        Args:
            slot: スロット名
            stage_id: Stage ID。指定時はそのStageでリセット。
                      未指定時は現在のloaded_stageを使用。

        Returns:
            成功したらTrue
        """
        slot_path = self.get_slot_path(slot)

        if not slot_path.exists():
            return False

        # 未指定の場合は現在のloaded_stageを使用
        if stage_id is None:
            status = self.get_slot_status(slot)
            stage_id = status.loaded_stage

        # 削除して再セットアップ
        shutil.rmtree(slot_path)
        return self.setup(slot, stage_id)

    def delete(self, slot: SlotName) -> bool:
        """
        スロットを削除

        Returns:
            成功したらTrue
        """
        slot_path = self.get_slot_path(slot)

        if not slot_path.exists():
            return False

        shutil.rmtree(slot_path)
        slot_path.mkdir(parents=True, exist_ok=True)  # 空ディレクトリを残す
        return True

    def copy(self, src: SlotName, dest: SlotName) -> bool:
        """
        スロットをコピー

        Returns:
            成功したらTrue
        """
        src_path = self.get_slot_path(src)
        dest_path = self.get_slot_path(dest)

        if not src_path.exists():
            return False

        # 宛先が存在する場合は削除
        if dest_path.exists():
            shutil.rmtree(dest_path)

        # コピー
        shutil.copytree(src_path, dest_path)

        # meta.json を更新
        meta_path = dest_path / "meta.json"
        if meta_path.exists():
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            meta["slot"] = dest
            meta["copied_from"] = src
            meta["copied_at"] = datetime.now().isoformat()
            meta_path.write_text(
                json.dumps(meta, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

        return True

    def is_ready(self, slot: SlotName) -> bool:
        """スロットがプレイ可能かどうか"""
        return self.get_slot_status(slot).ready
