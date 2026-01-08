"""
Stage Discovery and Management

templates/stages/ からStageを探索し、メタデータを提供します。
"""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class StageInfo:
    """Stage metadata"""

    id: str
    name: str
    name_ja: str
    description: str
    description_ja: str
    commands: tuple[str, ...]
    help_text: str
    path: Path
    has_ingame: bool
    has_state: bool


DEFAULT_STAGE_META = {
    "id": "unknown",
    "name": "Unknown Stage",
    "name_ja": "不明なステージ",
    "description": "No description available",
    "description_ja": "説明がありません",
    "commands": ["quit"],
    "help_text": "Type 'quit' to exit.",
}


class StageManager:
    """Stage discovery and management"""

    def __init__(self, base_path: Path | None = None) -> None:
        if base_path is None:
            base_path = Path(__file__).parent.parent.parent
        self.base_path = Path(base_path)
        self.stages_path = self.base_path / "templates" / "stages"

    def discover_stages(self) -> list[StageInfo]:
        """
        Scan for available stages.

        Returns:
            List of StageInfo, sorted by stage ID
        """
        stages = []

        if not self.stages_path.exists():
            return stages

        for stage_dir in sorted(self.stages_path.iterdir()):
            if stage_dir.is_dir() and stage_dir.name.startswith("step_"):
                info = self._load_stage_info(stage_dir)
                if info:
                    stages.append(info)

        return stages

    def _load_stage_info(self, stage_dir: Path) -> Optional[StageInfo]:
        """Load stage info from directory"""
        stage_json = stage_dir / "stage.json"

        if stage_json.exists():
            try:
                meta = json.loads(stage_json.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                meta = DEFAULT_STAGE_META.copy()
                meta["id"] = stage_dir.name
        else:
            meta = DEFAULT_STAGE_META.copy()
            meta["id"] = stage_dir.name
            meta["name"] = stage_dir.name.replace("_", " ").title()

        return StageInfo(
            id=meta.get("id", stage_dir.name),
            name=meta.get("name", stage_dir.name),
            name_ja=meta.get("name_ja", meta.get("name", "")),
            description=meta.get("description", ""),
            description_ja=meta.get("description_ja", ""),
            commands=tuple(meta.get("commands", ["quit"])),
            help_text=meta.get("help_text", ""),
            path=stage_dir,
            has_ingame=(stage_dir / "ingame").exists(),
            has_state=(stage_dir / "state.json").exists(),
        )

    def get_stage(self, stage_id: str) -> Optional[StageInfo]:
        """
        Get specific stage by ID.

        Args:
            stage_id: Stage identifier (e.g., "step_01")

        Returns:
            StageInfo if found, None otherwise
        """
        for stage in self.discover_stages():
            if stage.id == stage_id:
                return stage
        return None

    def get_stage_path(self, stage_id: str) -> Path | None:
        """
        Get path to stage directory.

        Args:
            stage_id: Stage identifier

        Returns:
            Path to stage directory if exists
        """
        stage = self.get_stage(stage_id)
        if stage:
            return stage.path
        return None
