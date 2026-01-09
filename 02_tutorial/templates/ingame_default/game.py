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


def create_lexer_update(slot_path: Path, meta: dict | None = None):
    """LEXER mode用のupdate関数（トークン表示のみ、実行しない）"""
    from src.dsl.lexer import tokenize, tokenize_with_errors

    meta = meta or {}
    stage_help = meta.get("stage_help_text", "")
    stage_goal = meta.get("stage_goal", "")
    stage_examples = meta.get("stage_examples", [])

    def update(state: GameState, cmd: str) -> GameState:
        cmd = cmd.strip()

        # メタコマンド
        if cmd == "help":
            output("\n=== Commands ===")
            output("  <DSL>     - DSLを入力してトークン化")
            output("  examples  - サンプルDSLを表示")
            output("  goal      - このStageの目的")
            output("  quit      - 終了")
            if stage_help:
                output("")
                output(stage_help)
            output("")
            return state

        if cmd == "goal":
            output(f"\n[Goal] {stage_goal}")
            output("※ このStageでは実行しません。トークン化のみです。")
            output("")
            return state

        if cmd == "examples":
            output("\n=== Sample DSL ===")
            for i, ex in enumerate(stage_examples, 1):
                output(f"  {i}. {ex}")
            output("\n上記をコピーして入力してみてください")
            output("")
            return state

        # ゲーム操作入力への警告
        if cmd.lower() in ("w", "a", "s", "d", "up", "down", "left", "right"):
            output(f"\n[Warning] '{cmd}' はゲーム操作です。")
            output("このStageではDSLコマンドを入力してください。")
            output("例: move player 5 3")
            output("'examples' でサンプルを確認できます。")
            output("")
            return state

        # DSLをトークン化（実行しない）
        output(f"\n[Source]")
        output(f"  {cmd}")

        tokens, errors = tokenize_with_errors(cmd)

        output("\n[Tokens]")
        for tok in tokens:
            if str(tok.type) not in ("TokenType.EOF", "TokenType.NEWLINE"):
                output(f"  {tok}")

        if errors:
            output("\n[Errors]")
            for err in errors:
                output(f"  Line {err.line}, Col {err.column}: {err.message}")

        output("\n※ 実行はしません。トークン化のみです。")
        output("")
        return state  # 状態は変更しない

    return update


def create_parser_update(slot_path: Path, meta: dict | None = None):
    """PARSER mode用のupdate関数（AST表示のみ、実行しない）"""
    from src.dsl.lexer import tokenize

    meta = meta or {}
    stage_help = meta.get("stage_help_text", "")
    stage_goal = meta.get("stage_goal", "")
    stage_examples = meta.get("stage_examples", [])

    def update(state: GameState, cmd: str) -> GameState:
        cmd = cmd.strip()

        # メタコマンド
        if cmd == "help":
            output("\n=== Commands ===")
            output("  <DSL>     - DSLを入力してAST化")
            output("  examples  - サンプルDSLを表示")
            output("  goal      - このStageの目的")
            output("  quit      - 終了")
            if stage_help:
                output("")
                output(stage_help)
            output("")
            return state

        if cmd == "goal":
            output(f"\n[Goal] {stage_goal}")
            output("※ このStageでは実行しません。AST生成のみです。")
            output("")
            return state

        if cmd == "examples":
            output("\n=== Sample DSL ===")
            for i, ex in enumerate(stage_examples, 1):
                output(f"  {i}. {ex}")
            output("\n上記をコピーして入力してみてください")
            output("")
            return state

        # ゲーム操作入力への警告
        if cmd.lower() in ("w", "a", "s", "d", "up", "down", "left", "right"):
            output(f"\n[Warning] '{cmd}' はゲーム操作です。")
            output("このStageではDSLコマンドを入力してください。")
            output("例: if player.hp < 50 then set player.state danger")
            output("'examples' でサンプルを確認できます。")
            output("")
            return state

        # DSLをパース（実行しない）
        output(f"\n[Source]")
        output(f"  {cmd}")

        try:
            # トークン化
            tokens = tokenize(cmd)
            output("\n[Tokens]")
            for tok in tokens:
                if str(tok.type) not in ("TokenType.EOF", "TokenType.NEWLINE"):
                    output(f"  {tok}")

            # AST生成
            ast = parse(cmd)
            output("\n[AST]")
            output(f"  {ast}")

        except Exception as e:
            output(f"\n[ParseError] {e}")

        output("\n※ 実行はしません。AST生成のみです。")
        output("")
        return state  # 状態は変更しない

    return update


