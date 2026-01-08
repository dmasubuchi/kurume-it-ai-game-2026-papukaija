"""
統合ゲーム本体

Step 01〜08の全機能を統合したゲームエントリーポイント。
SAVEスロットから実行され、DSLコマンドでゲームをプレイします。

使用方法:
    from ingame.game import run
    run(slot_path)
"""

import json
import sys
from pathlib import Path
from dataclasses import asdict
from datetime import datetime

# srcをインポートパスに追加（SAVEディレクトリから実行される場合）
_tutorial_root = Path(__file__).parent.parent.parent
if str(_tutorial_root) not in sys.path:
    sys.path.insert(0, str(_tutorial_root))

from src.core.state import GameState, Entity, Position, create_initial_state
from src.core.game_loop import run_game_loop
from src.core.io import get_input, output
from src.core.renderer import create_game_renderer
from src.dsl.parser import parse
from src.dsl.interpreter import Interpreter, interpret

# AIモジュールをインポート
try:
    import ai as ai_module  # type: ignore
except ImportError:
    ai_module = None

# ローカル設定をインポート（同じディレクトリから）
try:
    from . import config
except ImportError:
    # 直接実行時のフォールバック
    import config  # type: ignore


def load_state(slot_path: Path) -> GameState:
    """state.jsonからGameStateを復元"""
    state_file = slot_path / "state.json"

    if not state_file.exists():
        return create_initial_state(
            map_width=config.MAP_WIDTH,
            map_height=config.MAP_HEIGHT,
            player_start=(config.PLAYER_START_X, config.PLAYER_START_Y),
        )

    data = json.loads(state_file.read_text(encoding="utf-8"))

    # プレイヤー復元
    player_data = data.get("player", {})
    player = Entity(
        id=player_data.get("id", "player"),
        name=player_data.get("name", "Player"),
        pos=Position(
            x=player_data.get("x", config.PLAYER_START_X),
            y=player_data.get("y", config.PLAYER_START_Y),
        ),
        hp=player_data.get("hp", config.PLAYER_START_HP),
    )

    # エンティティ復元
    entities = []
    for e_data in data.get("entities", []):
        entities.append(
            Entity(
                id=e_data.get("id", ""),
                name=e_data.get("name", ""),
                pos=Position(x=e_data.get("x", 0), y=e_data.get("y", 0)),
                hp=e_data.get("hp", 100),
                is_active=e_data.get("is_active", True),
            )
        )

    return GameState(
        player=player,
        entities=tuple(entities),
        turn=data.get("turn", 0),
        score=data.get("score", 0),
        is_game_over=data.get("is_game_over", False),
        map_width=data.get("map_width", config.MAP_WIDTH),
        map_height=data.get("map_height", config.MAP_HEIGHT),
    )


