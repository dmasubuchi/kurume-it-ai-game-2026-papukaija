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
from src.algorithms.pathfinding import find_path, manhattan_distance, DIRECTIONS_4
from src.core.renderer import TextGrid, add_border

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


# =====================
# Friendly Input Guide
# =====================

# 自然言語入力の変換マップ
NATURAL_INPUT_MAP = {
    "go right": "d",
    "move right": "d",
    "right": "d",
    "go left": "a",
    "move left": "a",
    "left": "a",
    "go up": "w",
    "move up": "w",
    "up": "w",
    "go down": "s",
    "move down": "s",
    "down": "s",
}


def show_input_guide(cmd: str, input_mode: str, stage_mode: str) -> bool:
    """
    入力ガイドを表示する。
    Returns: True if guide was shown (unknown command), False otherwise
    """
    cmd_lower = cmd.lower().strip()

    # 自然言語入力の救済
    if cmd_lower in NATURAL_INPUT_MAP:
        correct = NATURAL_INPUT_MAP[cmd_lower]
        output(f"\nInput not recognized: {cmd}")
        output("")
        output(f"Hint: To {cmd_lower.replace('go ', '').replace('move ', '')}:")
        output(f"  Type: {correct}")
        output("")
        return True

    # GAMEモードでDSLっぽい入力が来た場合
    if input_mode == "GAME":
        # DSLっぽいパターンをチェック
        dsl_patterns = ["move ", "spawn ", "destroy ", "set ", "if ", "goto "]
        is_dsl_like = any(cmd_lower.startswith(p) for p in dsl_patterns)

        if is_dsl_like:
            output(f"\nInput not recognized: {cmd}")
            output("")
            output("This Step uses game controls, not DSL commands.")
            output("")
            output("Game controls:")
            output("  w / a / s / d  : move player")
            output("  wait           : observe AI behavior")
            output("")
            output("If you want to use DSL commands,")
            output("please select Step 07 (Interpreter) or Step 13 (Integration).")
            output("")
            return True

        # 通常のunknown
        output(f"\nInput not recognized: {cmd}")
        output("")
        output("This Step uses these commands:")
        output("  w / a / s / d  : move player")
        output("  wait           : observe AI")

        # モード固有のヒント
        if stage_mode == "FSM":
            output("  ai             : show FSM debug")
        elif stage_mode == "BT":
            output("  bt             : show BT structure")
        elif stage_mode == "GOAP":
            output("  goap           : show GOAP debug")
        elif stage_mode == "DIRECTOR":
            output("  director       : show tension status")
        elif stage_mode == "PATHFINDING":
            output("  path x y       : show path")
            output("  goto x y       : start auto-move")

        output("")
        output("Type 'help' for all commands.")
        output("")
        return True

    # DSLモードでゲーム操作が来た場合
    if input_mode == "DSL":
        game_controls = ["w", "a", "s", "d", "up", "down", "left", "right"]
        if cmd_lower in game_controls:
            output(f"\nInput not recognized: {cmd}")
            output("")
            output("This Step uses DSL input, not game controls.")
            output("")
            output("Example DSL commands:")
            output("  move player 5 3")
            output("  spawn enemy 10 5")
            output("  if player.hp < 50 then set player.state danger")
            output("")
            output("Type 'examples' to see more.")
            output("")
            return True

        # 通常のunknown
        output(f"\nInput not recognized: {cmd}")
        output("")
        output("This Step uses DSL commands.")
        output("Type 'examples' to see sample DSL commands.")
        output("")
        return True

    # MIXEDモード
    if input_mode == "MIXED":
        output(f"\nInput not recognized: {cmd}")
        output("")
        output("This Step accepts both game controls and DSL:")
        output("  w / a / s / d  : move player (shortcut)")
        output("  dsl <cmd>      : execute DSL directly")
        output("")
        output("Type 'help' for all commands.")
        output("")
        return True

    return False


def get_hint_text(input_mode: str, stage_mode: str) -> str:
    """ヒントテキストを取得"""
    if input_mode == "DSL":
        return "Hint: type 'examples' to see DSL samples"

    if input_mode == "MIXED":
        return "Hint: use 'dsl <cmd>' or w/a/s/d, type 'help' for all"

    # GAME mode
    if stage_mode == "PATHFINDING":
        return "Hint: type 'goto x y' for auto-move, or w/a/s/d"
    return "Hint: type 'wait' to observe AI, or w/a/s/d to move"


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
        entity = Entity(
            id=e_data.get("id", ""),
            name=e_data.get("name", ""),
            pos=Position(x=e_data.get("x", 0), y=e_data.get("y", 0)),
            hp=e_data.get("hp", 100),
            is_active=e_data.get("is_active", True),
        )
        # FSM状態を拡張属性として設定（frozen dataclass対応）
        if "fsm_state" in e_data:
            object.__setattr__(entity, 'fsm_state', e_data.get("fsm_state", "IDLE"))
        entities.append(entity)

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
                **({"fsm_state": e.fsm_state} if hasattr(e, 'fsm_state') else {}),
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
    stage_input_mode = meta.get("stage_input_mode", "GAME")
    stage_mode = meta.get("stage_mode", "WELCOME")

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

        show_input_guide(cmd, stage_input_mode, stage_mode)
        return state

    return update


def create_loop_update(slot_path: Path, meta: dict | None = None):
    """LOOP mode用のupdate関数（カウンター増減）"""
    meta = meta or {}
    stage_commands = meta.get("stage_commands", [])
    stage_help = meta.get("stage_help_text", "")
    stage_input_mode = meta.get("stage_input_mode", "GAME")
    stage_mode = meta.get("stage_mode", "LOOP")

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

        show_input_guide(cmd, stage_input_mode, stage_mode)
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


