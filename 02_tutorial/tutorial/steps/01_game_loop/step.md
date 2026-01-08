# Step 01: ゲームループ基礎

## 学習目標

- ゲームループの概念を理解する
- 入力 → 更新 → 描画 のサイクルを実装する
- 関数の責務分離を学ぶ

## 概要

ゲームは「無限ループ」で動きます。
毎フレーム（またはターン）、同じ処理を繰り返します：

```
while running:
    input = get_input()
    state = update(state, input)
    output = render(state)
    display(output)
```

このステップでは、最も単純なターン制ゲームループを実装します。

## 仕様

`openspec/specs/core/game-loop/spec.md` を参照

## 実装ファイル

- `src/core/game_loop.py` - ゲームループ関数

## 成果物

1. `src/core/game_loop.py`
2. `examples/step_01_game_loop/main.py` - 動作例

## 受け入れ条件

- [ ] `run_game_loop()` がターン制で動作する
- [ ] "quit" 入力でループが終了する
- [ ] update関数がStateを変更せず新しいStateを返す
- [ ] `python examples/step_01_game_loop/main.py` が動作する

## コード例

```python
# 最小限のゲームループ
def run_game_loop(state, get_input, update, render, output):
    while True:
        # 描画
        output(render(state))

        # 入力取得
        cmd = get_input()
        if cmd == "quit":
            break

        # 状態更新
        state = update(state, cmd)

    return state
```

## 次のステップ

Step 02 では State（ゲーム状態）の設計を学びます。
