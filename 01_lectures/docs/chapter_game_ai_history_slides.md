# 第2部：技術史（ゲームAIは何と戦ってきたか）

複雑性・状態・決定性との闘争史

## ゲームAIの3つの敵

- 複雑性（Complexity）：組み合わせ爆発、探索空間の指数的増大
- 状態（State）：ゲーム世界の「今」をどう表現し、追跡するか
- 決定性（Determinism）：同じ入力に対して、予測可能で再現可能な振る舞いをどう保証するか
- この3つの敵との戦いが、ゲームAI技術の進化を形作ってきた

## 第1章：黎明期（1950-1970年代）

チェスとゲーム理論の始まり

## クロード・シャノンの1950年論文

- ゲームAIの歴史は、Shannon (1950) "Programming a Computer for Playing Chess" に始まる
- チェスの探索空間を初めて計算
- 合法手の平均：約35手
- 平均ゲーム長：約80手（40手×両プレイヤー）
- 可能な局面数：約10^120（シャノン数）

## シャノンの2つの戦略

- Type A（力任せ探索）
- 全ての可能な手を一定深さまで探索
- 評価関数で末端ノードを評価
- ミニマックス法で最善手を選択
- Type B（選択的探索）
- 有望な手のみを深く探索
- 人間のような「直感」をアルゴリズム化
- 現代のモンテカルロ木探索の先駆け

## ミニマックス法（Minimax）

- 相手が最善手を打つと仮定して、自分の最善手を選ぶ
- 自分のターン：評価値を最大化（Max）
- 相手のターン：評価値を最小化（Min）
- 問題点：探索ノード数は O(b^d)
- b = 分岐数（チェスで約35）
- d = 探索深さ
- 深さ6で約18億ノード

## アルファベータ枝刈り（1958年）

- 発明者：Allen Newell、Herbert Simon
- 出典：Knuth & Moore (1975) "An Analysis of Alpha-Beta Pruning"
- 明らかに悪い手を探索しない
- α：自分の最低保証スコア
- β：相手の最高許容スコア
- α ≧ β なら枝刈り
- 効果：最良の場合 O(b^(d/2)) に削減

## 第2章：アーケードゲームの時代（1970-80年代）

決定論的AIの黄金期

## パックマンのゴーストAI（1980年）

- Namcoの岩谷徹が設計
- キャラクターごとに異なるAI性格を実装した最初のゲーム
- 4体のゴーストが異なるアルゴリズムで動く
- 出典：Pittman (2011) "The Pac-Man Dossier"

## 4体のゴーストの行動アルゴリズム

- Blinky（赤・おいかけ）：パックマンの現在位置を追跡
- Pinky（ピンク・まちぶせ）：パックマンの4タイル前方を狙う
- Inky（青・きまぐれ）：Blinkyとパックマンの位置から計算
- Clyde（橙・おとぼけ）：距離8タイル以上なら追跡、以下なら自分の隅へ

## Inkyのターゲット計算（最も複雑）

- パックマンの2タイル前方の位置を取得
- Blinkyからその位置へのベクトルを計算
- そのベクトルを2倍に延長した位置がターゲット
- 結果：Blinkyと挟み撃ちになる動き
- 単純なルールの組み合わせで複雑な行動を生成

## 決定論的AIの利点と限界

- 利点
- メモリ使用量が極めて少ない
- デバッグが容易（同じ入力→同じ出力）
- プレイヤーが「パターン」を学習できる
- 限界
- 一度パターンを覚えると簡単すぎる
- 「知性」を感じない
- 複雑な行動の実装が困難

## 第3章：有限状態機械の時代（1980-90年代）

FSM（Finite State Machine）

## FSMの基礎

- 有限個の状態の集合と、状態間の遷移規則で定義
- Q：状態の有限集合
- Σ：入力アルファベット（イベント）の有限集合
- δ：遷移関数（Q × Σ → Q）
- q0：初期状態
- 例：PATROL → CHASE → ATTACK → FLEE

## FSMの実装例（敵キャラクター）

- PATROL状態：巡回行動
- プレイヤー発見 → CHASEへ遷移
- CHASE状態：追跡行動
- 距離が近い → ATTACKへ遷移
- 体力低下 → FLEEへ遷移
- ATTACK状態：攻撃行動
- FLEE状態：逃走行動

## FSMの状態爆発問題

