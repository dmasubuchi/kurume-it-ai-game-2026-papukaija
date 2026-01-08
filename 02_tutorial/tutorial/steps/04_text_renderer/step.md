# Step 04: TextGridレンダラー

## 学習目標

- 純粋関数としてのレンダリングを理解する
- TextGridを使ったグリッド描画を実装する
- 状態からビューへの変換を学ぶ

## 概要

Rendererは状態を「見える形」に変換します。
最も重要なルールは「副作用なし」です：

```python
def render(state: GameState) -> str:
    # print禁止！
    # 副作用なし！
    return "画面の文字列表現"
```

このルールにより：
- テストが容易になる
- 状態の変化を追跡しやすい
- 描画先を簡単に切り替えられる

## 仕様

`openspec/specs/core/renderer/spec.md` を参照

## 実装ファイル

- `src/core/renderer.py` - TextGrid, render関数

## 成果物

1. `src/core/renderer.py`
2. `examples/step_04_renderer/main.py` - 動作例

## 受け入れ条件

- [ ] TextGridクラスが動作する
- [ ] render()は文字列を返す（printしない）
- [ ] プレイヤーと敵を描画できる
- [ ] 枠（ボーダー）を追加できる
- [ ] `python examples/step_04_renderer/main.py` が動作する

## コード例

```python
class TextGrid:
    def __init__(self, width: int, height: int, fill: str = "."):
        self.width = width
        self.height = height
        self.grid = [[fill] * width for _ in range(height)]

    def set(self, x: int, y: int, char: str) -> None:
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = char

    def render(self) -> str:
        return "\n".join("".join(row) for row in self.grid)
```

## 次のステップ

Step 05 ではDSL（独自言語）のレクサーを実装します。
