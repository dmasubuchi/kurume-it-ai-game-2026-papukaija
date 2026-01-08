# AI × Game Development Tutorial

久留米工業大学 2026年1月9日講義

## このチュートリアルについて

ターン制ゲームの実装を通じて、以下を学びます：

1. **ゲームループ** - 入力→更新→描画の基本サイクル
2. **状態管理** - 不変データ構造による安全な状態管理
3. **入出力分離** - 副作用の分離とテスタビリティ
4. **テキストレンダリング** - 純粋関数による画面生成
5. **DSL** - 簡易言語のLexer/Parser実装

## 始め方

```bash
cd 02_tutorial
python main.py
```

## ステップ一覧

| Step | 内容 | 実行方法 |
|------|------|----------|
| 00 | Hello World | `python examples/step_00_hello/main.py` |
| 01 | ゲームループ | `python examples/step_01_game_loop/main.py` |
| 02 | 状態管理 | `python examples/step_02_state/main.py` |
| 03 | 入出力 | `python examples/step_03_io/main.py` |
| 04 | レンダラー | `python examples/step_04_renderer/main.py` |
| 05 | Lexer | `python examples/step_05_lexer/main.py` |
| 06 | Parser | `python examples/step_06_parser/main.py` |

## SAVE管理

- **setup**: テンプレートから新規作成
- **reset**: テンプレート状態に戻す
- **copy**: スロット間コピー
- **delete**: スロット削除

## 設計原則

- **Pure Renderer**: `render(state) -> str`（printしない！）
- **Immutable State**: 状態は常に新しいオブジェクトを返す
- **Side Effect Isolation**: 副作用は `io.py` に集約
