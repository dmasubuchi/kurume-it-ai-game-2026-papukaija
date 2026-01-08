# Project Context

## Purpose

ゲーム開発の基礎を「要素分解→DSL→Interpreter→アルゴリズム追加」で学べる教育用チュートリアルリポジトリ。
ゲームエンジンを使わずに、ゲームがどのように動作するかを理解することを目的とする。

**目標:**
- ゲームループの仕組みを理解する
- 状態管理の設計パターンを学ぶ
- DSL（Domain Specific Language）とインタプリタの実装を体験する
- A*経路探索、FSM、ビヘイビアツリーなどのゲームAIアルゴリズムを実装する

## Tech Stack

- **言語**: Python 3.12+
- **UI**: CLI（TextGrid描画）
- **依存**: 標準ライブラリのみ（外部パッケージ禁止）
- **テスト**: pytest（開発依存のみ）
- **仕様管理**: OpenSpec

## Project Conventions

### Code Style

- PEP 8 準拠
- Type hints 必須
- docstring: Google style
- 関数名・変数名: snake_case
- クラス名: PascalCase
- 定数: UPPER_SNAKE_CASE

### Architecture Patterns

**ゲームループ（ターン制）:**
```
1入力 = 1更新 = 1描画
```

**Renderer（副作用禁止）:**
```python
def render(state: GameState) -> str:
    # print禁止、文字列を返すだけ
    ...
```

**State（唯一の真実）:**
- 真実は State にのみ存在
- Renderer/Logger/Parser が State を勝手に変えない

**ルール実行:**
```
DSL → Lexer → Parser → Interpreter → State更新
```

### Testing Strategy

- 各モジュールにユニットテスト
- `render()` は純粋関数なのでテスト容易
- `examples/` で統合テスト相当の動作確認

### Git Workflow

- feature branch → main へ PR
- commit message: `step_XX: 簡潔な説明`

## Domain Context

**ゲームの最小構成要素:**
1. 入力（Input）: プレイヤーからの操作
2. 状態（State）: ゲーム世界の「今」
3. ロジック（Logic）: 状態を変化させるルール
4. 出力（Output）: 状態の視覚化

**DSLの役割:**
- ゲームルールをデータとして記述
- Interpreter がルールを実行
- update() で state を直接書き換えない

## Important Constraints

1. **標準ライブラリのみ**: pip install 不要で動くこと
2. **ターン制**: リアルタイムは後回し（学習・デバッグ優先）
3. **副作用禁止**: render() は print しない
4. **エラーで落ちない**: 不正入力はログに残して無視
5. **仕様駆動**: 先に OpenSpec で仕様を書いてから実装

## External Dependencies

なし（標準ライブラリのみ）

## Step構成

| Step | タイトル | 成果物 |
|------|---------|--------|
| 00 | プロジェクトセットアップ | 基本構造 |
| 01 | ゲームループ基礎 | game_loop.py |
| 02 | State管理 | state.py |
| 03 | 入力処理 | io.py |
| 04 | TextGridレンダラー | renderer.py |
| 05 | DSLレクサー | lexer.py |
| 06 | DSLパーサー | parser.py |
| 07+ | アルゴリズム追加 | astar.py, fsm.py, etc. |
