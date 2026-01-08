"""
InGameランナー

SAVEディレクトリからゲームを動的にロードして実行します。
"""

import sys
import importlib.util
from pathlib import Path
from typing import Callable


def run_game(slot_path: Path) -> None:
    """
    SAVEスロットからゲームを実行

    Args:
        slot_path: SAVEディレクトリのパス（例: saves/SAVE_A）
    """
    slot_path = Path(slot_path)
    ingame_dir = slot_path / "ingame"
    game_file = ingame_dir / "game.py"

    if not game_file.exists():
        print(f"Error: {game_file} not found")
        print("Please run 'setup' from Manage Saves menu first.")
        return

    # ingameディレクトリをsys.pathに追加（モジュールインポート用）
    ingame_str = str(ingame_dir)
    if ingame_str not in sys.path:
        sys.path.insert(0, ingame_str)

    # game.pyを動的にロード
    spec = importlib.util.spec_from_file_location("ingame.game", game_file)
    if spec is None or spec.loader is None:
        print(f"Error: Cannot load {game_file}")
        return

    game_module = importlib.util.module_from_spec(spec)

    # ingameパッケージをsys.modulesに追加
    sys.modules["ingame"] = game_module
    sys.modules["ingame.game"] = game_module

    # configもロード
    config_file = ingame_dir / "config.py"
    if config_file.exists():
        config_spec = importlib.util.spec_from_file_location("ingame.config", config_file)
        if config_spec and config_spec.loader:
            config_module = importlib.util.module_from_spec(config_spec)
            sys.modules["ingame.config"] = config_module
            sys.modules["config"] = config_module  # 直接インポート用
            try:
                config_spec.loader.exec_module(config_module)
            except Exception as e:
                print(f"Warning: Error loading config: {e}")

    # game.pyを実行
    try:
        spec.loader.exec_module(game_module)

        # run関数を呼び出し
        if hasattr(game_module, "run"):
            game_module.run(slot_path)
        else:
            print("Error: game.py does not have a 'run' function")

    except Exception as e:
        print(f"Error running game: {e}")
        import traceback
        traceback.print_exc()

    finally:
        # クリーンアップ
        if "ingame" in sys.modules:
            del sys.modules["ingame"]
        if "ingame.game" in sys.modules:
            del sys.modules["ingame.game"]
        if "ingame.config" in sys.modules:
            del sys.modules["ingame.config"]
        if "config" in sys.modules:
            del sys.modules["config"]
        # sys.pathからingameディレクトリを削除
        if ingame_str in sys.path:
            sys.path.remove(ingame_str)