def create_interpreter_update(slot_path: Path, interpreter: Interpreter, meta: dict | None = None):
    """INTERPRETER mode用のupdate関数（フル実行）"""
    meta = meta or {}
    stage_commands = meta.get("stage_commands", [])
    stage_help = meta.get("stage_help_text", "")
    stage_goal = meta.get("stage_goal", "")
    stage_examples = meta.get("stage_examples", [])

    def update(state: GameState, cmd: str) -> GameState:
        cmd = cmd.strip()

        if cmd == "help":
            output("\n=== Commands ===")
            if stage_commands:
                for cmd_text in stage_commands:
                    output(f"  {cmd_text}")
            else:
                output("  move player <x> <y>   - 座標に移動")
                output("  spawn <type> <x> <y>  - エンティティ生成")
                output("  destroy <target>      - エンティティ削除")
                output("  set <entity>.<prop> <value>")
                output("  wait                  - AIターン")
                output("  examples / goal / status / quit")
            if stage_help:
                output("")
                output(stage_help)
            output("")
            return state

        if cmd == "goal":
            output(f"\n[Goal] {stage_goal}")
            output("※ このStageでは実行されます！Stateが変わります。")
            output("")
            return state

        if cmd == "examples":
            output("\n=== Sample DSL ===")
            for i, ex in enumerate(stage_examples, 1):
                output(f"  {i}. {ex}")
            output("\n上記をコピーして入力してみてください")
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
            ast = parse(cmd)
            result = interpreter.execute(ast, state)
            new_state = result.state.next_turn()

            # 実行結果を表示
            output(f"\n[Execute] {cmd}")
            output(f"  Player: ({new_state.player.pos.x}, {new_state.player.pos.y})")

            for error in result.errors:
                output(f"[RuntimeError] {error.message}")

            if config.DEBUG:
                for log in result.logs:
                    output(f"  {log}")

            if config.AUTO_SAVE:
                save_state(new_state, slot_path)
                update_meta(slot_path, new_state)

            return new_state

        except Exception as e:
            output(f"[Error] {e}")
            output("'help' でコマンド一覧、'examples' でサンプルを確認できます。")
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

    # Lexer mode (トークン表示のみ、実行しない)
    if mode == "LEXER":
        return create_lexer_update(slot_path, meta)

    # Parser mode (AST表示のみ、実行しない)
    if mode == "PARSER":
        return create_parser_update(slot_path, meta)

    # Interpreter mode (フル実行)
    return create_interpreter_update(slot_path, interpreter, meta)


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
    stage_goal = meta.get("stage_goal", "")
    stage_try_first = meta.get("stage_try_first", "")
    stage_examples = meta.get("stage_examples", [])

    # ガイド画面表示
    print()
    print("=" * 50)
    print(f"  {stage_name}")
    if stage_name_ja:
        print(f"  {stage_name_ja}")
    print(f"  Mode: {stage_mode}")
    print("=" * 50)
    print(f"SAVE: {slot_path.name}")

    # Goal表示
    if stage_goal:
        print()
        print(f"Goal: {stage_goal}")

    # Try First表示
    if stage_try_first:
        print()
        print("Try:")
        print(f"  {stage_try_first}")

    # Examples表示（最初の3つ）
    if stage_examples and len(stage_examples) > 1:
        print()
        print("Examples:")
        for ex in stage_examples[:3]:
            print(f"  {ex}")
        if len(stage_examples) > 3:
            print(f"  ... ('examples' で全て表示)")

    # Commands表示
    print()
    print("Commands:")
    if stage_mode in ("LEXER", "PARSER"):
        print("  <DSL>     - DSLを入力")
        print("  examples  - サンプルDSL表示")
        print("  goal      - このStageの目的")
        print("  quit      - 終了")
    else:
        print("  help      - コマンド一覧")
        print("  examples  - サンプル表示")
        print("  quit      - 終了")

    print()
    print("=" * 50)
    print()

    # 状態読み込み
    state = load_state(slot_path)
    append_log(slot_path, "Game started")

    # レンダラー作成（LEXER/PARSERモードでは簡略化）
    if stage_mode in ("LEXER", "PARSER"):
        # LEXER/PARSERモードではTextGridを表示しない
        render = lambda s: ""
    else:
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
