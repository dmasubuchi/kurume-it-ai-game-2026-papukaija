# AI × Game Development Tutorial

久留米工業大学 2026年1月9日講義

## このチュートリアルについて

ターン制ゲームの実装を通じて、以下を学びます：

### Part 1: ゲームエンジン基礎 (Step 01-04)
1. **ゲームループ** - 入力→更新→描画の基本サイクル
2. **状態管理** - 不変データ構造による安全な状態管理
3. **入出力分離** - 副作用の分離とテスタビリティ
4. **テキストレンダリング** - 純粋関数による画面生成

### Part 2: DSL実装 (Step 05-07)
5. **Lexer** - 文字列をトークンに分割
6. **Parser** - トークンからASTを構築
7. **Interpreter** - ASTを評価し状態を更新

### Part 3: AI技術 (Step 08-13)
8. **A*経路探索** - 最短経路アルゴリズム
9. **FSM敵AI** - 有限状態機械による行動制御
10. **Behavior Tree敵AI** - ツリー構造による意思決定
11. **GOAP敵AI** - 目標指向行動計画
12. **Director AI** - ゲーム体験全体の制御
13. **Human x AI x Rules** - 責任分界の理解

## 始め方

```bash
cd 02_tutorial
python main.py
```

## ステップ一覧

### Part 1: ゲームエンジン基礎

| Step | 内容 | 概要 |
|------|------|------|
| 00 | Hello World | プロジェクト確認 |
| 01 | ゲームループ | 入力→更新→描画サイクル |
| 02 | 状態管理 | 不変データ構造 |
| 03 | 入出力分離 | 副作用の分離 |
| 04 | レンダラー | 純粋関数による画面生成 |

### Part 2: DSL実装

| Step | 内容 | 概要 |
|------|------|------|
| 05 | Lexer | 文字列→トークン分割 |
| 06 | Parser | トークン→AST構築 |
| 07 | Interpreter | AST→状態更新 |

### Part 3: AI技術

| Step | 内容 | 概要 |
|------|------|------|
| 08 | A*経路探索 | 最短経路を計算しMOVE命令を生成 |
| 09 | FSM敵AI | IDLE/CHASE/FLEE状態遷移 |
| 10 | BT敵AI | Selector/Sequence/Condition/Action |
| 11 | GOAP敵AI | 目標から行動列を逆算 |
| 12 | Director | Tensionでゲーム体験を制御 |
| 13 | Integration | 人間・AI・ルールの統合 |

## 核心コンセプト：AIはDSL命令を生成する

```
Human Input ─┐
             ├─→ DSL Command ─→ Interpreter ─→ State Update
AI Decision ─┘

例: FSM(CHASE) → "move enemy 1 0" → Interpreter実行 → 敵が移動
```

すべてのAI（FSM/BT/GOAP/Director）は直接状態を変更せず、
**DSL命令を生成**し、**Interpreterが実行**します。

## SAVE管理

- **setup**: テンプレートから新規作成
- **reset**: テンプレート状態に戻す
- **copy**: スロット間コピー
- **delete**: スロット削除

## 設計原則

- **Pure Renderer**: `render(state) -> str`（printしない！）
- **Immutable State**: 状態は常に新しいオブジェクトを返す
- **Side Effect Isolation**: 副作用は `io.py` に集約
- **AI generates DSL**: AIは命令を生成し、Interpreterが実行する