def create_pathfinding_update(slot_path: Path, interpreter: Interpreter, meta: dict | None = None):
    """PATHFINDING mode用のupdate関数（A*経路探索 + MOVE命令実行）"""
    meta = meta or {}
    stage_commands = meta.get("stage_commands", [])
    stage_help = meta.get("stage_help_text", "")
    stage_goal = meta.get("stage_goal", "")
    stage_examples = meta.get("stage_examples", [])
    stage_input_mode = meta.get("stage_input_mode", "GAME")
    stage_mode = meta.get("stage_mode", "PATHFINDING")

    # 移動キュー（自動移動用）
    move_queue: list[tuple[int, int]] = []

    # 方向マッピング（手動移動用）
    moves = {
        "w": (0, -1), "up": (0, -1),
        "s": (0, 1), "down": (0, 1),
        "a": (-1, 0), "left": (-1, 0),
        "d": (1, 0), "right": (1, 0),
    }

    def get_obstacles(state: GameState) -> set[tuple[int, int]]:
        """Stateから障害物座標を取得"""
        obstacles = set()
        for entity in state.entities:
            if entity.is_active and entity.id in ("wall", "obstacle"):
                obstacles.add((entity.pos.x, entity.pos.y))
        return obstacles

    def is_walkable(state: GameState, x: int, y: int) -> bool:
        """通行可能かチェック"""
        if not (0 <= x < state.map_width and 0 <= y < state.map_height):
            return False
        obstacles = get_obstacles(state)
        return (x, y) not in obstacles

    def path_to_moves(path: tuple[Position, ...]) -> list[tuple[int, int]]:
        """経路をMOVE命令（dx, dy）のリストに変換"""
        moves_list = []
        for i in range(1, len(path)):
            dx = path[i].x - path[i-1].x
            dy = path[i].y - path[i-1].y
            moves_list.append((dx, dy))
        return moves_list

    def render_path(state: GameState, path: tuple[Position, ...]) -> str:
        """経路を可視化したTextGridを生成"""
        grid = TextGrid(width=state.map_width, height=state.map_height, fill=".")

        # 障害物
        for entity in state.entities:
            if entity.is_active:
                char = config.CHAR_MAPPING.get(entity.id, "?")
                grid.set(entity.pos.x, entity.pos.y, char)

        # 経路（*で表示）
        for pos in path:
            grid.set(pos.x, pos.y, "*")

        # ゴール（経路の最後）
        if path:
            grid.set(path[-1].x, path[-1].y, "G")

        # プレイヤー（優先）
        grid.set(state.player.pos.x, state.player.pos.y, "@")

        bordered = add_border(grid)
        return bordered.render()

    def update(state: GameState, cmd: str) -> GameState:
        nonlocal move_queue
        cmd = cmd.strip().lower()

        # ヘルプ
        if cmd == "help":
            output("\n=== Commands ===")
            if stage_commands:
                for cmd_text in stage_commands:
                    output(f"  {cmd_text}")
            else:
                output("  w/a/s/d         - 手動で1歩移動")
                output("  path <x> <y>    - 経路を表示（実行しない）")
                output("  goto <x> <y>    - 自動移動開始（A*経路）")
                output("  cancel          - 自動移動を中断")
                output("  spawn wall <x> <y> - 壁を生成")
                output("  status / examples / goal / quit")
            if stage_help:
                output("")
                output(stage_help)
            output("")
            return state

        if cmd == "goal":
            output(f"\n[Goal] {stage_goal}")
            output("")
            return state

        if cmd == "examples":
            output("\n=== Sample Commands ===")
            for i, ex in enumerate(stage_examples, 1):
                output(f"  {i}. {ex}")
            output("")
            return state

        if cmd == "status":
            auto_status = f"ON (remaining: {len(move_queue)})" if move_queue else "OFF"
            output(f"\nTurn: {state.turn}")
            output(f"Player: ({state.player.pos.x}, {state.player.pos.y})")
            output(f"HP: {state.player.hp}")
            output(f"AutoMove: {auto_status}")
            output(f"Entities: {len(state.entities)}")
            output("")
            return state

        if cmd == "save":
            save_state(state, slot_path)
            update_meta(slot_path, state)
            output("Game saved.")
            return state

        # cancel: 自動移動を中断
        if cmd == "cancel":
            if move_queue:
                output(f"\n[Cancel] AutoMove stopped. Remaining {len(move_queue)} moves discarded.")
                move_queue = []
            else:
                output("\n[Cancel] No auto-move in progress.")
            output("")
            return state

        # path x y: 経路を表示（実行しない）
        if cmd.startswith("path "):
            parts = cmd.split()
            if len(parts) != 3:
                output("\n[Error] Usage: path <x> <y>")
                output("")
                return state

            try:
                goal_x, goal_y = int(parts[1]), int(parts[2])
            except ValueError:
                output("\n[Error] x and y must be integers")
                output("")
                return state

            # 範囲チェック
            if not (0 <= goal_x < state.map_width and 0 <= goal_y < state.map_height):
                output(f"\n[Error] ({goal_x}, {goal_y}) is out of map bounds")
                output("")
                return state

            # A*で経路探索
            start = state.player.pos
            goal = Position(x=goal_x, y=goal_y)

            def walkable_checker(x: int, y: int) -> bool:
                return is_walkable(state, x, y)

            result = find_path(
                start, goal, walkable_checker,
                state.map_width, state.map_height,
                allow_diagonal=False,
                heuristic=manhattan_distance
            )

            if result.found:
                output(f"\n[Path] Found: length={len(result.path)}, cost={result.cost:.0f}")
                output(f"  From: ({start.x}, {start.y})")
                output(f"  To:   ({goal_x}, {goal_y})")
                output("")
                output(render_path(state, result.path))
                output("")
                output("※ 経路表示のみ。移動するには 'goto' を使用してください。")
            else:
                output(f"\n[Path] No path to ({goal_x}, {goal_y})")
                output(f"  Explored: {result.explored_count} nodes")

            output("")
            return state  # 状態は変更しない

        # goto x y: 自動移動開始
        if cmd.startswith("goto "):
            parts = cmd.split()
            if len(parts) != 3:
                output("\n[Error] Usage: goto <x> <y>")
                output("")
                return state

            try:
                goal_x, goal_y = int(parts[1]), int(parts[2])
            except ValueError:
                output("\n[Error] x and y must be integers")
                output("")
                return state

            # 範囲チェック
            if not (0 <= goal_x < state.map_width and 0 <= goal_y < state.map_height):
                output(f"\n[Error] ({goal_x}, {goal_y}) is out of map bounds")
                output("")
                return state

            # 既に自動移動中ならキャンセル
            if move_queue:
                output(f"[Info] Previous auto-move cancelled.")
                move_queue = []

            # A*で経路探索
            start = state.player.pos
            goal = Position(x=goal_x, y=goal_y)

            def walkable_checker(x: int, y: int) -> bool:
                return is_walkable(state, x, y)

            result = find_path(
                start, goal, walkable_checker,
                state.map_width, state.map_height,
                allow_diagonal=False,
                heuristic=manhattan_distance
            )

            if not result.found:
                output(f"\n[Goto] No path to ({goal_x}, {goal_y})")
                output("")
                return state

            # MOVE命令列を生成してキューに追加
            move_queue = path_to_moves(result.path)

            output(f"\n[Goto] Path found: length={len(result.path)}, cost={result.cost:.0f}")
            output(f"  Queued moves: {len(move_queue)}")

            # 最初の5手を表示
            preview = move_queue[:5]
            preview_str = ", ".join([f"({dx},{dy})" for dx, dy in preview])
            if len(move_queue) > 5:
                preview_str += f", ... (+{len(move_queue)-5} more)"
            output(f"  First moves: {preview_str}")
            output("")

            # 最初の1手を実行
            if move_queue:
                dx, dy = move_queue.pop(0)
                new_state = state.move_player(dx, dy).next_turn()
                remaining = len(move_queue)
                output(f"[AutoMove] Step 1: move ({dx}, {dy}) → ({new_state.player.pos.x}, {new_state.player.pos.y})")
                if remaining > 0:
                    output(f"  Remaining: {remaining} moves (press Enter to continue, 'cancel' to stop)")
                else:
                    output(f"  Destination reached!")
                output("")

                if config.AUTO_SAVE:
                    save_state(new_state, slot_path)
                    update_meta(slot_path, new_state)

                return new_state

            return state

        # 空入力: 自動移動を1手進める
        if cmd == "" and move_queue:
            dx, dy = move_queue.pop(0)
            new_state = state.move_player(dx, dy).next_turn()
            step_num = state.turn + 1
            remaining = len(move_queue)
            output(f"[AutoMove] Step {step_num}: move ({dx}, {dy}) → ({new_state.player.pos.x}, {new_state.player.pos.y})")
            if remaining > 0:
                output(f"  Remaining: {remaining} moves")
            else:
                output(f"  Destination reached!")
            output("")

            if config.AUTO_SAVE:
                save_state(new_state, slot_path)
                update_meta(slot_path, new_state)

            return new_state

        # 手動移動 (w/a/s/d)
        if cmd in moves:
            dx, dy = moves[cmd]
            new_x = state.player.pos.x + dx
            new_y = state.player.pos.y + dy

            if not is_walkable(state, new_x, new_y):
                output(f"\n[Blocked] Cannot move to ({new_x}, {new_y})")
                output("")
                return state

            new_state = state.move_player(dx, dy).next_turn()

            # 自動移動中なら中断
            if move_queue:
                output(f"[Info] Manual move - auto-move cancelled ({len(move_queue)} moves discarded)")
                move_queue = []

            if config.AUTO_SAVE:
                save_state(new_state, slot_path)
                update_meta(slot_path, new_state)

            return new_state

        # spawn wall x y (壁を追加)
        if cmd.startswith("spawn "):
            parts = cmd.split()
            if len(parts) != 4:
                output("\n[Error] Usage: spawn <type> <x> <y>")
                output("")
                return state

            entity_type = parts[1]
            try:
                ex, ey = int(parts[2]), int(parts[3])
            except ValueError:
                output("\n[Error] x and y must be integers")
                output("")
                return state

            # 新しいエンティティを追加
            new_entity = Entity(
                id=entity_type,
                name=entity_type.capitalize(),
                pos=Position(x=ex, y=ey),
                hp=100,
                is_active=True,
            )
            new_entities = state.entities + (new_entity,)
            new_state = state.replace(entities=new_entities).next_turn()

            output(f"\n[Spawn] Created {entity_type} at ({ex}, {ey})")
            output("")

            if config.AUTO_SAVE:
                save_state(new_state, slot_path)
                update_meta(slot_path, new_state)

            return new_state

        # 未知のコマンド - フレンドリーガイドを表示
        show_input_guide(cmd, stage_input_mode, stage_mode)
        return state

    return update


