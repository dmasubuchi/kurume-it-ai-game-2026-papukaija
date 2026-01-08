# kurume-it-ai-game-2026-papukaija

久留米工業大学「AI技術の活用（ゲームとAI）」講義教材 2026

## 概要

このリポジトリは、2026年1月9日の久留米工業大学講義で使用する教材です。
ターン制ゲームの実装を通じて、AIとゲーム開発の基礎を学びます。

## ディレクトリ構造

```
kurume-it-ai-game-2026-papukaija/
├── README.md              # このファイル
├── 01_lectures/           # 講義資料
│   ├── slides/           # PowerPointスライド
│   ├── docs/             # 講義レポート・章別資料
│   └── knowledge/        # ナレッジベース
├── 02_tutorial/           # 実装チュートリアル
│   ├── main.py           # エントリーポイント
│   ├── src/              # ソースコード
│   ├── examples/         # 各ステップの実行例
│   ├── tutorial/         # ステップ別解説
│   ├── saves/            # SAVEデータ（.gitignore）
│   └── templates/        # 初期テンプレート
├── 03_exercises/          # 演習課題（今後追加）
└── tools/                 # スライド生成ツール
```

## クイックスタート

### 1. チュートリアルを始める

```bash
cd 02_tutorial
python main.py
```

### 2. SAVEスロットをセットアップ

メニューで `4) Manage Saves` → `setup A` を実行

### 3. 各ステップを試す

```bash
# Step 00: Hello World
python examples/step_00_hello/main.py

# Step 01: ゲームループ
python examples/step_01_game_loop/main.py

# Step 02: 状態管理
python examples/step_02_state/main.py

# Step 03: 入出力
python examples/step_03_io/main.py

# Step 04: レンダラー
python examples/step_04_renderer/main.py

# Step 05: Lexer
python examples/step_05_lexer/main.py

# Step 06: Parser
python examples/step_06_parser/main.py
```

## 学習内容

| Step | トピック | 学ぶこと |
|------|---------|---------|
| 00 | プロジェクト設定 | Python環境、プロジェクト構造 |
| 01 | ゲームループ | 入力→更新→描画のサイクル |
| 02 | 状態管理 | 不変データ構造、frozen dataclass |
| 03 | 入出力 | 副作用の分離、テスト容易性 |
| 04 | レンダラー | 純粋関数 `render(state) -> str` |
| 05 | Lexer | トークン化、DSL基礎 |
| 06 | Parser | AST、構文解析 |

## 設計原則

1. **Pure Renderer**: `render(state) -> str` - printしない、文字列を返すだけ
2. **Immutable State**: 状態は変更せず、新しいオブジェクトを返す
3. **Side Effect Isolation**: 副作用は `io.py` に集約

## 動作環境

- Python 3.12+
- 標準ライブラリのみ使用（外部依存なし）

## ライセンス

教育目的での使用を許可します。

---

久留米工業大学 2026年1月9日講義
