"""
レンダラー - 状態を視覚化する

このモジュールは状態を文字列に変換します。
最も重要なルール：print禁止！副作用なし！

render(state) -> str  # これだけ！
"""

from dataclasses import dataclass, field
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.state import GameState, Entity


@dataclass
class TextGrid:
    """
    テキストベースのグリッド描画クラス

    2次元のテキストグリッドを管理し、
    文字を配置して最終的に文字列として出力します。
    """

    width: int
    height: int
    fill: str = "."
    grid: list[list[str]] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        """グリッドを初期化"""
        self.grid = [[self.fill] * self.width for _ in range(self.height)]

    def set(self, x: int, y: int, char: str) -> None:
        """
        指定位置に文字を設定する

        Args:
            x: X座標（0から始まる）
            y: Y座標（0から始まる）
            char: 設定する文字（1文字）
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = char[0] if char else self.fill

    def get(self, x: int, y: int) -> str:
        """
        指定位置の文字を取得する

        Args:
            x: X座標
            y: Y座標

        Returns:
            その位置の文字（範囲外の場合は空文字）
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return ""

    def fill_rect(self, x: int, y: int, w: int, h: int, char: str) -> None:
        """
        矩形領域を塗りつぶす

        Args:
            x: 左上X座標
            y: 左上Y座標
            w: 幅
            h: 高さ
            char: 塗りつぶす文字
        """
        for dy in range(h):
            for dx in range(w):
                self.set(x + dx, y + dy, char)

    def draw_text(self, x: int, y: int, text: str) -> None:
        """
        テキストを横に描画する

        Args:
            x: 開始X座標
            y: Y座標
            text: 描画するテキスト
        """
        for i, char in enumerate(text):
            self.set(x + i, y, char)

    def draw_box(self, x: int, y: int, w: int, h: int, char: str = "#") -> None:
        """
        枠線を描画する

        Args:
            x: 左上X座標
            y: 左上Y座標
            w: 幅
            h: 高さ
            char: 枠線の文字
        """
        # 上下の線
        for dx in range(w):
            self.set(x + dx, y, char)
            self.set(x + dx, y + h - 1, char)
        # 左右の線
        for dy in range(h):
            self.set(x, y + dy, char)
            self.set(x + w - 1, y + dy, char)

    def render(self) -> str:
        """
        グリッドを文字列に変換する（副作用なし！）

        Returns:
            グリッドの文字列表現
        """
        return "\n".join("".join(row) for row in self.grid)

    def copy(self) -> "TextGrid":
        """グリッドのコピーを作成する"""
        new_grid = TextGrid(self.width, self.height, self.fill)
        for y in range(self.height):
            for x in range(self.width):
                new_grid.grid[y][x] = self.grid[y][x]
        return new_grid


def add_border(grid: TextGrid, char: str = "#") -> TextGrid:
    """
    グリッドの周囲に枠を追加する

    Args:
        grid: 元のグリッド
        char: 枠線の文字

    Returns:
        枠付きの新しいグリッド
    """
    new_width = grid.width + 2
    new_height = grid.height + 2
    new_grid = TextGrid(new_width, new_height, char)

    # 内側をコピー
    for y in range(grid.height):
        for x in range(grid.width):
            new_grid.set(x + 1, y + 1, grid.get(x, y))

    return new_grid


def create_game_renderer(
    char_mapping: dict[str, str] | None = None,
    show_status: bool = True,
    show_log: bool = True,
) -> Callable[["GameState"], str]:
    """
    GameState用のレンダラーを作成する

    Args:
        char_mapping: エンティティ種別→描画文字のマッピング
        show_status: ステータス行を表示するか
        show_log: ログを表示するか

    Returns:
        レンダラー関数
    """
    default_mapping = {
        "player": "@",
        "enemy": "E",
        "item": "!",
        "wall": "#",
        "floor": ".",
    }
    mapping = {**default_mapping, **(char_mapping or {})}

    def render(state: "GameState") -> str:
        """状態を文字列に変換する（副作用なし！）"""
        lines: list[str] = []

        # ステータス行
        if show_status:
            lines.append(f"Turn: {state.turn}  Score: {state.score}  HP: {state.player.hp}")
            lines.append("")

        # マップ描画
        grid = TextGrid(state.map_width, state.map_height, mapping["floor"])

        # エンティティを描画
        for entity in state.entities:
            if entity.is_active:
                char = mapping.get(entity.id, "?")
                grid.set(entity.pos.x, entity.pos.y, char)

        # プレイヤーを描画（最後に描画して上書き優先）
        grid.set(state.player.pos.x, state.player.pos.y, mapping["player"])

        # 枠付きで出力
        bordered = add_border(grid)
        lines.append(bordered.render())

        # ログ
        if show_log and state.log_messages:
            lines.append("")
            for msg in state.log_messages[-3:]:  # 最新3件
                lines.append(f"  {msg}")

        lines.append("")
        return "\n".join(lines)

    return render


# デフォルトのシンプルなレンダラー
def simple_render(state: "GameState") -> str:
    """
    シンプルなレンダラー（副作用なし！）

    Args:
        state: ゲーム状態

    Returns:
        画面の文字列表現
    """
    lines: list[str] = []

    lines.append(f"=== Turn {state.turn} ===")
    lines.append(f"Player: ({state.player.pos.x}, {state.player.pos.y})")
    lines.append("")

    # マップ
    for y in range(state.map_height):
        row = ""
        for x in range(state.map_width):
            if x == state.player.pos.x and y == state.player.pos.y:
                row += "@"
            else:
                row += "."
        lines.append(row)

    lines.append("")
    return "\n".join(lines)
