# Game Loop Specification

## Overview

ゲームループは、ゲームの心臓部です。
入力 → 更新 → 描画 のサイクルを繰り返します。

## Requirements

### Requirement: Turn-Based Loop

ターン制のゲームループを実装する。

**Rationale:** 学習・デバッグを優先するため、リアルタイムではなくターン制から始める。

#### Scenario: Basic turn cycle

```gherkin
Given the game is running
When the player provides input
Then the game state is updated once
And the game is rendered once
```

#### Scenario: Empty input

```gherkin
Given the game is running
When the player provides empty input
Then the game state is NOT updated
And the game waits for next input
```

### Requirement: Game Loop Function

`run_game_loop()` 関数を提供する。

**Signature:**
```python
def run_game_loop(
    state: GameState,
    get_input: Callable[[], str],
    update: Callable[[GameState, str], GameState],
    render: Callable[[GameState], str],
    output: Callable[[str], None]
) -> GameState:
    ...
```

#### Scenario: Loop with quit command

```gherkin
Given the game is running
When the player inputs "quit"
Then the game loop exits
And the final state is returned
```

### Requirement: Pure Update Function

update関数は新しいStateを返し、元のStateを変更しない。

#### Scenario: State immutability

```gherkin
Given an initial state
When update is called
Then the original state is unchanged
And a new state is returned
```

## Non-Requirements

- リアルタイムループ（Step 07以降で追加）
- フレームレート制御（Step 07以降で追加）
- delta time（Step 07以降で追加）
