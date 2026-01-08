# Renderer Specification

## Overview

Rendererは状態を視覚的表現（文字列）に変換します。
最も重要な特性は「副作用なし」です。printを行わず、文字列を返すだけです。

## Requirements

### Requirement: Pure Function

render関数は純粋関数であること。

**Signature:**
```python
def render(state: GameState) -> str:
    # print禁止！
    # 副作用なし！
    return "..."
```

#### Scenario: No side effects

```gherkin
Given a render function
When render(state) is called
Then no output is printed to stdout
And a string is returned
```

### Requirement: TextGrid

テキストベースのグリッド描画機能を提供する。

```python
class TextGrid:
    def __init__(self, width: int, height: int, fill: str = "."):
        ...

    def set(self, x: int, y: int, char: str) -> None:
        ...

    def get(self, x: int, y: int) -> str:
        ...

    def render(self) -> str:
        ...
```

#### Scenario: Create grid

```gherkin
Given width=5 and height=3
When TextGrid is created
Then a 5x3 grid is initialized
And all cells contain "."
```

#### Scenario: Set cell

```gherkin
Given a 5x3 TextGrid
When set(2, 1, "@") is called
Then cell at (2, 1) becomes "@"
```

### Requirement: Render State to TextGrid

GameStateをTextGridに描画する。

#### Scenario: Render player

```gherkin
Given a GameState with player at (3, 2)
When render_to_grid(state, grid) is called
Then the grid has "@" at (3, 2)
```

### Requirement: Border and Frame

グリッドの周囲に枠を追加できる。

```python
def add_border(grid: TextGrid, char: str = "#") -> TextGrid:
    ...
```

## Non-Requirements

- 色付け（ANSIカラー）は後のステップで追加
- アニメーション
- スプライト（複数文字のエンティティ）
