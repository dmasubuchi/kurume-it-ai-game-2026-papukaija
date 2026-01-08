# Step 03: 入力処理（I/O層）

## 学習目標

- 副作用を分離する設計を理解する
- I/O層の責務を学ぶ
- テスト可能なコードを書く方法を学ぶ

## 概要

I/O層は「副作用の境界」です。
print, input などの副作用を持つ操作をここに集約することで、
他のコード（render, update等）を純粋関数として保てます。

**設計原則:**
- 副作用はI/O層にのみ存在
- render(), update() は純粋関数
- テスト時はI/Oをモックに差し替え

## 仕様

`openspec/specs/core/io-layer/spec.md` を参照

## 実装ファイル

- `src/core/io.py` - I/O関数

## 成果物

1. `src/core/io.py`
2. `examples/step_03_io/main.py` - 動作例

## 受け入れ条件

- [ ] `get_input()` で標準入力を取得できる
- [ ] `output()` で標準出力に表示できる
- [ ] `clear_screen()` で画面をクリアできる
- [ ] モック入力でテストできる
- [ ] `python examples/step_03_io/main.py` が動作する

## コード例

```python
# 本番用
def get_input() -> str:
    return input("> ").strip()

# テスト用モック
def create_mock_input(commands: list[str]):
    it = iter(commands)
    def mock_input() -> str:
        return next(it, "quit")
    return mock_input
```

## 次のステップ

Step 04 ではTextGridレンダラーを実装します。
