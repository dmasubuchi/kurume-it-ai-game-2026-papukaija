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

        if meta_path.exists():
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
                created_at = meta.get("created_at")
                last_played = meta.get("last_played")
                turn = meta.get("turn", 0)
            except (json.JSONDecodeError, KeyError):
                pass

        return SlotStatus(
            name=slot,
            exists=True,
            ready=ready,
            created_at=created_at,
            last_played=last_played,
            turn=turn,
        )

    def status(self) -> list[SlotStatus]:
        """全スロットの状態を取得"""
        return [self.get_slot_status(slot) for slot in SLOTS]

    def setup(self, slot: SlotName) -> bool:
        """
        スロットをテンプレートから初期化

        Returns:
            成功したらTrue
        """
        slot_path = self.get_slot_path(slot)

        # 既に存在する場合は失敗
        if slot_path.exists() and any(slot_path.iterdir()):
            return False

        # ディレクトリ作成
        slot_path.mkdir(parents=True, exist_ok=True)

        # テンプレートからコピー
        ingame_template = self.templates_path / "ingame_default"
        if ingame_template.exists():
            ingame_dest = slot_path / "ingame"
            shutil.copytree(ingame_template, ingame_dest)

        # state.json をテンプレートからコピー
        state_template = self.templates_path / "state_default.json"
        if state_template.exists():
            shutil.copy(state_template, slot_path / "state.json")

        # meta.json を作成
        now = datetime.now().isoformat()
        meta = {
            "created_at": now,
            "last_played": now,
            "turn": 0,
            "slot": slot,
        }
        (slot_path / "meta.json").write_text(
            json.dumps(meta, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        # log.txt を作成
        (slot_path / "log.txt").write_text(
            f"[{now}] SAVE_{slot} initialized\n",
            encoding="utf-8",
        )

        return True

    def reset(self, slot: SlotName) -> bool:
        """
        スロットをテンプレート状態にリセット

        Returns:
            成功したらTrue
        """
        slot_path = self.get_slot_path(slot)

        if not slot_path.exists():
            return False

        # 削除して再セットアップ
        shutil.rmtree(slot_path)
        return self.setup(slot)

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
