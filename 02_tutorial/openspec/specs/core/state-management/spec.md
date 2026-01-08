# State Management Specification

## Overview

Stateはゲーム世界の「今」を表すデータです。
すべてのゲーム情報はStateに集約され、唯一の真実となります。

## Requirements

### Requirement: Immutable State

Stateは不変（immutable）であること。

**Rationale:**
- デバッグしやすい（状態の変化を追跡できる）
- 副作用を防ぐ
- undo/redo が実装しやすい

#### Scenario: State is frozen dataclass

```gherkin
Given a GameState instance
When trying to modify its attributes
Then an error is raised
```

### Requirement: State Factory

`create_initial_state()` でゲームの初期状態を生成する。

#### Scenario: Create initial state

```gherkin
When create_initial_state is called
Then a valid GameState is returned
And all entities have default positions
And player is at start position
```

### Requirement: State Update

状態更新は新しいStateを返す。元のStateは変更しない。

```python
def update_state(state: GameState, action: Action) -> GameState:
    # 元の state は変更しない
    return GameState(...)
```

#### Scenario: Replace method

```gherkin
Given a GameState with player at (0, 0)
When replace(player_x=5) is called
Then a new GameState is returned
And the new state has player at (5, 0)
And the original state still has player at (0, 0)
```

### Requirement: GameState Structure

基本的なGameStateは以下の構造を持つ：

```python
@dataclass(frozen=True)
class GameState:
    # プレイヤー情報
    player_x: int
    player_y: int
    player_hp: int

    # ゲーム進行
    turn: int
    score: int
    is_game_over: bool

    # エンティティ（タプルで不変性を保つ）
    entities: tuple[Entity, ...]
```

## Non-Requirements

- 複雑なネスト構造（Step 07以降で追加）
- シリアライズ/デシリアライズ（Step 07以降で追加）