- 問題：状態数と遷移数が指数的に増加
- 3条件（視認、体力、弾薬）：2^3 = 8状態
- 5条件：2^5 = 32状態
- 10条件：2^10 = 1024状態
- Half-Life (1998) の敵AI
- 50以上の状態が必要に
- 遷移の組み合わせが管理不能
- バグの特定が困難

## 階層型FSM（HFSM）の解決策

- 状態をネストして階層化
- Combat（上位状態）
- Aggressive → Charge, Attack
- Defensive → TakeCover, Retreat
- NonCombat（上位状態）
- Patrol, Investigate
- 上位状態の遷移で下位状態全体を切り替え

## 第4章：ビヘイビアツリーの登場（2000年代）

Halo 2と行動木の発明

## Halo 2のAI革命（2004年）

- 開発者：Damian Isla（Bungie）
- FSMの限界を打破する新アーキテクチャ
- 出典：Isla (2005) "Handling Complexity in the Halo 2 AI" GDC 2005
- 現在のゲームAIの標準手法となる

## ビヘイビアツリーの構造

- 木構造で行動を階層的に記述
- ルートから毎フレーム評価（Tick）
- 各ノードはSUCCESS / FAILURE / RUNNINGを返す
- 子ノードの結果に基づいて親が判断

## ノードタイプ：Composite（複合）

- Selector（選択）
- 子を順に評価、最初の成功で終了
- 「どれか一つを実行」
- Sequence（順序）
- 子を順に実行、全て成功で成功
- 「全てを順番に実行」
- Parallel（並列）
- 複数の子を同時実行

## ノードタイプ：Decorator / Leaf

- Decorator（装飾）
- Inverter：結果を反転
- Repeater：繰り返し実行
- Succeeder：常に成功を返す
- Leaf（葉）
- Action：実際の行動を実行
- Condition：条件をチェック

## BTがFSMを超える理由

- 状態の追加：ノード追加のみ（FSM：全遷移を再検討）
- 並列行動：Parallelノードで容易（FSM：困難）
- 再利用性：サブツリーとして再利用可能
- 可読性：階層構造で明確
- デバッグ：実行パスが視覚化可能

## Unreal Engine 4への統合（2014年）

- Epic GamesがUE4に標準搭載
- Blackboard：AIの知識データベース
- Service：定期実行のバックグラウンドタスク
- Observer Aborts：条件変化時の即座の中断
- 業界標準として普及

## 第5章：計画型AI（2000-2010年代）

GOAP と HTN

## GOAP（Goal-Oriented Action Planning）

- 起源：F.E.A.R.（Monolith, 2005）
- 開発者：Jeff Orkin（MIT Media Lab出身）
- 出典：Orkin (2006) "Three States and a Plan: The A.I. of F.E.A.R." GDC 2006
- 行動を「どう動くか」ではなく「何を達成するか」から逆算

## GOAPの仕組み

- World State：現在の状態（Key-Value）
- 例：enemy_alive=true, weapon_loaded=false
- Goal：達成したい状態
- 例：enemy_alive=false
- Action：前提条件と効果を持つ
- Reload：前提{ammo>0}, 効果{loaded=true}
- Shoot：前提{loaded=true}, 効果{enemy_alive=false}
- Planner：A*でWorld State→Goalへの行動列を探索

## F.E.A.R.のAIが革命的だった理由

- 従来：IF-THEN-ELSEのスクリプト
- if visible and health>50 then attack
- GOAP：目標だけを与える
- 「敵を排除せよ」
- AIが自律的に計画：カバー→リロード→射撃
- 結果：フランキング、制圧射撃、連携行動が自然発生

## HTN（Hierarchical Task Network）

- GOAPの限界：単純行動の組み合わせのみ
- HTNの解決策：タスクを階層的に分解
- 高レベル：「敵を倒す」
- 方法1：近接攻撃 → 接近、殴る
- 方法2：射撃 → 構える、照準、撃つ
- 方法3：爆発物 → 取り出す、投げる、退避
- 出典：Hoang et al. (2005) "Hierarchical Plan Representations for Encoding Strategic Game AI"

## 第6章：空間認識と経路探索

A*、NavMesh、影響マップ

## A*アルゴリズム（1968年）