def save_state(state: GameState, slot_path: Path) -> None:
    """GameStateをstate.jsonに保存"""
    state_file = slot_path / "state.json"

    data = {
        "version": "1.0",
        "player": {
            "id": state.player.id,
            "name": state.player.name,
            "x": state.player.pos.x,
            "y": state.player.pos.y,
            "hp": state.player.hp,
        },
        "entities": [
            {
                "id": e.id,
                "name": e.name,
                "x": e.pos.x,
                "y": e.pos.y,
                "hp": e.hp,
                "is_active": e.is_active,
            }
            for e in state.entities
        ],
        "turn": state.turn,
        "score": state.score,
        "is_game_over": state.is_game_over,
        "map_width": state.map_width,
        "map_height": state.map_height,
    }

    state_file.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def update_meta(slot_path: Path, state: GameState) -> None:
    """meta.jsonを更新"""
    meta_file = slot_path / "meta.json"

    if meta_file.exists():
        meta = json.loads(meta_file.read_text(encoding="utf-8"))
    else:
        meta = {"created_at": datetime.now().isoformat()}

    meta["last_played"] = datetime.now().isoformat()
    meta["turn"] = state.turn
    meta["score"] = state.score

    meta_file.write_text(
        json.dumps(meta, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def append_log(slot_path: Path, message: str) -> None:
    """log.txtにメッセージを追加"""
    log_file = slot_path / "log.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")


def execute_ai_turn(state: GameState, interpreter: Interpreter) -> GameState:
    """
    AIターンを実行

    全アクティブエンティティがプレイヤーに向かって移動
    """
    if not ai_module:
        output("AI module not available")
        return state.next_turn()

    current_state = state

    # 各エンティティの行動を決定・実行
    for entity in state.entities:
        if not entity.is_active:
            continue

        # エンティティ情報を辞書形式でAIに渡す
        entity_dict = {
            "name": entity.name,
            "id": entity.id,
            "x": entity.pos.x,
            "y": entity.pos.y,
            "hp": entity.hp,
            "is_active": entity.is_active,
        }

        # ゲーム状態を辞書形式で渡す
        state_dict = {
            "player": {
                "x": current_state.player.pos.x,
                "y": current_state.player.pos.y,
                "hp": current_state.player.hp,
            },
            "entities": [
                {
                    "name": e.name,
                    "id": e.id,
                    "x": e.pos.x,
                    "y": e.pos.y,
                    "is_active": e.is_active,
                }
                for e in current_state.entities
            ],
            "map_width": current_state.map_width,
            "map_height": current_state.map_height,
        }

        # AIに行動を決定させる
        try:
            action = ai_module.decide_action(entity_dict, state_dict)
            if action:
                result = interpreter.execute(parse(action), current_state)
                current_state = result.state
                output(f"  {entity.name}: {action}")
        except Exception as e:
            output(f"  AI error for {entity.name}: {e}")

    return current_state.next_turn()


def create_simple_update(slot_path: Path, meta: dict | None = None):
    """Simple mode用のupdate関数（w/a/s/d移動、WELCOME/STATE/IO/RENDERERモード用）"""
    meta = meta or {}
    stage_commands = meta.get("stage_commands", [])
    stage_help = meta.get("stage_help_text", "")

    # 方向マッピング
    moves = {
        "w": (0, -1), "up": (0, -1),
        "s": (0, 1), "down": (0, 1),
        "a": (-1, 0), "left": (-1, 0),
        "d": (1, 0), "right": (1, 0),
    }

    def update(state: GameState, cmd: str) -> GameState:
        cmd = cmd.strip().lower()

        if cmd == "help":
            output("\n=== Commands ===")
            if stage_commands:
                for cmd_text in stage_commands:
                    output(f"  {cmd_text}")
            else:
                output("  w/a/s/d  - Move (up/left/down/right)")
                output("  status   - Show status")
                output("  save     - Save game")
                output("  quit     - Exit")
            if stage_help:
                output("")
                output(stage_help)
            output("")
            return state

        if cmd == "status":
            output(f"\nTurn: {state.turn}")
            output(f"Position: ({state.player.pos.x}, {state.player.pos.y})")
            output(f"HP: {state.player.hp}")
            output("")
            return state

        if cmd == "save":
            save_state(state, slot_path)
            update_meta(slot_path, state)
            output("Game saved.")
            return state

        # 移動コマンド
        if cmd in moves:
            dx, dy = moves[cmd]
            new_state = state.move_player(dx, dy).next_turn()

            if config.AUTO_SAVE:
                save_state(new_state, slot_path)
                update_meta(slot_path, new_state)

            return new_state.add_log(f"Moved to ({new_state.player.pos.x}, {new_state.player.pos.y})")

        output(f"Unknown command: {cmd}")
        output("Type 'help' for commands.")
        return state

    return update


def create_loop_update(slot_path: Path, meta: dict | None = None):
    """LOOP mode用のupdate関数（カウンター増減）"""
    meta = meta or {}
    stage_commands = meta.get("stage_commands", [])
    stage_help = meta.get("stage_help_text", "")

    def update(state: GameState, cmd: str) -> GameState:
        cmd = cmd.strip().lower()

        if cmd == "help":
            output("\n=== Commands ===")
            if stage_commands:
                for cmd_text in stage_commands:
                    output(f"  {cmd_text}")
            else:
                output("  up / +   - Increment score")
                output("  down / - - Decrement score")
                output("  reset    - Reset score to 0")
                output("  status   - Show status")
                output("  quit     - Exit")
            if stage_help:
                output("")
                output(stage_help)
            output("")
            return state

        if cmd == "status":
            output(f"\nTurn: {state.turn}")
            output(f"Score: {state.score}")
            output("")
            return state

        if cmd in ("up", "+"):
            new_state = state.replace(score=state.score + 1).next_turn()
            output(f"Score: {new_state.score}")
            return new_state

        if cmd in ("down", "-"):
            new_state = state.replace(score=state.score - 1).next_turn()
            output(f"Score: {new_state.score}")
            return new_state

        if cmd == "reset":
            new_state = state.replace(score=0).next_turn()
            output("Score reset to 0")
            return new_state

        output(f"Unknown command: {cmd}")
        return state

    return update


def create_dsl_update(slot_path: Path, interpreter: Interpreter, meta: dict | None = None, show_tokens: bool = False, show_ast: bool = False):
    """DSL mode用のupdate関数（LEXER/PARSER/INTERPRETERモード用）"""
    meta = meta or {}
    stage_commands = meta.get("stage_commands", [])
    stage_help = meta.get("stage_help_text", "")

    # Lexerが必要な場合
    if show_tokens:
        from src.dsl.lexer import tokenize

    def update(state: GameState, cmd: str) -> GameState:
        cmd = cmd.strip()

        if cmd == "help":
            output("\n=== Commands ===")
            if stage_commands:
                for cmd_text in stage_commands:
                    output(f"  {cmd_text}")
            else:
                output("  move player <dx> <dy> - Move player")
                output("  spawn <type> <x> <y>  - Spawn entity")
                output("  destroy <target>      - Destroy entity")
                output("  set <entity>.<prop> <value>")
                output("  if <condition> then <action>")
                output("  wait                  - AI turn")
                output("  status / save / quit")
            if stage_help:
                output("")
                output(stage_help)
            output("")
            return state

        if cmd == "status":
            output(f"\nTurn: {state.turn}")
            output(f"Score: {state.score}")
            output(f"Player: ({state.player.pos.x}, {state.player.pos.y}) HP={state.player.hp}")
            output(f"Entities: {len(state.entities)}")
            output("")
            return state

        if cmd == "save":
            save_state(state, slot_path)
            update_meta(slot_path, state)
            output("Game saved.")
            return state

        if cmd == "wait":
            return execute_ai_turn(state, interpreter)

        # DSLコマンドを実行
        try:
            # トークン表示
            if show_tokens:
                tokens = tokenize(cmd)
                output("\n[Tokens]")
                for tok in tokens:
                    output(f"  {tok}")
                output("")

            # AST生成
            ast = parse(cmd)

            # AST表示
            if show_ast:
                output("\n[AST]")
                output(f"  {ast}")
                output("")

            # 実行
            result = interpreter.execute(ast, state)
            new_state = result.state.next_turn()

            for error in result.errors:
                output(f"Error: {error.message}")

            if config.DEBUG:
                for log in result.logs:
                    output(f"  {log}")

            if config.AUTO_SAVE:
                save_state(new_state, slot_path)
                update_meta(slot_path, new_state)

            return new_state

        except Exception as e:
            output(f"Error: {e}")
            return state

    return update


def create_update(slot_path: Path, interpreter: Interpreter, meta: dict | None = None):
    """modeに応じたupdate関数を作成"""
    meta = meta or {}
    mode = meta.get("stage_mode", "INTERPRETER")

    # Simple modes (w/a/s/d 移動)
    if mode in ("WELCOME", "STATE", "IO", "RENDERER"):
        return create_simple_update(slot_path, meta)

    # Loop mode (カウンター)
    if mode == "LOOP":
        return create_loop_update(slot_path, meta)

    # Lexer demo mode (トークン表示 + 実行)
    if mode == "LEXER":
        return create_dsl_update(slot_path, interpreter, meta, show_tokens=True, show_ast=False)

    # Parser demo mode (AST表示 + 実行)
    if mode == "PARSER":
        return create_dsl_update(slot_path, interpreter, meta, show_tokens=False, show_ast=True)

    # Interpreter mode (通常のDSL実行)
    return create_dsl_update(slot_path, interpreter, meta, show_tokens=False, show_ast=False)


def load_meta(slot_path: Path) -> dict:
    """meta.jsonを読み込み"""
    meta_file = slot_path / "meta.json"
    if meta_file.exists():
        try:
            return json.loads(meta_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {}


def run(slot_path: Path) -> None:
    """ゲームを実行"""
    slot_path = Path(slot_path)

    # meta.jsonからStage情報を取得
    meta = load_meta(slot_path)
    stage_name = meta.get("stage_name") or meta.get("loaded_stage") or "Game"
    stage_name_ja = meta.get("stage_name_ja", "")
    stage_help = meta.get("stage_help_text", "")
    stage_mode = meta.get("stage_mode", "INTERPRETER")

    print()
    print("=" * 50)
    print(f"  {stage_name}")
    if stage_name_ja:
        print(f"  {stage_name_ja}")
    print(f"  Mode: {stage_mode}")
    print("=" * 50)
    print(f"SAVE: {slot_path.name}")
    if stage_help:
        print()
        print(stage_help)
    print()
    print("Type 'help' for commands, 'quit' to exit")
    print()

    # 状態読み込み
    state = load_state(slot_path)
    append_log(slot_path, "Game started")

    # レンダラー作成
    render = create_game_renderer(
        char_mapping=config.CHAR_MAPPING,
        show_status=True,
        show_log=True,
    )

    # インタプリタ作成
    interpreter = Interpreter()

    # update関数作成（meta情報を渡す）
    update = create_update(slot_path, interpreter, meta)

    # ゲームループ実行
    def game_get_input() -> str:
        try:
            return input("CMD> ").strip()
        except EOFError:
            return "quit"

    final_state = run_game_loop(
        initial_state=state,
        get_input=game_get_input,
        update=update,
        render=render,
        output=output,
        quit_commands=("quit", "exit", "q"),
    )

    # 最終保存
    save_state(final_state, slot_path)
    update_meta(slot_path, final_state)
    append_log(slot_path, f"Game ended. Turn: {final_state.turn}, Score: {final_state.score}")

    print()
    print(f"Game saved. Turn: {final_state.turn}, Score: {final_state.score}")
    print()


if __name__ == "__main__":
    # 直接実行時のテスト
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        run(Path(tmpdir))
