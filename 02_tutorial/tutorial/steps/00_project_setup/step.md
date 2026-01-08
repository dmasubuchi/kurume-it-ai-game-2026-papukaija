# Step 00: プロジェクトセットアップ

## 学習目標

- プロジェクト構造を理解する
- ゲーム開発の基本的な設計パターンを知る
- 「動くHello World」を作成する

## 概要

このステップでは、ゲーム開発チュートリアルの基盤を構築します。
エンジンを使わずに、Pythonの標準ライブラリのみでゲームを作る準備をします。

## 前提知識

- Python 3.12+ の基本文法
- コマンドライン操作

## ディレクトリ構造

```
game-dev-tutorial/
├── openspec/          # 仕様管理
├── tutorial/steps/    # 各ステップの仕様
├── src/               # 実装コード
│   ├── core/          # コア機能
│   ├── dsl/           # DSL関連
│   └── algorithms/    # AIアルゴリズム
├── examples/          # 動作例
└── tests/             # テスト
```

## 成果物

1. 基本ディレクトリ構造
2. `examples/step_00_hello/main.py` - 最小限の動作確認

## 受け入れ条件

- [ ] `python examples/step_00_hello/main.py` が実行できる
- [ ] "Hello, Game Dev Tutorial!" と表示される
- [ ] `openspec list` でプロジェクトが認識される

## 次のステップ

Step 01 ではゲームループの基礎を実装します。