- 発明者：Hart, Nilsson, Raphael（スタンフォード研究所）
- 出典：Hart et al. (1968) "A Formal Basis for the Heuristic Determination of Minimum Cost Paths"
- f(n) = g(n) + h(n)
- g(n)：開始点からnまでの実コスト
- h(n)：nから目標までの推定コスト
- h(n)が許容的なら最適解を保証

## ナビゲーションメッシュ（NavMesh）

- 従来のウェイポイント方式の問題
- 手動配置が大変
- 経路が不自然
- 動的障害物への対応困難
- NavMeshの原理
- 歩行可能領域を凸多角形で分割
- 多角形の隣接関係でグラフ構築
- A*で多角形間の経路を探索

## Recast/Detour（2009年）

- 開発者：Mikko Mononen
- オープンソースのNavMesh生成・経路探索ライブラリ
- 採用例
- Unity
- Unreal Engine
- 多くのAAAゲーム
- 業界標準となる

## 影響マップ（Influence Map）

- 用途：戦術的な位置評価
- 各ユニットが周囲に「影響」を及ぼす
- 距離に応じて影響度を減衰
- 味方：正の影響（安全）
- 敵：負の影響（危険）
- 応用：カバー位置選択、フランキング経路計算
- 出典：Tozour (2001) "Influence Mapping" Game Programming Gems 2

## 第7章：強化学習の時代（2010年代-現在）

DQN、AlphaGo、OpenAI Five

## Deep Q-Network（DQN, 2015）

- DeepMindのブレークスルー
- Atari 2600のゲームを画面ピクセルのみから学習
- 出典：Mnih et al. (2015) "Human-level control through deep reinforcement learning" Nature
- 入力：84x84x4（4フレーム分）
- CNN + 全結合層
- 出力：各行動のQ値

## DQNの技術的革新

- Experience Replay
- 過去の経験をバッファに保存
- ランダムサンプリングで学習
- データの相関を破壊し安定化
- Target Network
- Q値の更新対象と評価対象を分離
- 学習の発振を防止

## AlphaGo / AlphaZero（2016-2017）

- AlphaGo (2016)
- モンテカルロ木探索 + 深層学習
- 人間の棋譜で事前学習 + 自己対戦
- 出典：Silver et al. (2016) Nature
- AlphaZero (2017)
- 人間の知識を一切使わない
- ルールのみから自己対戦で学習
- チェス、将棋、囲碁で人間を超える

## OpenAI Five（2018-2019）

- Dota 2の5v5チーム戦を強化学習
- 約45,000年分の自己対戦（分散計算）
- 世界チャンピオンチームに勝利
- 技術：LSTM、PPO、1万以上の行動空間
- 出典：Berner et al. (2019) "Dota 2 with Large Scale Deep Reinforcement Learning"

## 強化学習が商用ゲームで普及しない理由

- 学習コスト
- 数千〜数百万時間の学習
- 大規模計算リソースが必要
- 再現性の問題
- ランダムシード依存
- 同じ学習を再現できない

## 強化学習の商用化の壁（続き）

- 説明可能性の欠如
- なぜその行動か説明不能
- バグ原因特定が困難
- QA（品質保証）が困難
- バランス調整の困難さ
- 「少しだけ弱く」が困難
- 再学習が必要

## 強化学習の現実的な適用領域

- NPCの動作生成（アニメーション遷移）
- 自動ゲームテスト
- ゲームバランス調整の補助
- 「ゲームプレイAI」ではなく「開発支援AI」として活用

## 第8章：象徴的事例研究

Halo 2、Left 4 Dead、Suphx

## Halo 2のエンカウンターデザイン

- 「賢さ」だけでなく「面白さ」を重視
- 3つの原則（Butcher & Griesemer, GDC 2002）
- 反応的であれ：プレイヤーの行動に即座に反応
- 予測可能であれ：プレイヤーが「読める」行動
- 間違いを犯せ：完璧すぎるAIは面白くない

## Left 4 Dead のAI Director（2008年）

- プレイヤー状況に応じてゲームペースを動的調整
- Intensity（緊張度）のモデル
- 戦闘中：緊張度 ↑
- 安全地帯：緊張度 ↓
- 仲間ダウン：緊張度 ↑↑
- 出典：Booth (2009) "The AI Systems of Left 4 Dead"

## AI Directorのスポーン制御