def create_fsm_update(slot_path: Path, interpreter: Interpreter, meta: dict | None = None):
    """FSM mode用のupdate関数（敵AIがFSMでMOVE命令を生成）"""
    meta = meta or {}
    stage_commands = meta.get("stage_commands", [])
    stage_help = meta.get("stage_help_text", "")
    stage_goal = meta.get("stage_goal", "")
    stage_examples = meta.get("stage_examples", [])
    stage_input_mode = meta.get("stage_input_mode", "GAME")
    stage_mode = meta.get("stage_mode", "FSM")

    # AI有効フラグ
    ai_enabled = [True]  # リストで包んでnonlocal不要に

    # 方向マッピング
    moves = {
        "w": (0, -1), "up": (0, -1),
        "s": (0, 1), "down": (0, 1),
        "a": (-1, 0), "left": (-1, 0),
        "d": (1, 0), "right": (1, 0),
    }

    # FSM閾値（configから取得またはデフォルト）
    CHASE_DISTANCE = getattr(config, 'CHASE_DISTANCE', 5)
    LOSE_DISTANCE = getattr(config, 'LOSE_DISTANCE', 8)
    FLEE_HP = getattr(config, 'FLEE_HP', 30)

    def manhattan_dist(x1: int, y1: int, x2: int, y2: int) -> int:
        """マンハッタン距離"""
        return abs(x1 - x2) + abs(y1 - y2)

    def get_enemy(state: GameState) -> Entity | None:
        """敵エンティティを取得"""
        for e in state.entities:
            if e.id == "enemy" and e.is_active:
                return e
        return None

    def get_fsm_state(entity: Entity) -> str:
        """エンティティのFSM状態を取得（拡張属性から）"""
        # 現時点ではstate.jsonに直接書けないので、HPベースで推測
        # 本来はentity.fsm_stateを参照したい
        return getattr(entity, 'fsm_state', 'IDLE')

    def evaluate_fsm_transition(enemy: Entity, player_pos: Position) -> tuple[str, str]:
        """FSM遷移を評価し、(new_state, reason)を返す"""
        dist = manhattan_dist(enemy.pos.x, enemy.pos.y, player_pos.x, player_pos.y)
        current_state = get_fsm_state(enemy)

        # FLEE条件: HPが低い
        if enemy.hp <= FLEE_HP:
            if current_state != "FLEE":
                return ("FLEE", f"hp={enemy.hp} <= {FLEE_HP}")
            return ("FLEE", "")

        # CHASE条件: プレイヤーが近い
        if current_state == "IDLE" and dist <= CHASE_DISTANCE:
            return ("CHASE", f"player_dist={dist} <= {CHASE_DISTANCE}")

        # IDLE条件: プレイヤーが遠い
        if current_state == "CHASE" and dist >= LOSE_DISTANCE:
            return ("IDLE", f"player_dist={dist} >= {LOSE_DISTANCE}")

        return (current_state, "")

    def get_greedy_move(enemy: Entity, target: Position, flee: bool = False) -> tuple[int, int]:
        """貪欲法で1歩移動（CHASEは近づく、FLEEは離れる）"""
        dx, dy = 0, 0
        ex, ey = enemy.pos.x, enemy.pos.y
        tx, ty = target.x, target.y

        if flee:
            # 逃げる: 距離が増える方向
            if ex < tx:
                dx = -1
            elif ex > tx:
                dx = 1
            if ey < ty:
                dy = -1
            elif ey > ty:
                dy = 1
        else:
            # 追跡: 距離が減る方向
            if ex < tx:
                dx = 1
            elif ex > tx:
                dx = -1
            if ey < ty:
                dy = 1
            elif ey > ty:
                dy = -1

        # 斜め移動は禁止（4方向のみ）
        if dx != 0 and dy != 0:
            # X方向を優先
            dy = 0

        return (dx, dy)

    def build_enemy_commands(state: GameState) -> list[str]:
        """敵AIの命令列を生成（State直書き禁止、DSL命令のみ）"""
        enemy = get_enemy(state)
        if not enemy:
            return []

        # FSM遷移を評価
        new_state, reason = evaluate_fsm_transition(enemy, state.player.pos)
        current_state = get_fsm_state(enemy)

        commands = []
        logs = []

        # 状態遷移ログ
        if reason and new_state != current_state:
            logs.append(f"[FSM] {enemy.id}: {current_state} -> {new_state} ({reason})")

        # 状態に応じた行動
        if new_state == "IDLE":
            # 待機（移動しない）
            logs.append(f"[AI] {enemy.id}: IDLE (no action)")

        elif new_state == "CHASE":
            dx, dy = get_greedy_move(enemy, state.player.pos, flee=False)
            if dx != 0 or dy != 0:
                commands.append(f"move {enemy.id} {dx} {dy}")
                logs.append(f"[AI] {enemy.id} action: MOVE (dx={dx}, dy={dy})")
            else:
                logs.append(f"[AI] {enemy.id}: already at target")

        elif new_state == "FLEE":
            dx, dy = get_greedy_move(enemy, state.player.pos, flee=True)
            if dx != 0 or dy != 0:
                commands.append(f"move {enemy.id} {dx} {dy}")
                logs.append(f"[AI] {enemy.id} action: FLEE MOVE (dx={dx}, dy={dy})")
            else:
                logs.append(f"[AI] {enemy.id}: cannot flee further")

        # ログを出力
        for log in logs:
            output(log)

        return commands, new_state

    def execute_enemy_ai(state: GameState) -> GameState:
        """敵AIを実行してStateを更新"""
        if not ai_enabled[0]:
            output("[AI] Disabled")
            return state

        enemy = get_enemy(state)
        if not enemy:
            return state

        commands, new_fsm_state = build_enemy_commands(state)

        # 敵のFSM状態を更新（エンティティを置き換え）
        new_entities = []
        for e in state.entities:
            if e.id == "enemy":
                # FSM状態を更新した新しいエンティティ
                new_e = Entity(
                    id=e.id,
                    name=e.name,
                    pos=e.pos,
                    hp=e.hp,
                    is_active=e.is_active,
                )
                # FSM状態を拡張属性として設定（frozen dataclass対応）
                object.__setattr__(new_e, 'fsm_state', new_fsm_state)
                new_entities.append(new_e)
            else:
                new_entities.append(e)

        current_state = state.replace(entities=tuple(new_entities))

        # MOVE命令を実行
        for cmd in commands:
            try:
                # 敵用のmove命令を実行
                parts = cmd.split()
                if len(parts) == 4 and parts[0] == "move":
                    entity_id = parts[1]
                    dx, dy = int(parts[2]), int(parts[3])

                    # エンティティを移動
                    updated_entities = []
                    for e in current_state.entities:
                        if e.id == entity_id:
                            new_x = max(0, min(current_state.map_width - 1, e.pos.x + dx))
                            new_y = max(0, min(current_state.map_height - 1, e.pos.y + dy))
                            new_e = Entity(
                                id=e.id,
                                name=e.name,
                                pos=Position(x=new_x, y=new_y),
                                hp=e.hp,
                                is_active=e.is_active,
                            )
                            # FSM状態を引き継ぐ（frozen dataclass対応）
                            if hasattr(e, 'fsm_state'):
                                object.__setattr__(new_e, 'fsm_state', e.fsm_state)
                            updated_entities.append(new_e)
                        else:
                            updated_entities.append(e)
                    current_state = current_state.replace(entities=tuple(updated_entities))

            except Exception as e:
                output(f"[AI Error] {e}")

        return current_state

    def check_collision(state: GameState) -> tuple[GameState, str | None]:
        """敵との接触をチェック"""
        enemy = get_enemy(state)
        if not enemy:
            return state, None

        if state.player.pos.x == enemy.pos.x and state.player.pos.y == enemy.pos.y:
            # 接触: HP減少
            new_hp = state.player.hp - 10
            new_player = Entity(
                id=state.player.id,
                name=state.player.name,
                pos=state.player.pos,
                hp=new_hp,
                is_active=state.player.is_active,
            )
            new_state = state.replace(player=new_player)
            if new_hp <= 0:
                return new_state.replace(is_game_over=True), "Game Over! Enemy caught you."
            return new_state, f"Ouch! Enemy hit you! HP: {new_hp}"
        return state, None

    def check_goal(state: GameState) -> tuple[GameState, str | None]:
        """ゴール到達をチェック"""
        for e in state.entities:
            if e.id == "goal" and e.is_active:
                if state.player.pos.x == e.pos.x and state.player.pos.y == e.pos.y:
                    return state.replace(is_game_over=True), "You reached the goal! Congratulations!"
        return state, None

    def update(state: GameState, cmd: str) -> GameState:
        cmd = cmd.strip().lower()

        # ヘルプ
        if cmd == "help":
            output("\n=== Commands ===")
            if stage_commands:
                for cmd_text in stage_commands:
                    output(f"  {cmd_text}")
            else:
                output("  w/a/s/d     - Move player")
                output("  wait        - Skip turn (observe AI)")
                output("  toggle_ai   - Toggle enemy AI on/off")
                output("  ai          - Show AI debug info")
                output("  status      - Show status")
                output("  quit        - Exit")
            if stage_help:
                output("")
                output(stage_help)
            output("")
            return state

        if cmd == "goal":
            output(f"\n[Goal] {stage_goal}")
            output("")
            return state

        if cmd == "examples":
            output("\n=== Sample Commands ===")
            for i, ex in enumerate(stage_examples, 1):
                output(f"  {i}. {ex}")
            output("")
            return state

        if cmd == "status":
            enemy = get_enemy(state)
            enemy_info = "None"
            if enemy:
                fsm = get_fsm_state(enemy)
                dist = manhattan_dist(enemy.pos.x, enemy.pos.y, state.player.pos.x, state.player.pos.y)
                enemy_info = f"({enemy.pos.x},{enemy.pos.y}) HP={enemy.hp} State={fsm} Dist={dist}"

            output(f"\nTurn: {state.turn}")
            output(f"Player: ({state.player.pos.x}, {state.player.pos.y}) HP={state.player.hp}")
            output(f"Enemy: {enemy_info}")
            output(f"AI: {'ON' if ai_enabled[0] else 'OFF'}")
            output("")
            return state

        if cmd == "save":
            save_state(state, slot_path)
            update_meta(slot_path, state)
            output("Game saved.")
            return state

        # toggle_ai: AI ON/OFF
        if cmd == "toggle_ai":
            ai_enabled[0] = not ai_enabled[0]
            status = "ON" if ai_enabled[0] else "OFF"
            output(f"\n[AI] Toggled: {status}")
            output("")
            return state

        # ai: デバッグ表示
        if cmd == "ai":
            enemy = get_enemy(state)
            if not enemy:
                output("\n[AI Debug] No enemy found")
                output("")
                return state

            dist = manhattan_dist(enemy.pos.x, enemy.pos.y, state.player.pos.x, state.player.pos.y)
            current_state = get_fsm_state(enemy)
            new_state, reason = evaluate_fsm_transition(enemy, state.player.pos)

            output("\n=== AI Debug ===")
            output(f"  Enemy: ({enemy.pos.x}, {enemy.pos.y})")
            output(f"  HP: {enemy.hp}")
            output(f"  Distance to player: {dist}")
            output(f"  Current FSM state: {current_state}")
            output(f"  Next FSM state: {new_state}")
            if reason:
                output(f"  Transition reason: {reason}")
            output("")
            output("  FSM Thresholds:")
            output(f"    CHASE: dist <= {CHASE_DISTANCE}")
            output(f"    LOSE:  dist >= {LOSE_DISTANCE}")
            output(f"    FLEE:  hp <= {FLEE_HP}")
            output("")
            return state

        # wait: プレイヤーは動かず、AIだけ動く
        if cmd == "wait":
            output("\n[Wait] Observing enemy AI...")

            # 敵AIを実行
            new_state = execute_enemy_ai(state)

            # 接触チェック
            new_state, collision_msg = check_collision(new_state)
            if collision_msg:
                output(collision_msg)

            # ゴールチェック
            new_state, goal_msg = check_goal(new_state)
            if goal_msg:
                output(goal_msg)

            new_state = new_state.next_turn()

            if config.AUTO_SAVE:
                save_state(new_state, slot_path)
                update_meta(slot_path, new_state)

            return new_state

        # 移動コマンド (w/a/s/d)
        if cmd in moves:
            dx, dy = moves[cmd]
            new_x = state.player.pos.x + dx
            new_y = state.player.pos.y + dy

            # 範囲チェック
            if not (0 <= new_x < state.map_width and 0 <= new_y < state.map_height):
                output(f"\n[Blocked] Cannot move outside map")
                return state

            new_state = state.move_player(dx, dy)

            # ゴールチェック
            new_state, goal_msg = check_goal(new_state)
            if goal_msg:
                output(goal_msg)

            # 敵AIを実行
            new_state = execute_enemy_ai(new_state)

            # 接触チェック
            new_state, collision_msg = check_collision(new_state)
            if collision_msg:
                output(collision_msg)

            new_state = new_state.next_turn()

            if config.AUTO_SAVE:
                save_state(new_state, slot_path)
                update_meta(slot_path, new_state)

            return new_state

        # 未知のコマンド - フレンドリーガイドを表示
        show_input_guide(cmd, stage_input_mode, stage_mode)
        return state

    return update


