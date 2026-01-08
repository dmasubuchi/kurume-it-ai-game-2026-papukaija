# I/O Layer Specification

## Overview

I/O層は、入出力の「副作用」を集約する場所です。
print、input などの副作用を持つ操作はここにのみ存在し、
他のモジュール（render, update等）は純粋関数として保たれます。

## Requirements

### Requirement: Input Abstraction

入力を抽象化し、様々なソースから取得できるようにする。

#### Scenario: Standard input

```gherkin
Given the io module is imported
When get_input() is called
Then it returns a string from standard input
```

#### Scenario: Mock input for testing

```gherkin
Given a mock input queue ["up", "down", "quit"]
When get_input is called 3 times
Then it returns "up", "down", "quit" in order
```

### Requirement: Output Abstraction

出力を抽象化し、様々な出力先に対応する。

#### Scenario: Print output

```gherkin
Given the io module is imported
When output("Hello") is called
Then "Hello" is printed to stdout
```

### Requirement: Screen Clear

画面をクリアする機能を提供する。

#### Scenario: Clear terminal

```gherkin
Given the io module is imported
When clear_screen() is called
Then the terminal is cleared
```

### Requirement: Input with Prompt

プロンプトを表示して入力を取得する。

```python
def get_input_with_prompt(prompt: str = "> ") -> str:
    return input(prompt).strip()
```

## Non-Requirements

- GUI入出力（このチュートリアルはCLIのみ）
- ネットワーク入出力