- 緊張度が高い
- スポーン抑制
- 回復アイテム増加
- 緊張度が低い
- 大群スポーン
- 特殊感染者投入
- Peak-Valley設計
- 緊張のピークと谷を交互に配置
- 「恐怖→安堵」の心理サイクル

## 麻雀AI Suphx（Microsoft, 2019）

- 典型的な不完全情報ゲームへの挑戦
- 相手の手牌が見えない
- 山牌の内容が不明
- 他家の待ち・鳴き意図が不明
- 出典：Li et al. (2020) "Suphx: Mastering Mahjong with Deep Reinforcement Learning"

## Suphxの技術

- Oracle Guiding
- 完全情報を知る「神」の行動を模倣学習
- Self-Play
- 自己対戦による強化学習
- 多視点学習
- 4人全ての視点で学習
- 成果：天鳳で十段達成、人間トップを超える

## 第9章：LLM時代のゲームAI（2023年-）

可能性と限界

## LLMの可能性

- NPCとの自然言語対話
- Character.ai、Inworld AI
- 事前定義されたセリフからの脱却
- 動的コンテンツ生成
- ストーリー分岐の自動生成
- クエストの動的作成
- 世界設定の即興生成

## LLMのゲームAIとしての根本的問題

- レイテンシ
- 応答に数百ms〜数秒
- 60FPSでは16.7ms以内に判断必要
- 決定論性の欠如
- 同じ入力に異なる出力
- 再現可能なデバッグが困難

## LLMの限界（続き）

- 状態管理の弱さ
- 長期的一貫性の維持が困難
- 「3ターン前の約束」を忘れる
- 幻覚（Hallucination）
- 存在しないアイテムや能力を参照
- ゲームルールの逸脱

## ハイブリッドアプローチ

- 現実的な解決策
- LLM（創造性・自然言語）
- ↓
- ルールベースフィルター（安全性・一貫性）
- ↓
- ゲーム状態管理（決定論・検証可能性）
- ↓
- 実行

## NPCの対話システム例

- LLMが応答候補を生成
- ゲームロジックが整合性をチェック
- 不整合な内容は修正または却下
- 有効な応答のみをプレイヤーに提示
- LLMは「脳」、ルールベースは「身体」

## 第10章：技術史の教訓

変わらない3つの敵

## 繰り返されるパターン

- 新技術の登場
- 「万能だ！」という期待
- 現実の制約との衝突
- 適用領域の限定
- 他技術とのハイブリッド化
- 成熟した実用的手法へ

## 変わらない敵①：複雑性

- FSM → Behavior Tree → GOAP → HTN
- 複雑性を「管理」する方法が進化
- 複雑性そのものは消えない
- 「どう整理するか」の技術競争

## 変わらない敵②：状態

- ワールドモデルの精緻化
- Blackboard、影響マップ
- しかし「完全な世界モデル」は常に不可能
- 何を表現し、何を捨てるかの設計判断

## 変わらない敵③：決定性

- 学習型AIは決定性と相性が悪い
- ゲームでは再現可能性が品質保証に直結
- ルールベースと学習型のハイブリッドが現実解
- 「どこまで決定論的であるべきか」の設計判断

## AIが進化しても変わらないこと

- どのAI技術を「選択」するかは人間の判断
- AIの行動が「面白いか」を評価するのは人間
- バグの原因を「特定」するのは人間
- AIの失敗の「責任」を取るのは人間

## 主要参考文献（学術論文）

- Shannon (1950) "Programming a Computer for Playing Chess"
- Hart et al. (1968) "A Formal Basis for the Heuristic Determination of Minimum Cost Paths"
- Mnih et al. (2015) "Human-level control through deep reinforcement learning"
- Silver et al. (2016, 2017) AlphaGo / AlphaZero論文
- Li et al. (2020) "Suphx: Mastering Mahjong with Deep Reinforcement Learning"

## 主要参考文献（GDC講演）

- Isla (2005) "Handling Complexity in the Halo 2 AI"
- Orkin (2006) "Three States and a Plan: The A.I. of F.E.A.R."
- Booth (2009) "The AI Systems of Left 4 Dead"
- Butcher & Griesemer (2002) "The Illusion of Intelligence"

## まとめ：技術史から学ぶこと

- 新技術は万能ではない
- 適用領域を見極める目が重要
- ハイブリッド化が現実解
- 3つの敵（複雑性・状態・決定性）は消えない
- 人間の判断・評価・責任は残り続ける