def create_bt_update(slot_path: Path, interpreter: Interpreter, meta: dict | None = None):
    """BT mode用のupdate関数（敵AIがBehavior TreeでMOVE命令を生成）"""
    meta = meta or {}
    stage_commands = meta.get("stage_commands", [])
    stage_help = meta.get("stage_help_text", "")
    stage_goal = meta.get("stage_goal", "")
    stage_examples = meta.get("stage_examples", [])
    stage_input_mode = meta.get("stage_input_mode", "GAME")
    stage_mode = meta.get("stage_mode", "BT")

    # AI有効フラグ
    ai_enabled = [True]

    # 方向マッピング
    moves = {
        "w": (0, -1), "up": (0, -1),
        "s": (0, 1), "down": (0, 1),
        "a": (-1, 0), "left": (-1, 0),
        "d": (1, 0), "right": (1, 0),
    }

    # BT閾値（configから取得またはデフォルト）
    CHASE_DISTANCE = getattr(config, 'CHASE_DISTANCE', 5)
    FLEE_HP = getattr(config, 'FLEE_HP', 30)

    # =====================
    # Behavior Tree Nodes
    # =====================
    class BTResult:
        SUCCESS = "SUCCESS"
        FAILURE = "FAILURE"
        RUNNING = "RUNNING"

    class BTNode:
        """BTノード基底クラス"""
        def __init__(self, name: str):
            self.name = name

        def tick(self, state: GameState, enemy, logs: list) -> tuple[str, list[str]]:
            """評価して(結果, 命令列)を返す"""
            raise NotImplementedError

    class Condition(BTNode):
        """条件ノード"""
        def __init__(self, name: str, check_fn):
            super().__init__(name)
            self.check_fn = check_fn

        def tick(self, state: GameState, enemy, logs: list) -> tuple[str, list[str]]:
            result = self.check_fn(state, enemy)
            status = BTResult.SUCCESS if result else BTResult.FAILURE
            logs.append(f"  [Condition] {self.name}: {status}")
            return (status, [])

    class Action(BTNode):
        """行動ノード"""
        def __init__(self, name: str, action_fn):
            super().__init__(name)
            self.action_fn = action_fn

        def tick(self, state: GameState, enemy, logs: list) -> tuple[str, list[str]]:
            commands = self.action_fn(state, enemy)
            logs.append(f"  [Action] {self.name}: SUCCESS -> {commands}")
            return (BTResult.SUCCESS, commands)

    class Sequence(BTNode):
        """シーケンスノード（全て成功で成功）"""
        def __init__(self, name: str, children: list):
            super().__init__(name)
            self.children = children

        def tick(self, state: GameState, enemy, logs: list) -> tuple[str, list[str]]:
            logs.append(f"  [Sequence] {self.name}")
            all_commands = []
            for child in self.children:
                result, commands = child.tick(state, enemy, logs)
                if result == BTResult.FAILURE:
                    return (BTResult.FAILURE, [])
                all_commands.extend(commands)
            return (BTResult.SUCCESS, all_commands)

    class Selector(BTNode):
        """セレクタノード（一つ成功で成功）"""
        def __init__(self, name: str, children: list):
            super().__init__(name)
            self.children = children

        def tick(self, state: GameState, enemy, logs: list) -> tuple[str, list[str]]:
            logs.append(f"  [Selector] {self.name}")
            for child in self.children:
                result, commands = child.tick(state, enemy, logs)
                if result == BTResult.SUCCESS:
                    return (BTResult.SUCCESS, commands)
            return (BTResult.FAILURE, [])

    # =====================
    # Helper Functions
    # =====================
    def manhattan_dist(x1: int, y1: int, x2: int, y2: int) -> int:
        return abs(x1 - x2) + abs(y1 - y2)

    def get_enemy(state: GameState):
        for e in state.entities:
            if e.id == "enemy" and e.is_active:
                return e
        return None

    def get_greedy_move(enemy, target: Position, flee: bool = False) -> tuple[int, int]:
        dx, dy = 0, 0
        ex, ey = enemy.pos.x, enemy.pos.y
        tx, ty = target.x, target.y

        if flee:
            if ex < tx:
                dx = -1
            elif ex > tx:
                dx = 1
            if ey < ty:
                dy = -1
            elif ey > ty:
                dy = 1
        else:
            if ex < tx:
                dx = 1
            elif ex > tx:
                dx = -1
            if ey < ty:
                dy = 1
            elif ey > ty:
                dy = -1

        if dx != 0 and dy != 0:
            dy = 0  # X優先

        return (dx, dy)

    # =====================
    # Condition Functions
    # =====================
    def is_player_close(state: GameState, enemy) -> bool:
        dist = manhattan_dist(enemy.pos.x, enemy.pos.y, state.player.pos.x, state.player.pos.y)
        return dist <= CHASE_DISTANCE

    def is_low_hp(state: GameState, enemy) -> bool:
        return enemy.hp <= FLEE_HP

    # =====================
    # Action Functions
    # =====================
    def action_chase(state: GameState, enemy) -> list[str]:
        dx, dy = get_greedy_move(enemy, state.player.pos, flee=False)
        if dx != 0 or dy != 0:
            return [f"move {enemy.id} {dx} {dy}"]
        return []

    def action_flee(state: GameState, enemy) -> list[str]:
        dx, dy = get_greedy_move(enemy, state.player.pos, flee=True)
        if dx != 0 or dy != 0:
            return [f"move {enemy.id} {dx} {dy}"]
        return []

    def action_idle(state: GameState, enemy) -> list[str]:
        return []  # 何もしない

    # =====================
    # Build Behavior Tree
    # =====================
    # Tree Structure:
    # Root (Selector)
    #   ├─ FleeSequence (Sequence)
    #   │    ├─ IsLowHP (Condition)
    #   │    └─ Flee (Action)
    #   ├─ ChaseSequence (Sequence)
    #   │    ├─ IsPlayerClose (Condition)
    #   │    └─ Chase (Action)
    #   └─ Idle (Action)

    flee_sequence = Sequence("FleeSequence", [
        Condition("IsLowHP", is_low_hp),
        Action("Flee", action_flee),
    ])

    chase_sequence = Sequence("ChaseSequence", [
        Condition("IsPlayerClose", is_player_close),
        Action("Chase", action_chase),
    ])

    idle_action = Action("Idle", action_idle)

    root = Selector("Root", [
        flee_sequence,
        chase_sequence,
        idle_action,
    ])

    # =====================
    # Tree Visualization
    # =====================
    def get_tree_string() -> str:
        return """
[BT] Enemy Behavior Tree:
Root (Selector)
  ├─ FleeSequence (Sequence)
  │    ├─ IsLowHP (Condition): hp <= {flee_hp}
  │    └─ Flee (Action)
  ├─ ChaseSequence (Sequence)
  │    ├─ IsPlayerClose (Condition): dist <= {chase_dist}
  │    └─ Chase (Action)
  └─ Idle (Action)
""".format(flee_hp=FLEE_HP, chase_dist=CHASE_DISTANCE)

    # =====================
    # Execute Enemy AI
    # =====================
    def build_enemy_commands(state: GameState) -> tuple[list[str], list[str], str]:
        """BTを評価して(命令列, ログ, 選ばれたブランチ名)を返す"""
        enemy = get_enemy(state)
        if not enemy:
            return ([], [], "")

        logs = ["[BT] Tick:"]
        result, commands = root.tick(state, enemy, logs)

        # 選ばれたブランチを特定
        branch = "Idle"
        if is_low_hp(state, enemy):
            branch = "Flee"
        elif is_player_close(state, enemy):
            branch = "Chase"

        return (commands, logs, branch)

    def execute_enemy_ai(state: GameState) -> GameState:
        if not ai_enabled[0]:
            output("[AI] Disabled")
            return state

        enemy = get_enemy(state)
        if not enemy:
            return state

        commands, logs, branch = build_enemy_commands(state)

        # ログ出力
        for log in logs:
            output(log)
        output(f"[BT] Selected branch: {branch}")

        # MOVE命令を実行
        current_state = state
        for cmd in commands:
            try:
                parts = cmd.split()
                if len(parts) == 4 and parts[0] == "move":
                    entity_id = parts[1]
                    dx, dy = int(parts[2]), int(parts[3])

                    updated_entities = []
                    for e in current_state.entities:
                        if e.id == entity_id:
                            new_x = max(0, min(current_state.map_width - 1, e.pos.x + dx))
                            new_y = max(0, min(current_state.map_height - 1, e.pos.y + dy))
                            new_e = Entity(
                                id=e.id,
                                name=e.name,
                                pos=Position(x=new_x, y=new_y),
                                hp=e.hp,
                                is_active=e.is_active,
                            )
                            updated_entities.append(new_e)
                        else:
                            updated_entities.append(e)
                    current_state = current_state.replace(entities=tuple(updated_entities))

                    output(f"[AI] {entity_id} action: MOVE (dx={dx}, dy={dy})")

            except Exception as e:
                output(f"[AI Error] {e}")

        return current_state

    def check_collision(state: GameState) -> tuple[GameState, str | None]:
        enemy = get_enemy(state)
        if not enemy:
            return state, None

        if state.player.pos.x == enemy.pos.x and state.player.pos.y == enemy.pos.y:
            new_hp = state.player.hp - 10
            new_player = Entity(
                id=state.player.id,
                name=state.player.name,
                pos=state.player.pos,
                hp=new_hp,
                is_active=state.player.is_active,
            )
            new_state = state.replace(player=new_player)
            if new_hp <= 0:
                return new_state.replace(is_game_over=True), "Game Over! Enemy caught you."
            return new_state, f"Ouch! Enemy hit you! HP: {new_hp}"
        return state, None

    def check_goal(state: GameState) -> tuple[GameState, str | None]:
        for e in state.entities:
            if e.id == "goal" and e.is_active:
                if state.player.pos.x == e.pos.x and state.player.pos.y == e.pos.y:
                    return state.replace(is_game_over=True), "You reached the goal! Congratulations!"
        return state, None

    def update(state: GameState, cmd: str) -> GameState:
        cmd = cmd.strip().lower()

        if cmd == "help":
            output("\n=== Commands ===")
            if stage_commands:
                for cmd_text in stage_commands:
                    output(f"  {cmd_text}")
            else:
                output("  w/a/s/d     - Move player")
                output("  wait        - Skip turn (observe AI)")
                output("  toggle_ai   - Toggle enemy AI on/off")
                output("  bt          - Show BT structure")
                output("  status      - Show status")
                output("  quit        - Exit")
            if stage_help:
                output("")
                output(stage_help)
            output("")
            return state

        if cmd == "goal":
            output(f"\n[Goal] {stage_goal}")
            output("")
            return state

        if cmd == "examples":
            output("\n=== Sample Commands ===")
            for i, ex in enumerate(stage_examples, 1):
                output(f"  {i}. {ex}")
            output("")
            return state

        if cmd == "status":
            enemy = get_enemy(state)
            enemy_info = "None"
            if enemy:
                dist = manhattan_dist(enemy.pos.x, enemy.pos.y, state.player.pos.x, state.player.pos.y)
                enemy_info = f"({enemy.pos.x},{enemy.pos.y}) HP={enemy.hp} Dist={dist}"

            output(f"\nTurn: {state.turn}")
            output(f"Player: ({state.player.pos.x}, {state.player.pos.y}) HP={state.player.hp}")
            output(f"Enemy: {enemy_info}")
            output(f"AI: {'ON' if ai_enabled[0] else 'OFF'}")
            output("")
            return state

        if cmd == "save":
            save_state(state, slot_path)
            update_meta(slot_path, state)
            output("Game saved.")
            return state

        if cmd == "toggle_ai":
            ai_enabled[0] = not ai_enabled[0]
            status = "ON" if ai_enabled[0] else "OFF"
            output(f"\n[AI] Toggled: {status}")
            output("")
            return state

        if cmd == "bt":
            output(get_tree_string())
            return state

        if cmd == "wait":
            output("\n[Wait] Observing enemy AI...")
            new_state = execute_enemy_ai(state)
            new_state, collision_msg = check_collision(new_state)
            if collision_msg:
                output(collision_msg)
            new_state, goal_msg = check_goal(new_state)
            if goal_msg:
                output(goal_msg)
            new_state = new_state.next_turn()
            if config.AUTO_SAVE:
                save_state(new_state, slot_path)
                update_meta(slot_path, new_state)
            return new_state

        if cmd in moves:
            dx, dy = moves[cmd]
            new_x = state.player.pos.x + dx
            new_y = state.player.pos.y + dy

            if not (0 <= new_x < state.map_width and 0 <= new_y < state.map_height):
                output(f"\n[Blocked] Cannot move outside map")
                return state

            new_state = state.move_player(dx, dy)
            new_state, goal_msg = check_goal(new_state)
            if goal_msg:
                output(goal_msg)
            new_state = execute_enemy_ai(new_state)
            new_state, collision_msg = check_collision(new_state)
            if collision_msg:
                output(collision_msg)
            new_state = new_state.next_turn()
            if config.AUTO_SAVE:
                save_state(new_state, slot_path)
                update_meta(slot_path, new_state)
            return new_state

        show_input_guide(cmd, stage_input_mode, stage_mode)
        return state

    return update


