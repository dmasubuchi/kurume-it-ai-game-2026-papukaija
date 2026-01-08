"""
DSLインタプリタ（実行器）

ASTを実際に実行し、GameStateを変更します。
これはインタプリタの3番目のステップです。

例:
    AST: MoveCommand(target="player", x=5, y=3)
    実行: state.move_player() を呼び出し、新しいstateを返す
"""

from dataclasses import dataclass, replace
from typing import Any, Callable

from src.core.state import GameState, Entity, Position
from src.dsl.parser import (
    Program,
    ASTNode,
    MoveCommand,
    SpawnCommand,
    DestroyCommand,
    SetCommand,
    IfStatement,
    Expression,
    NumberLiteral,
    StringLiteral,
    BoolLiteral,
    Identifier,
    PropertyAccess,
    BinaryOp,
    UnaryOp,
)


# ============================================
# ランタイムエラー
# ============================================


@dataclass
class RuntimeError:
    """実行時エラー"""

    message: str
    node: ASTNode | None = None


@dataclass
class ExecutionResult:
    """実行結果"""

    state: GameState
    errors: list[RuntimeError]
    logs: list[str]


# ============================================
# インタプリタ
# ============================================


class Interpreter:
    """
    DSLインタプリタ

    ASTを実行してGameStateを変更します。
    """

    def __init__(
        self,
        on_log: Callable[[str], None] | None = None,
    ) -> None:
        """
        Args:
            on_log: ログ出力コールバック
        """
        self.on_log = on_log or (lambda x: None)
        self.errors: list[RuntimeError] = []
        self.logs: list[str] = []

    def _log(self, message: str) -> None:
        """ログを記録"""
        self.logs.append(message)
        self.on_log(message)

    def _error(self, message: str, node: ASTNode | None = None) -> None:
        """エラーを記録"""
        self.errors.append(RuntimeError(message=message, node=node))
        self._log(f"Error: {message}")

    # ============================================
    # 式の評価
    # ============================================

    def evaluate(self, expr: Expression, state: GameState) -> Any:
        """
        式を評価して値を返す

        Args:
            expr: 評価する式
            state: 現在のゲーム状態

        Returns:
            評価結果の値
        """
        if isinstance(expr, NumberLiteral):
            return expr.value

        if isinstance(expr, StringLiteral):
            return expr.value

        if isinstance(expr, BoolLiteral):
            return expr.value

        if isinstance(expr, Identifier):
            return self._resolve_identifier(expr.name, state)

        if isinstance(expr, PropertyAccess):
            return self._resolve_property(expr.object, expr.property, state)

        if isinstance(expr, BinaryOp):
            left = self.evaluate(expr.left, state)
            right = self.evaluate(expr.right, state)
            return self._apply_binary_op(expr.op, left, right)

        if isinstance(expr, UnaryOp):
            operand = self.evaluate(expr.operand, state)
            return self._apply_unary_op(expr.op, operand)

        self._error(f"Unknown expression type: {type(expr).__name__}", expr)
        return None

    def _resolve_identifier(self, name: str, state: GameState) -> Entity | None:
        """識別子を解決してエンティティを返す"""
        if name == "player":
            return state.player

        # entitiesから検索
        for entity in state.entities:
            if entity.name == name or entity.id == name:
                return entity

        self._error(f"Unknown identifier: {name}")
        return None

    def _resolve_property(
        self, obj_name: str, prop_name: str, state: GameState
    ) -> Any:
        """プロパティアクセスを解決"""
        entity = self._resolve_identifier(obj_name, state)
        if entity is None:
            return None

        # Position プロパティ
        if prop_name == "x":
            return entity.pos.x
        if prop_name == "y":
            return entity.pos.y

        # Entity プロパティ
        if prop_name == "hp":
            return entity.hp
        if prop_name == "name":
            return entity.name
        if prop_name == "id":
            return entity.id
        if prop_name == "is_active":
            return entity.is_active

        # 汎用プロパティ（将来の拡張用）
        if hasattr(entity, prop_name):
            return getattr(entity, prop_name)

        self._error(f"Unknown property: {obj_name}.{prop_name}")
        return None

    def _apply_binary_op(self, op: str, left: Any, right: Any) -> Any:
        """二項演算を適用"""
        # 比較演算
        if op == "<":
            return left < right
        if op == ">":
            return left > right
        if op == "<=":
            return left <= right
        if op == ">=":
            return left >= right
        if op == "==" or op == "=":
            return left == right
        if op == "!=":
            return left != right

        # 論理演算
        if op == "and":
            return left and right
        if op == "or":
            return left or right

        # 算術演算
        if op == "+":
            return left + right
        if op == "-":
            return left - right
        if op == "*":
            return left * right
        if op == "/":
            return left / right if right != 0 else 0

        self._error(f"Unknown operator: {op}")
        return None

    def _apply_unary_op(self, op: str, operand: Any) -> Any:
        """単項演算を適用"""
        if op == "not":
            return not operand
        if op == "-":
            return -operand

        self._error(f"Unknown unary operator: {op}")
        return None

    # ============================================
    # コマンドの実行
    # ============================================

    def execute_command(self, cmd: ASTNode, state: GameState) -> GameState:
        """
        コマンドを実行して新しい状態を返す

        Args:
            cmd: 実行するコマンド
            state: 現在のゲーム状態

        Returns:
            新しいゲーム状態
        """
        if isinstance(cmd, MoveCommand):
            return self._execute_move(cmd, state)

        if isinstance(cmd, SpawnCommand):
            return self._execute_spawn(cmd, state)

        if isinstance(cmd, DestroyCommand):
            return self._execute_destroy(cmd, state)

        if isinstance(cmd, SetCommand):
            return self._execute_set(cmd, state)

        if isinstance(cmd, IfStatement):
            return self._execute_if(cmd, state)

        self._error(f"Unknown command type: {type(cmd).__name__}", cmd)
        return state

    def _execute_move(self, cmd: MoveCommand, state: GameState) -> GameState:
        """move コマンドを実行"""
        self._log(f"Moving {cmd.target} to ({cmd.x}, {cmd.y})")

        if cmd.target == "player":
            # プレイヤー移動
            new_player = state.player.move_to(cmd.x, cmd.y)
            return state.replace(
                player=new_player,
                log_messages=state.log_messages + (f"Moved to ({cmd.x}, {cmd.y})",),
            )

        # 他のエンティティを移動
        new_entities = []
        moved = False
        for entity in state.entities:
            if entity.name == cmd.target or entity.id == cmd.target:
                new_entities.append(entity.move_to(cmd.x, cmd.y))
                moved = True
            else:
                new_entities.append(entity)

        if not moved:
            self._error(f"Entity not found: {cmd.target}", cmd)
            return state

        return state.replace(entities=tuple(new_entities))

    def _execute_spawn(self, cmd: SpawnCommand, state: GameState) -> GameState:
        """spawn コマンドを実行"""
        # 新しいエンティティを作成
        entity_id = f"{cmd.entity_type}_{len(state.entities)}"
        name = cmd.name if cmd.name else cmd.entity_type

        new_entity = Entity(
            id=entity_id,
            name=name,
            pos=Position(x=cmd.x, y=cmd.y),
        )

        self._log(f"Spawned {name} at ({cmd.x}, {cmd.y})")

        return state.replace(
            entities=state.entities + (new_entity,),
            log_messages=state.log_messages + (f"Spawned {name}",),
        )

    def _execute_destroy(self, cmd: DestroyCommand, state: GameState) -> GameState:
        """destroy コマンドを実行"""
        self._log(f"Destroying {cmd.target}")

        new_entities = tuple(
            e
            for e in state.entities
            if e.name != cmd.target and e.id != cmd.target
        )

        destroyed_count = len(state.entities) - len(new_entities)
        if destroyed_count == 0:
            self._error(f"Entity not found: {cmd.target}", cmd)
            return state

        return state.replace(
            entities=new_entities,
            score=state.score + (destroyed_count * 10),
            log_messages=state.log_messages + (f"Destroyed {cmd.target}",),
        )

    def _execute_set(self, cmd: SetCommand, state: GameState) -> GameState:
        """set コマンドを実行"""
        self._log(f"Setting {cmd.target}.{cmd.property} = {cmd.value}")

        if cmd.target == "player":
            new_player = self._set_entity_property(state.player, cmd.property, cmd.value)
            if new_player is None:
                return state
            return state.replace(player=new_player)

        # 他のエンティティを更新
        new_entities = []
        updated = False
        for entity in state.entities:
            if entity.name == cmd.target or entity.id == cmd.target:
                new_entity = self._set_entity_property(entity, cmd.property, cmd.value)
                if new_entity is not None:
                    new_entities.append(new_entity)
                    updated = True
                else:
                    new_entities.append(entity)
            else:
                new_entities.append(entity)

        if not updated:
            self._error(f"Entity not found: {cmd.target}", cmd)
            return state

        return state.replace(entities=tuple(new_entities))

    def _set_entity_property(
        self, entity: Entity, prop: str, value: Any
    ) -> Entity | None:
        """エンティティのプロパティを設定"""
        if prop == "hp":
            return replace(entity, hp=int(value))
        if prop == "x":
            return entity.move_to(int(value), entity.pos.y)
        if prop == "y":
            return entity.move_to(entity.pos.x, int(value))
        if prop == "is_active":
            return replace(entity, is_active=bool(value))

        self._error(f"Cannot set property: {prop}")
        return None

    def _execute_if(self, cmd: IfStatement, state: GameState) -> GameState:
        """if 文を実行"""
        condition_result = self.evaluate(cmd.condition, state)
        self._log(f"Condition evaluated to: {condition_result}")

        if condition_result:
            return self.execute_command(cmd.then_action, state)
        elif cmd.else_action is not None:
            return self.execute_command(cmd.else_action, state)

        return state

    # ============================================
    # プログラム全体の実行
    # ============================================

    def execute(self, program: Program, state: GameState) -> ExecutionResult:
        """
        プログラム全体を実行

        Args:
            program: 実行するプログラム（ASTのルート）
            state: 初期ゲーム状態

        Returns:
            実行結果（新しい状態、エラー、ログ）
        """
        self.errors = []
        self.logs = []

        current_state = state

        for stmt in program.statements:
            current_state = self.execute_command(stmt, current_state)

        return ExecutionResult(
            state=current_state,
            errors=self.errors,
            logs=self.logs,
        )


# ============================================
# 簡易関数
# ============================================


def interpret(source: str, state: GameState) -> ExecutionResult:
    """
    ソースコードを解釈実行する（簡易関数）

    Args:
        source: DSLソースコード
        state: 現在のゲーム状態

    Returns:
        実行結果
    """
    from src.dsl.parser import parse

    program = parse(source)
    interpreter = Interpreter()
    return interpreter.execute(program, state)


def execute_command(source: str, state: GameState) -> GameState:
    """
    単一コマンドを実行して新しい状態を返す（簡易関数）

    Args:
        source: DSLコマンド
        state: 現在のゲーム状態

    Returns:
        新しいゲーム状態
    """
    result = interpret(source, state)
    return result.state
