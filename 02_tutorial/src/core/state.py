"""
ゲーム状態（State）管理

Stateはゲーム世界の「唯一の真実」です。
不変（immutable）なdataclassとして定義し、
状態の変更は常に新しいStateを返すことで行います。
"""

from dataclasses import dataclass, field, replace
from typing import Self


@dataclass(frozen=True)
class Position:
    """2D位置（不変）"""

    x: int = 0
    y: int = 0

    def move(self, dx: int, dy: int) -> Self:
        """移動した新しい位置を返す"""
        return Position(x=self.x + dx, y=self.y + dy)

    def distance_to(self, other: "Position") -> float:
        """他の位置までの距離"""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


@dataclass(frozen=True)
class Entity:
    """ゲーム内エンティティ（不変）"""

    id: str
    name: str
    pos: Position = field(default_factory=Position)
    hp: int = 100
    is_active: bool = True

    def move_to(self, x: int, y: int) -> Self:
        """指定位置に移動した新しいEntityを返す"""
        return replace(self, pos=Position(x=x, y=y))

    def move_by(self, dx: int, dy: int) -> Self:
        """相対移動した新しいEntityを返す"""
        return replace(self, pos=self.pos.move(dx, dy))

    def take_damage(self, damage: int) -> Self:
        """ダメージを受けた新しいEntityを返す"""
        new_hp = max(0, self.hp - damage)
        return replace(self, hp=new_hp, is_active=new_hp > 0)


@dataclass(frozen=True)
class GameState:
    """
    ゲーム状態（不変）

    全てのゲーム情報を保持する「唯一の真実」です。
    """

    # プレイヤー
    player: Entity = field(
        default_factory=lambda: Entity(id="player", name="Player", pos=Position(5, 5))
    )

    # エンティティリスト（タプルで不変性を保つ）
    entities: tuple[Entity, ...] = ()

    # ゲーム進行
    turn: int = 0
    score: int = 0
    is_game_over: bool = False

    # マップサイズ
    map_width: int = 20
    map_height: int = 10

    # ログ（最新のメッセージ）
    log_messages: tuple[str, ...] = ()

    def replace(self, **changes) -> Self:
        """変更を適用した新しいStateを返す"""
        return replace(self, **changes)

    def next_turn(self) -> Self:
        """ターンを進めた新しいStateを返す"""
        return self.replace(turn=self.turn + 1)

    def add_score(self, points: int) -> Self:
        """スコアを追加した新しいStateを返す"""
        return self.replace(score=self.score + points)

    def add_log(self, message: str) -> Self:
        """ログを追加した新しいStateを返す"""
        # 最新5件のみ保持
        new_logs = (self.log_messages + (message,))[-5:]
        return self.replace(log_messages=new_logs)

    def move_player(self, dx: int, dy: int) -> Self:
        """プレイヤーを移動した新しいStateを返す"""
        new_pos = self.player.pos.move(dx, dy)

        # 境界チェック
        new_x = max(0, min(self.map_width - 1, new_pos.x))
        new_y = max(0, min(self.map_height - 1, new_pos.y))

        new_player = self.player.move_to(new_x, new_y)
        return self.replace(player=new_player)

    def game_over(self) -> Self:
        """ゲームオーバー状態を返す"""
        return self.replace(is_game_over=True)


def create_initial_state(
    map_width: int = 20,
    map_height: int = 10,
    player_start: tuple[int, int] = (5, 5),
) -> GameState:
    """
    ゲームの初期状態を生成する

    Args:
        map_width: マップの幅
        map_height: マップの高さ
        player_start: プレイヤーの開始位置

    Returns:
        初期状態のGameState
    """
    player = Entity(
        id="player",
        name="Player",
        pos=Position(x=player_start[0], y=player_start[1]),
    )

    return GameState(
        player=player,
        map_width=map_width,
        map_height=map_height,
    )