def create_goap_update(slot_path: Path, interpreter: Interpreter, meta: dict | None = None):
    """GOAP mode用のupdate関数（敵AIがGOAPでMOVE命令を生成）"""
    meta = meta or {}
    stage_commands = meta.get("stage_commands", [])
    stage_help = meta.get("stage_help_text", "")
    stage_goal = meta.get("stage_goal", "")
    stage_examples = meta.get("stage_examples", [])
    stage_input_mode = meta.get("stage_input_mode", "GAME")
    stage_mode = meta.get("stage_mode", "GOAP")

    ai_enabled = [True]
    moves = {
        "w": (0, -1), "s": (0, 1), "a": (-1, 0), "d": (1, 0),
    }

    CHASE_DISTANCE = getattr(config, 'CHASE_DISTANCE', 8)
    FLEE_HP = getattr(config, 'FLEE_HP', 30)

    # =====================
    # GOAP World State & Actions
    # =====================
    def get_world_state(state: GameState, enemy) -> dict:
        """現在のワールド状態を取得"""
        dist = abs(enemy.pos.x - state.player.pos.x) + abs(enemy.pos.y - state.player.pos.y)
        return {
            "enemy_hp": enemy.hp,
            "player_near": dist <= CHASE_DISTANCE,
            "player_adjacent": dist <= 1,
            "enemy_low_hp": enemy.hp <= FLEE_HP,
        }

    class GOAPAction:
        def __init__(self, name: str, preconditions: dict, effects: dict, cost: int, command_fn):
            self.name = name
            self.preconditions = preconditions
            self.effects = effects
            self.cost = cost
            self.command_fn = command_fn

        def is_applicable(self, world: dict) -> bool:
            for key, value in self.preconditions.items():
                if world.get(key) != value:
                    return False
            return True

        def apply(self, world: dict) -> dict:
            new_world = world.copy()
            new_world.update(self.effects)
            return new_world

    def manhattan_dist(x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    def get_enemy(state: GameState):
        for e in state.entities:
            if e.id == "enemy" and e.is_active:
                return e
        return None

    def get_greedy_move(enemy, target, flee=False):
        dx, dy = 0, 0
        if flee:
            dx = -1 if enemy.pos.x < target.x else (1 if enemy.pos.x > target.x else 0)
            dy = -1 if enemy.pos.y < target.y else (1 if enemy.pos.y > target.y else 0)
        else:
            dx = 1 if enemy.pos.x < target.x else (-1 if enemy.pos.x > target.x else 0)
            dy = 1 if enemy.pos.y < target.y else (-1 if enemy.pos.y > target.y else 0)
        if dx != 0 and dy != 0:
            dy = 0
        return dx, dy

    def cmd_approach(state, enemy):
        dx, dy = get_greedy_move(enemy, state.player.pos, flee=False)
        return [f"move {enemy.id} {dx} {dy}"] if dx or dy else []

    def cmd_flee(state, enemy):
        dx, dy = get_greedy_move(enemy, state.player.pos, flee=True)
        return [f"move {enemy.id} {dx} {dy}"] if dx or dy else []

    def cmd_attack(state, enemy):
        return []  # 攻撃は省略（教材用）

    def cmd_idle(state, enemy):
        return []

    # GOAPアクション定義
    actions = [
        GOAPAction("Flee", {"enemy_low_hp": True}, {"safe": True}, 1, cmd_flee),
        GOAPAction("Attack", {"player_adjacent": True, "enemy_low_hp": False}, {"player_damaged": True}, 1, cmd_attack),
        GOAPAction("Approach", {"player_near": True, "enemy_low_hp": False}, {"player_adjacent": True}, 2, cmd_approach),
        GOAPAction("Idle", {}, {}, 3, cmd_idle),
    ]

    def plan_goap(world: dict, goal: dict, max_depth: int = 3) -> list:
        """簡易GOAPプランナー"""
        # ゴールが達成済みかチェック
        def goal_reached(w):
            for k, v in goal.items():
                if w.get(k) != v:
                    return False
            return True

        if goal_reached(world):
            return []

        # 適用可能なアクションを探す
        for action in actions:
            if action.is_applicable(world):
                return [action]

        return [actions[-1]]  # Idle fallback

    current_plan = []
    current_goal = {"player_damaged": True}

    def build_enemy_commands(state: GameState) -> tuple[list[str], list[str], str]:
        nonlocal current_plan, current_goal
        enemy = get_enemy(state)
        if not enemy:
            return [], [], ""

        world = get_world_state(state, enemy)
        logs = ["[GOAP] Planning:"]
        logs.append(f"  World: {world}")

        # ゴール選択
        if world["enemy_low_hp"]:
            current_goal = {"safe": True}
        else:
            current_goal = {"player_damaged": True}

        logs.append(f"  Goal: {current_goal}")

        # プラン生成
        current_plan = plan_goap(world, current_goal)
        plan_names = [a.name for a in current_plan]
        logs.append(f"  Plan: {plan_names}")

        # 最初のアクションを実行
        commands = []
        branch = "Idle"
        if current_plan:
            action = current_plan[0]
            branch = action.name
            commands = action.command_fn(state, enemy)
            logs.append(f"  Executing: {action.name}")

        return commands, logs, branch

    def execute_enemy_ai(state: GameState) -> GameState:
        if not ai_enabled[0]:
            output("[AI] Disabled")
            return state
        enemy = get_enemy(state)
        if not enemy:
            return state

        commands, logs, branch = build_enemy_commands(state)
        for log in logs:
            output(log)
        output(f"[GOAP] Selected action: {branch}")

        current_state = state
        for cmd in commands:
            parts = cmd.split()
            if len(parts) == 4 and parts[0] == "move":
                entity_id, dx, dy = parts[1], int(parts[2]), int(parts[3])
                updated = []
                for e in current_state.entities:
                    if e.id == entity_id:
                        nx = max(0, min(current_state.map_width - 1, e.pos.x + dx))
                        ny = max(0, min(current_state.map_height - 1, e.pos.y + dy))
                        updated.append(Entity(e.id, e.name, Position(nx, ny), e.hp, e.is_active))
                    else:
                        updated.append(e)
                current_state = current_state.replace(entities=tuple(updated))
                output(f"[AI] {entity_id} action: MOVE (dx={dx}, dy={dy})")
        return current_state

    def check_collision(state):
        enemy = get_enemy(state)
        if enemy and state.player.pos.x == enemy.pos.x and state.player.pos.y == enemy.pos.y:
            new_hp = state.player.hp - 10
            new_player = Entity(state.player.id, state.player.name, state.player.pos, new_hp, state.player.is_active)
            new_state = state.replace(player=new_player)
            if new_hp <= 0:
                return new_state.replace(is_game_over=True), "Game Over!"
            return new_state, f"Hit! HP: {new_hp}"
        return state, None

    def check_goal(state):
        for e in state.entities:
            if e.id == "goal" and e.is_active and state.player.pos == e.pos:
                return state.replace(is_game_over=True), "Goal reached!"
        return state, None

    def update(state: GameState, cmd: str) -> GameState:
        cmd = cmd.strip().lower()
        if cmd == "help":
            output("\n=== Commands ===")
            for c in (stage_commands or ["w/a/s/d", "wait", "toggle_ai", "goap", "status", "quit"]):
                output(f"  {c}")
            output("")
            return state
        if cmd == "goap":
            enemy = get_enemy(state)
            if enemy:
                world = get_world_state(state, enemy)
                output("\n[GOAP Debug]")
                output(f"  World State: {world}")
                output(f"  Actions: {[a.name for a in actions]}")
            return state
        if cmd == "toggle_ai":
            ai_enabled[0] = not ai_enabled[0]
            output(f"[AI] {'ON' if ai_enabled[0] else 'OFF'}")
            return state
        if cmd == "status":
            enemy = get_enemy(state)
            output(f"\nTurn: {state.turn}, Player: ({state.player.pos.x},{state.player.pos.y}) HP={state.player.hp}")
            if enemy:
                output(f"Enemy: ({enemy.pos.x},{enemy.pos.y}) HP={enemy.hp}")
            return state
        if cmd == "wait":
            new_state = execute_enemy_ai(state)
            new_state, msg = check_collision(new_state)
            if msg: output(msg)
            new_state, msg = check_goal(new_state)
            if msg: output(msg)
            return new_state.next_turn()
        if cmd in moves:
            dx, dy = moves[cmd]
            new_state = state.move_player(dx, dy)
            new_state, msg = check_goal(new_state)
            if msg: output(msg)
            new_state = execute_enemy_ai(new_state)
            new_state, msg = check_collision(new_state)
            if msg: output(msg)
            return new_state.next_turn()
        show_input_guide(cmd, stage_input_mode, stage_mode)
        return state

    return update


def create_director_update(slot_path: Path, interpreter: Interpreter, meta: dict | None = None):
    """Director mode用のupdate関数（System AIがゲーム全体を制御）"""
    meta = meta or {}
    stage_commands = meta.get("stage_commands", [])
    stage_help = meta.get("stage_help_text", "")
    stage_input_mode = meta.get("stage_input_mode", "GAME")
    stage_mode = meta.get("stage_mode", "DIRECTOR")
    stage_goal = meta.get("stage_goal", "")

    ai_enabled = [True]
    director_enabled = [True]
    moves = {"w": (0, -1), "s": (0, 1), "a": (-1, 0), "d": (1, 0)}

    LOW_HP = getattr(config, 'LOW_HP_THRESHOLD', 30)
    HIGH_HP = getattr(config, 'HIGH_HP_THRESHOLD', 70)
    CHASE_LOW = getattr(config, 'CHASE_DISTANCE_LOW', 8)
    CHASE_MID = getattr(config, 'CHASE_DISTANCE_MID', 5)
    CHASE_HIGH = getattr(config, 'CHASE_DISTANCE_HIGH', 3)

    tension = ["MID"]
    chase_distance = [CHASE_MID]

    def evaluate_tension(state):
        if state.player.hp <= LOW_HP:
            return "HIGH"
        elif state.player.hp >= HIGH_HP:
            return "LOW"
        return "MID"

    def apply_director_rules(new_tension):
        old = tension[0]
        tension[0] = new_tension
        if new_tension == "HIGH":
            chase_distance[0] = CHASE_HIGH
        elif new_tension == "LOW":
            chase_distance[0] = CHASE_LOW
        else:
            chase_distance[0] = CHASE_MID
        return old != new_tension

    def get_enemy(state):
        for e in state.entities:
            if e.id == "enemy" and e.is_active:
                return e
        return None

    def manhattan_dist(x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    def execute_enemy_ai(state):
        if not ai_enabled[0]:
            return state
        enemy = get_enemy(state)
        if not enemy:
            return state
        dist = manhattan_dist(enemy.pos.x, enemy.pos.y, state.player.pos.x, state.player.pos.y)
        if dist <= chase_distance[0]:
            dx = 1 if enemy.pos.x < state.player.pos.x else (-1 if enemy.pos.x > state.player.pos.x else 0)
            dy = 1 if enemy.pos.y < state.player.pos.y else (-1 if enemy.pos.y > state.player.pos.y else 0)
            if dx and dy:
                dy = 0
            if dx or dy:
                nx = max(0, min(state.map_width - 1, enemy.pos.x + dx))
                ny = max(0, min(state.map_height - 1, enemy.pos.y + dy))
                updated = []
                for e in state.entities:
                    if e.id == "enemy":
                        updated.append(Entity(e.id, e.name, Position(nx, ny), e.hp, e.is_active))
                    else:
                        updated.append(e)
                output(f"[AI] enemy MOVE (dx={dx}, dy={dy})")
                return state.replace(entities=tuple(updated))
        output(f"[AI] enemy IDLE (dist={dist} > chase={chase_distance[0]})")
        return state

    def check_collision(state):
        enemy = get_enemy(state)
        if enemy and state.player.pos.x == enemy.pos.x and state.player.pos.y == enemy.pos.y:
            new_hp = state.player.hp - 10
            new_player = Entity(state.player.id, state.player.name, state.player.pos, new_hp, state.player.is_active)
            new_state = state.replace(player=new_player)
            if new_hp <= 0:
                return new_state.replace(is_game_over=True), "Game Over!"
            return new_state, f"Hit! HP: {new_hp}"
        return state, None

    def update(state, cmd):
        cmd = cmd.strip().lower()
        if cmd == "help":
            output("\n=== Commands ===")
            for c in (stage_commands or ["w/a/s/d", "wait", "director", "toggle_director", "status", "quit"]):
                output(f"  {c}")
            return state
        if cmd == "director":
            output(f"\n[Director]")
            output(f"  Tension: {tension[0]}")
            output(f"  Chase Distance: {chase_distance[0]}")
            output(f"  Rules: HP<={LOW_HP}->HIGH, HP>={HIGH_HP}->LOW")
            return state
        if cmd == "toggle_director":
            director_enabled[0] = not director_enabled[0]
            output(f"[Director] {'ON' if director_enabled[0] else 'OFF'}")
            return state
        if cmd == "toggle_ai":
            ai_enabled[0] = not ai_enabled[0]
            output(f"[AI] {'ON' if ai_enabled[0] else 'OFF'}")
            return state
        if cmd == "status":
            enemy = get_enemy(state)
            output(f"\nTurn: {state.turn}, Player HP: {state.player.hp}")
            output(f"Tension: {tension[0]}, Chase: {chase_distance[0]}")
            if enemy:
                output(f"Enemy: ({enemy.pos.x},{enemy.pos.y})")
            return state
        if cmd == "wait":
            if director_enabled[0]:
                new_t = evaluate_tension(state)
                if apply_director_rules(new_t):
                    output(f"[Director] Tension: {tension[0]} -> chase={chase_distance[0]}")
            new_state = execute_enemy_ai(state)
            new_state, msg = check_collision(new_state)
            if msg: output(msg)
            return new_state.next_turn()
        if cmd in moves:
            dx, dy = moves[cmd]
            new_state = state.move_player(dx, dy)
            if director_enabled[0]:
                new_t = evaluate_tension(new_state)
                if apply_director_rules(new_t):
                    output(f"[Director] Tension: {tension[0]} -> chase={chase_distance[0]}")
            new_state = execute_enemy_ai(new_state)
            new_state, msg = check_collision(new_state)
            if msg: output(msg)
            return new_state.next_turn()
        show_input_guide(cmd, stage_input_mode, stage_mode)
        return state

    return update


def create_integration_update(slot_path: Path, interpreter: Interpreter, meta: dict | None = None):
    """Integration mode用のupdate関数（人間 x AI x ルール）"""
    meta = meta or {}
    stage_commands = meta.get("stage_commands", [])
    stage_goal = meta.get("stage_goal", "")
    stage_input_mode = meta.get("stage_input_mode", "MIXED")
    stage_mode = meta.get("stage_mode", "INTEGRATION")

    ai_enabled = [True]
    last_dsl = [""]
    last_result = [""]
    ALLOWED_VERBS = getattr(config, 'ALLOWED_VERBS', ["move", "spawn", "destroy", "set", "wait"])

    def get_enemy(state):
        for e in state.entities:
            if e.id == "enemy" and e.is_active:
                return e
        return None

    def validate_dsl(dsl: str) -> tuple[bool, str]:
        parts = dsl.strip().split()
        if not parts:
            return False, "Empty command"
        verb = parts[0].lower()
        if verb not in ALLOWED_VERBS:
            return False, f"Unknown verb: {verb}. Allowed: {ALLOWED_VERBS}"
        return True, "Valid"

    def execute_dsl(state, dsl):
        parts = dsl.strip().split()
        if not parts:
            return state, "Empty"
        verb = parts[0].lower()
        if verb == "move" and len(parts) >= 4:
            target, dx, dy = parts[1], int(parts[2]), int(parts[3])
            if target == "player":
                return state.move_player(dx, dy), f"Player moved ({dx},{dy})"
            else:
                updated = []
                for e in state.entities:
                    if e.id == target:
                        nx = max(0, min(state.map_width - 1, e.pos.x + dx))
                        ny = max(0, min(state.map_height - 1, e.pos.y + dy))
                        updated.append(Entity(e.id, e.name, Position(nx, ny), e.hp, e.is_active))
                    else:
                        updated.append(e)
                return state.replace(entities=tuple(updated)), f"{target} moved"
        return state, "Unknown DSL"

    def execute_ai(state):
        if not ai_enabled[0]:
            return state, []
        enemy = get_enemy(state)
        if not enemy:
            return state, []
        dist = abs(enemy.pos.x - state.player.pos.x) + abs(enemy.pos.y - state.player.pos.y)
        if dist <= 5:
            dx = 1 if enemy.pos.x < state.player.pos.x else (-1 if enemy.pos.x > state.player.pos.x else 0)
            dy = 1 if enemy.pos.y < state.player.pos.y else (-1 if enemy.pos.y > state.player.pos.y else 0)
            if dx and dy:
                dy = 0
            if dx or dy:
                dsl = f"move enemy {dx} {dy}"
                return execute_dsl(state, dsl)[0], [dsl]
        return state, []

    def update(state, cmd):
        nonlocal last_dsl, last_result
        cmd = cmd.strip()
        cmd_lower = cmd.lower()

        if cmd_lower == "help":
            output("\n=== Commands ===")
            output("  dsl <cmd>  - Execute DSL directly")
            output("  ai on/off  - Toggle AI")
            output("  validate   - Show last DSL validation")
            output("  status     - Show status")
            output("  quit       - Exit")
            output(f"\nAllowed DSL verbs: {ALLOWED_VERBS}")
            return state

        if cmd_lower == "validate":
            output(f"\n[Validate]")
            output(f"  Last DSL: {last_dsl[0]}")
            output(f"  Result: {last_result[0]}")
            return state

        if cmd_lower == "ai on":
            ai_enabled[0] = True
            output("[AI] ON")
            return state
        if cmd_lower == "ai off":
            ai_enabled[0] = False
            output("[AI] OFF")
            return state

        if cmd_lower == "status":
            enemy = get_enemy(state)
            output(f"\nTurn: {state.turn}")
            output(f"Player: ({state.player.pos.x},{state.player.pos.y}) HP={state.player.hp}")
            if enemy:
                output(f"Enemy: ({enemy.pos.x},{enemy.pos.y})")
            output(f"AI: {'ON' if ai_enabled[0] else 'OFF'}")
            return state

        if cmd_lower.startswith("dsl "):
            dsl = cmd[4:].strip()
            last_dsl[0] = dsl
            valid, msg = validate_dsl(dsl)
            last_result[0] = msg
            if not valid:
                output(f"[Human] DSL rejected: {msg}")
                return state
            output(f"[Human] DSL accepted: {dsl}")
            new_state, result = execute_dsl(state, dsl)
            output(f"  Result: {result}")
            new_state, ai_dsls = execute_ai(new_state)
            for ai_dsl in ai_dsls:
                output(f"[AI] Proposed: {ai_dsl}")
            return new_state.next_turn()

        # w/a/s/d shortcut
        moves = {"w": (0, -1), "s": (0, 1), "a": (-1, 0), "d": (1, 0)}
        if cmd_lower in moves:
            dx, dy = moves[cmd_lower]
            dsl = f"move player {dx} {dy}"
            last_dsl[0] = dsl
            last_result[0] = "Valid (shortcut)"
            output(f"[Human] Input: {cmd} -> DSL: {dsl}")
            new_state, _ = execute_dsl(state, dsl)
            new_state, ai_dsls = execute_ai(new_state)
            for ai_dsl in ai_dsls:
                output(f"[AI] Proposed: {ai_dsl}")
            return new_state.next_turn()

        show_input_guide(cmd, stage_input_mode, stage_mode)
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

    # Pathfinding mode (A*経路探索 + MOVE命令実行)
    if mode == "PATHFINDING":
        return create_pathfinding_update(slot_path, interpreter, meta)

    # FSM mode (敵AIがFSMでMOVE命令を生成)
    if mode == "FSM":
        return create_fsm_update(slot_path, interpreter, meta)

    # BT mode (敵AIがBTでMOVE命令を生成)
    if mode == "BT":
        return create_bt_update(slot_path, interpreter, meta)

    # GOAP mode (敵AIがGOAPでMOVE命令を生成)
    if mode == "GOAP":
        return create_goap_update(slot_path, interpreter, meta)

    # Director mode (System AIがゲーム全体を制御)
    if mode == "DIRECTOR":
        return create_director_update(slot_path, interpreter, meta)

    # Integration mode (人間 x AI x ルール)
    if mode == "INTEGRATION":
        return create_integration_update(slot_path, interpreter, meta)

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
    stage_input_mode = meta.get("stage_input_mode", "GAME")
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
    hint_text = get_hint_text(stage_input_mode, stage_mode)

    def game_get_input() -> str:
        try:
            print(hint_text)
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
