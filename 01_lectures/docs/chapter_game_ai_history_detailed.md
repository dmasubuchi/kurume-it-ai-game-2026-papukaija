# 第2部：技術史（ゲームAIは何と戦ってきたか）

## 複雑性・状態・決定性との闘争史

---

## 序：ゲームAIの3つの敵

ゲームAIは誕生以来、3つの根本的な敵と戦い続けてきた。

- 複雑性（Complexity）：組み合わせ爆発、探索空間の指数的増大
- 状態（State）：ゲーム世界の「今」をどう表現し、追跡するか
- 決定性（Determinism）：同じ入力に対して、予測可能で再現可能な振る舞いをどう保証するか

この3つの敵との戦いが、ゲームAI技術の進化を形作ってきた。

---

## 第1章：黎明期（1950-1970年代）

### 1.1 チェスとゲーム理論の始まり

ゲームAIの歴史は、クロード・シャノンの1950年の論文に始まる。

**出典：**
- Shannon, C. E. (1950). "Programming a Computer for Playing Chess." *Philosophical Magazine*, Ser.7, Vol. 41, No. 314.

シャノンは、チェスの探索空間を計算した。

- 合法手の平均：約35手
- 平均ゲーム長：約80手（40手×両プレイヤー）
- 可能な局面数：約10^120（シャノン数）

**シャノンの2つの戦略：**

1. **Type A（力任せ探索）**
   - 全ての可能な手を一定深さまで探索
   - 評価関数で末端ノードを評価
   - ミニマックス法で最善手を選択

2. **Type B（選択的探索）**
   - 有望な手のみを深く探索
   - 人間のような「直感」をアルゴリズム化
   - 現代のモンテカルロ木探索の先駆け

### 1.2 ミニマックス法とアルファベータ枝刈り

**ミニマックス法（Minimax）**

```
function minimax(node, depth, maximizingPlayer):
    if depth == 0 or node is terminal:
        return evaluate(node)

    if maximizingPlayer:
        value = -∞
        for each child of node:
            value = max(value, minimax(child, depth-1, false))
        return value
    else:
        value = +∞
        for each child of node:
            value = min(value, minimax(child, depth-1, true))
        return value
```

**問題点：** 探索ノード数は O(b^d)（b=分岐数、d=深さ）

**アルファベータ枝刈り（Alpha-Beta Pruning）**

1958年、アレン・ニューウェルとハーバート・サイモンが発明。

```
function alphabeta(node, depth, α, β, maximizingPlayer):
    if depth == 0 or node is terminal:
        return evaluate(node)

    if maximizingPlayer:
        value = -∞
        for each child of node:
            value = max(value, alphabeta(child, depth-1, α, β, false))
            α = max(α, value)
            if α >= β:
                break  # β cut-off
        return value
    else:
        value = +∞
        for each child of node:
            value = min(value, alphabeta(child, depth-1, α, β, true))
            β = min(β, value)
            if β <= α:
                break  # α cut-off
        return value
```

**効果：** 最良の場合、探索ノード数を O(b^(d/2)) に削減。

**出典：**
- Knuth, D. E., & Moore, R. W. (1975). "An Analysis of Alpha-Beta Pruning." *Artificial Intelligence*, 6(4), 293-326.

---

## 第2章：アーケードゲームの時代（1970-1980年代）

### 2.1 パックマンのゴーストAI（1980年）

パックマン（Namco, 1980）は、キャラクターごとに異なるAI性格を実装した最初のゲームの一つ。

**4体のゴーストの行動アルゴリズム：**

| ゴースト | 日本名 | 性格 | ターゲット計算 |
|---------|--------|------|----------------|
| Blinky | 赤ベイ（おいかけ） | 追跡者 | パックマンの現在位置 |
| Pinky | ピンキー（まちぶせ） | 待ち伏せ | パックマンの4タイル前方 |
| Inky | 青ベイ（きまぐれ） | 気まぐれ | Blinkyとパックマンの位置から計算 |
| Clyde | 愚鈍（おとぼけ） | 愚鈍 | 距離8タイル以上→パックマン、以下→自分の隅 |

**Inkyのターゲット計算（最も複雑）：**
1. パックマンの2タイル前方の位置を取得
2. Blinkyからその位置へのベクトルを計算
3. そのベクトルを2倍に延長した位置がターゲット

**状態マシン：**
```
[Scatter] ←→ [Chase] ←→ [Frightened]
    ↑            ↑            ↑
    └────────────┴────────────┘
         タイマーで自動遷移
```

**出典：**
- Pittman, J. (2011). "The Pac-Man Dossier." *Gamasutra*.
- Iwatani, T. (Creator of Pac-Man). GDC講演資料.

### 2.2 決定論的AIの限界

この時代のAIは完全に決定論的だった。

**利点：**
- メモリ使用量が極めて少ない（状態を保存する必要がない）
- デバッグが容易（同じ入力→同じ出力）
- プレイヤーが「パターン」を学習できる（攻略の楽しさ）

**限界：**
- 一度パターンを覚えると、ゲームが簡単になりすぎる
- 「知性」を感じない
- 複雑な行動を実装するのが困難

---

## 第3章：有限状態機械の時代（1980-1990年代）

### 3.1 FSM（Finite State Machine）の基礎

**定義：**
FSMは、有限個の状態の集合と、状態間の遷移規則で定義される計算モデル。

**形式的定義：**
- Q：状態の有限集合
- Σ：入力アルファベット（イベント）の有限集合
- δ：遷移関数（Q × Σ → Q）
- q0：初期状態
- F：受理状態の集合（ゲームAIでは通常使用しない）

**実装例（敵キャラクターAI）：**

```python
class EnemyFSM:
    def __init__(self):
        self.state = "PATROL"

    def update(self, player_distance, health):
        if self.state == "PATROL":
            if player_distance < 10:
                self.state = "CHASE"
            # パトロール行動
            self.patrol()

        elif self.state == "CHASE":
            if player_distance > 15:
                self.state = "PATROL"
            elif player_distance < 2:
                self.state = "ATTACK"
            elif health < 20:
                self.state = "FLEE"
            # 追跡行動
            self.chase_player()

        elif self.state == "ATTACK":
            if player_distance > 2:
                self.state = "CHASE"
            elif health < 20:
                self.state = "FLEE"
            # 攻撃行動
            self.attack()

        elif self.state == "FLEE":
            if health > 50:
                self.state = "PATROL"
            # 逃走行動
            self.flee()
```

### 3.2 FSMの状態爆発問題

**問題：** 状態数と遷移数が指数的に増加する。

例：3つの独立した条件（敵の視認、体力、弾薬）を考慮する場合

- 単純FSM：2^3 = 8状態が必要
- 5つの条件：2^5 = 32状態
- 10の条件：2^10 = 1024状態

**Half-Life（1998）の敵AI：**

Valveの開発者は、FSMの限界に直面した。

- 兵士AIに50以上の状態が必要になった
- 遷移の組み合わせが管理不能に
- バグの特定が困難に

**出典：**
- Isla, D. (2005). "Handling Complexity in the Halo 2 AI." *GDC 2005*.

### 3.3 階層型FSM（HFSM）

**解決策：** 状態をネストして階層化する。

```
[Combat]
├── [Aggressive]
│   ├── [Charge]
│   └── [Attack]
└── [Defensive]
    ├── [TakeCover]
    └── [Retreat]

[NonCombat]
├── [Patrol]
└── [Investigate]
```

**利点：**
- 関連する状態をグループ化
- 上位状態の遷移で、下位状態全体を切り替え可能
- コードの再利用性向上

**限界：**
- 依然として状態爆発の根本解決にはならない
- 並列行動の表現が困難

---

## 第4章：ビヘイビアツリーの登場（2000年代）

### 4.1 Halo 2と行動木の発明（2004年）

**背景：**
Halo 2（Bungie, 2004）の開発中、AIプログラマーのDamian Islaは、FSMの限界を打破する新しいアーキテクチャを考案した。

**ビヘイビアツリー（Behavior Tree）の構造：**

```
        [Selector]
       /    |    \
  [Sequence] [Sequence] [Action]
   /    \     /    \      Patrol
Attack Flee Cover Shoot
```

**ノードタイプ：**

1. **Composite（複合ノード）**
   - **Selector（選択）**：子ノードを順に評価し、最初に成功したものを実行
   - **Sequence（順序）**：子ノードを順に実行し、全て成功で成功
   - **Parallel（並列）**：複数の子ノードを同時実行

2. **Decorator（装飾ノード）**
   - **Inverter**：子の結果を反転
   - **Repeater**：子を指定回数繰り返す
   - **Succeeder**：常に成功を返す

3. **Leaf（葉ノード）**
   - **Action**：実際の行動を実行
   - **Condition**：条件をチェック

**実装例：**

```python
class Node:
    def tick(self):
        raise NotImplementedError

class Selector(Node):
    def __init__(self, children):
        self.children = children

    def tick(self):
        for child in self.children:
            result = child.tick()
            if result == SUCCESS:
                return SUCCESS
            if result == RUNNING:
                return RUNNING
        return FAILURE

class Sequence(Node):
    def __init__(self, children):
        self.children = children

    def tick(self):
        for child in self.children:
            result = child.tick()
            if result == FAILURE:
                return FAILURE
            if result == RUNNING:
                return RUNNING
        return SUCCESS
```

**出典：**
- Isla, D. (2005). "Handling Complexity in the Halo 2 AI." *GDC 2005*.
- Champandard, A. J. (2007). "Understanding Behavior Trees." *AiGameDev.com*.

### 4.2 ビヘイビアツリーがFSMを超える理由

| 観点 | FSM | Behavior Tree |
|------|-----|---------------|
| 状態の追加 | 全遷移を再検討 | ノード追加のみ |
| 並列行動 | 困難 | Parallelノードで容易 |
| 再利用性 | 低い | サブツリーとして再利用可能 |
| 可読性 | 状態図が複雑化 | 階層構造で明確 |
| デバッグ | 状態遷移の追跡が困難 | 実行パスが視覚化可能 |

### 4.3 Unreal Engine 4への統合

2014年、Epic GamesはUnreal Engine 4にビヘイビアツリーを標準搭載。

**UE4のBT拡張機能：**
- **Blackboard**：AIの知識データベース
- **Service**：定期的に実行されるバックグラウンドタスク
- **Observer Aborts**：条件変化時の即座の中断

---

## 第5章：計画型AI（2000-2010年代）

### 5.1 GOAP（Goal-Oriented Action Planning）

**起源：**
F.E.A.R.（Monolith Productions, 2005）で初めて商用ゲームに実装。

**開発者：** Jeff Orkin（MIT Media Lab出身）

**出典：**
- Orkin, J. (2003). "Applying Goal-Oriented Action Planning to Games." *AI Game Programming Wisdom 2*.
- Orkin, J. (2006). "Three States and a Plan: The A.I. of F.E.A.R." *GDC 2006*.

**GOAPの仕組み：**

1. **World State（世界状態）**：現在の状態をKey-Valueで表現
2. **Goal（目標）**：達成したい状態
3. **Action（行動）**：前提条件と効果を持つ
4. **Planner（計画器）**：A*などで行動列を探索

**例：敵を倒すという目標**

```
現在の世界状態:
{
  "enemy_alive": true,
  "weapon_loaded": false,
  "ammo_count": 10,
  "in_cover": false
}

目標:
{
  "enemy_alive": false
}

利用可能な行動:
- Reload: 前提{ammo_count > 0}, 効果{weapon_loaded: true, ammo_count: -1}
- Shoot: 前提{weapon_loaded: true}, 効果{enemy_alive: false, weapon_loaded: false}
- TakeCover: 前提{}, 効果{in_cover: true}

計画結果: [Reload] → [Shoot]
```

**A*によるプラン探索：**

```python
def plan(start_state, goal, actions):
    open_set = [(0, start_state, [])]  # (コスト, 状態, 行動列)
    closed_set = set()

    while open_set:
        cost, state, plan = heapq.heappop(open_set)

        if goal_satisfied(state, goal):
            return plan

        state_key = frozenset(state.items())
        if state_key in closed_set:
            continue
        closed_set.add(state_key)

        for action in actions:
            if preconditions_met(state, action):
                new_state = apply_effects(state, action)
                new_cost = cost + action.cost
                heapq.heappush(open_set, (new_cost, new_state, plan + [action]))

    return None  # 計画失敗
```

### 5.2 F.E.A.R.のAIが革命的だった理由

**従来のAI（スクリプト型）：**
```
IF player_visible AND health > 50 THEN attack
ELSE IF player_visible AND health <= 50 THEN take_cover
ELSE patrol
```

**F.E.A.R.のGOAP AI：**
- 目標「敵を排除する」を与えるだけ
- AIが自律的に「カバーを取る→リロード→射撃」を計画
- 状況に応じて計画を動的に変更

**結果：**
- 兵士AIが「賢く」見える行動を自然に生成
- フランキング（側面攻撃）、制圧射撃、連携行動
- 開発者は行動の組み合わせを全て記述する必要がない

### 5.3 HTN（Hierarchical Task Network）

**GOAPの限界：**
- 単純な行動のみで複雑なタスクを表現しにくい
- 行動の順序に関する知識を活かしにくい

**HTN（階層型タスクネットワーク）：**

```
高レベルタスク: 敵を倒す
├── 方法1: 近接攻撃
│   ├── 接近する
│   └── 殴る
├── 方法2: 射撃
│   ├── 武器を構える
│   ├── 照準を合わせる
│   └── 撃つ
└── 方法3: 爆発物使用
    ├── グレネードを取り出す
    ├── 投げる
    └── 退避する
```

**Primitive Task（基本タスク）**：直接実行可能な行動
**Compound Task（複合タスク）**：より小さなタスクに分解される

**出典：**
- Erol, K., Hendler, J., & Nau, D. S. (1994). "HTN Planning: Complexity and Expressivity." *AAAI-94*.
- Hoang, H., Lee-Urban, S., & Muñoz-Avila, H. (2005). "Hierarchical Plan Representations for Encoding Strategic Game AI." *AIIDE 2005*.

---

## 第6章：空間認識と経路探索

### 6.1 A*アルゴリズム（1968年）

**発明者：** Peter Hart, Nils Nilsson, Bertram Raphael（スタンフォード研究所）

**出典：**
- Hart, P. E., Nilsson, N. J., & Raphael, B. (1968). "A Formal Basis for the Heuristic Determination of Minimum Cost Paths." *IEEE Transactions on Systems Science and Cybernetics*, 4(2), 100-107.

**アルゴリズム：**

```python
def a_star(start, goal, graph, heuristic):
    open_set = [(0, start)]
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == goal:
            return reconstruct_path(came_from, current)

        for neighbor in graph.neighbors(current):
            tentative_g = g_score[current] + graph.cost(current, neighbor)

            if tentative_g < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None  # パスなし
```

**f(n) = g(n) + h(n)**
- g(n)：開始点からnまでの実コスト
- h(n)：nから目標までのヒューリスティック（推定コスト）
- h(n)が許容的（実際のコスト以下）なら最適解を保証

### 6.2 ナビゲーションメッシュ（NavMesh）

**従来のウェイポイント方式の問題：**
- 手動配置が大変
- 経路が不自然（直線的）
- 動的な障害物への対応が困難

**NavMeshの原理：**
- 歩行可能な領域を凸多角形で分割
- 多角形の隣接関係でグラフを構築
- A*で多角形間の経路を探索

**Recast/Detour（Mikko Mononen, 2009）：**

オープンソースのNavMesh生成・経路探索ライブラリ。
Unity、Unreal Engine、多くのAAAゲームで採用。

**出典：**
- Mononen, M. (2009). "Recast Navigation." GitHub Repository.
- Snook, G. (2000). "Simplified 3D Movement and Pathfinding Using Navigation Meshes." *Game Programming Gems*.

### 6.3 影響マップ（Influence Map）

**用途：** 戦術的な位置評価

```python
def calculate_influence_map(width, height, units):
    influence = [[0.0] * width for _ in range(height)]

    for unit in units:
        for y in range(height):
            for x in range(width):
                distance = math.sqrt((x - unit.x)**2 + (y - unit.y)**2)
                # 距離に応じて影響度を減衰
                inf = unit.strength / (1 + distance * 0.5)
                if unit.team == ENEMY:
                    influence[y][x] -= inf
                else:
                    influence[y][x] += inf

    return influence
```

**応用例：**
- 正の値：味方支配領域（安全）
- 負の値：敵支配領域（危険）
- カバー位置の選択、フランキング経路の計算に使用

**出典：**
- Tozour, P. (2001). "Influence Mapping." *Game Programming Gems 2*.
- Miles, D. (2013). "Building a Better Centaur: AI at Massive Scale." *GDC 2013*.

---

## 第7章：強化学習の時代（2010年代-現在）

### 7.1 Deep Q-Network（DQN, 2013-2015）

**DeepMindのブレークスルー：**

Atari 2600のゲームを、画面ピクセルのみから学習。

**出典：**
- Mnih, V., et al. (2015). "Human-level control through deep reinforcement learning." *Nature*, 518(7540), 529-533.

**アーキテクチャ：**
```
入力: 84x84x4 (4フレーム分のグレースケール画像)
    ↓
Conv1: 32フィルタ, 8x8, stride 4
    ↓
Conv2: 64フィルタ, 4x4, stride 2
    ↓
Conv3: 64フィルタ, 3x3, stride 1
    ↓
全結合: 512ユニット
    ↓
出力: 各行動のQ値
```

**Experience Replay：**
- 過去の経験をバッファに保存
- ランダムサンプリングで学習
- 連続するデータの相関を破壊し、学習を安定化

**Target Network：**
- Q値の更新対象と評価対象を分離
- 学習の発振を防止

### 7.2 AlphaGo / AlphaZero（2016-2017）

**AlphaGo（2016）：**
- モンテカルロ木探索 + 深層学習
- 人間の棋譜で事前学習 + 自己対戦で強化学習

**AlphaZero（2017）：**
- 人間の知識を一切使わない
- ルールのみから自己対戦で学習
- チェス、将棋、囲碁で人間とAlphaGoを超える

**出典：**
- Silver, D., et al. (2016). "Mastering the game of Go with deep neural networks and tree search." *Nature*, 529(7587), 484-489.
- Silver, D., et al. (2017). "Mastering Chess and Shogi by Self-Play with a General Reinforcement Learning Algorithm." *arXiv:1712.01815*.

### 7.3 OpenAI Five（2018-2019）

**Dota 2での成果：**
- 5v5のチーム戦を強化学習で学習
- 約45,000年分の自己対戦（分散計算）
- 世界チャンピオンチームに勝利

**技術的特徴：**
- LSTM（長期記憶）の使用
- PPO（Proximal Policy Optimization）アルゴリズム
- 1万以上の行動空間
- 約2万の観測変数

**出典：**
- OpenAI (2019). "OpenAI Five." *OpenAI Blog*.
- Berner, C., et al. (2019). "Dota 2 with Large Scale Deep Reinforcement Learning." *arXiv:1912.06680*.

### 7.4 強化学習の商用ゲームでの現実

**なぜAAAゲームでは強化学習が普及しないのか：**

1. **学習コスト**
   - 数千〜数百万時間の学習時間
   - 大規模な計算リソースが必要

2. **再現性の問題**
   - 学習結果がランダムシードに依存
   - 同じ学習を再現できない

3. **説明可能性の欠如**
   - なぜその行動を選んだか説明できない
   - バグの原因特定が困難
   - QA（品質保証）が困難

4. **バランス調整の困難さ**
   - 「少しだけ弱くする」が困難
   - 難易度調整がパラメータ調整ではなく再学習

**現実的な適用領域：**
- NPCの動作生成（アニメーション遷移）
- 自動ゲームテスト
- ゲームバランス調整の補助

---

## 第8章：象徴的事例研究

### 8.1 Halo 2のエンカウンターデザイン（2004）

**Encounter（遭遇戦）の設計哲学：**

Bungieは、AIの「賢さ」だけでなく「面白さ」を重視した。

**3つの原則：**
1. **反応的であれ**：プレイヤーの行動に即座に反応
2. **予測可能であれ**：プレイヤーが「読める」行動
3. **間違いを犯せ**：完璧すぎるAIは面白くない

**出典：**
- Butcher, C., & Griesemer, J. (2002). "The Illusion of Intelligence: The Integration of AI and Level Design in Halo." *GDC 2002*.

### 8.2 Left 4 Dead のAI Director（2008）

**概要：**
プレイヤーの状況に応じて、ゲームのペースを動的に調整。

**Intensity（緊張度）のモデル：**
```
緊張度の更新:
- 敵との戦闘中: 緊張度 ↑
- 安全地帯: 緊張度 ↓ (時間経過)
- 仲間がダウン: 緊張度 ↑↑

スポーン制御:
- 緊張度が高い: スポーン抑制、回復アイテム増加
- 緊張度が低い: 大群スポーン、特殊感染者投入
```

**Peak-Valley設計：**
- 緊張のピークと谷を交互に配置
- 心理学的な「恐怖→安堵」のサイクル

**出典：**
- Booth, M. (2009). "The AI Systems of Left 4 Dead." *AI Game Programming Wisdom 4*.
- Valve (2008). "Left 4 Dead AI Director." GDC講演.

### 8.3 麻雀AI Suphx（Microsoft, 2019）

**不完全情報ゲームへの挑戦：**

麻雀は、典型的な不完全情報ゲーム。
- 相手の手牌が見えない
- 山牌の内容が不明
- 他家の待ち・鳴き意図が不明

**Suphxの技術：**
1. **Oracle Guiding**：完全情報を知っている「神」の行動を模倣学習
2. **Self-Play**：自己対戦による強化学習
3. **多視点学習**：4人のプレイヤー全ての視点で学習

**成果：**
- 天鳳（オンライン麻雀）で十段を達成
- 人間のトッププレイヤーを超える成績

**出典：**
- Li, J., et al. (2020). "Suphx: Mastering Mahjong with Deep Reinforcement Learning." *arXiv:2003.13590*.

---

## 第9章：LLM時代のゲームAI（2023年-）

### 9.1 LLMの可能性

**NPCとの自然言語対話：**
- Character.ai、Inworld AI
- 事前定義されたセリフからの脱却
- プレイヤーの自由な質問に応答

**動的なコンテンツ生成：**
- ストーリー分岐の自動生成
- クエストの動的作成
- 世界設定の即興生成

### 9.2 LLMの限界

**ゲームAIとしての根本的問題：**

1. **レイテンシ**
   - 応答に数百ミリ秒〜数秒
   - 60FPSのゲームでは16.7ms以内に判断が必要

2. **決定論性の欠如**
   - 同じ入力に異なる出力
   - 再現可能なデバッグが困難

3. **状態管理の弱さ**
   - 長期的な一貫性の維持が困難
   - 「3ターン前に約束したこと」を忘れる

4. **幻覚（Hallucination）**
   - 存在しないアイテムや能力を参照
   - ゲームルールの逸脱

### 9.3 ハイブリッドアプローチ

**現実的な解決策：**

```
[LLM]（創造性・自然言語）
    ↓
[ルールベースフィルター]（安全性・一貫性）
    ↓
[ゲーム状態管理]（決定論・検証可能性）
    ↓
[実行]
```

**例：NPCの対話システム**
1. LLMが応答候補を生成
2. ゲームロジックが整合性をチェック
3. 不整合な内容は修正または却下
4. 有効な応答のみをプレイヤーに提示

---

## 第10章：技術史の教訓

### 10.1 繰り返されるパターン

ゲームAIの歴史は、同じパターンを繰り返している：

```
新技術の登場
    ↓
「万能だ！」という期待
    ↓
現実の制約との衝突
    ↓
適用領域の限定
    ↓
他技術とのハイブリッド化
    ↓
成熟した実用的手法へ
```

### 10.2 変わらない3つの敵

1. **複雑性**
   - FSM → Behavior Tree → GOAP → HTN
   - 複雑性を「管理」する方法が進化

2. **状態**
   - ワールドモデルの精緻化
   - Blackboard、影響マップ
   - しかし「完全な世界モデル」は常に不可能

3. **決定性**
   - 学習型AIは決定性と相性が悪い
   - ゲームでは再現可能性が品質保証に直結
   - ルールベースと学習型のハイブリッドが現実解

### 10.3 人間の役割

**AIが進化しても変わらないこと：**

- どのAI技術を「選択」するかは人間の判断
- AIの行動が「面白いか」を評価するのは人間
- バグの原因を「特定」するのは人間
- AIの失敗の「責任」を取るのは人間

---

## 参考文献一覧

### 学術論文
1. Shannon, C. E. (1950). "Programming a Computer for Playing Chess."
2. Hart, P. E., Nilsson, N. J., & Raphael, B. (1968). "A Formal Basis for the Heuristic Determination of Minimum Cost Paths."
3. Knuth, D. E., & Moore, R. W. (1975). "An Analysis of Alpha-Beta Pruning."
4. Mnih, V., et al. (2015). "Human-level control through deep reinforcement learning."
5. Silver, D., et al. (2016). "Mastering the game of Go."
6. Silver, D., et al. (2017). "Mastering Chess and Shogi by Self-Play."
7. Li, J., et al. (2020). "Suphx: Mastering Mahjong with Deep Reinforcement Learning."

### GDC講演・業界資料
1. Isla, D. (2005). "Handling Complexity in the Halo 2 AI."
2. Orkin, J. (2006). "Three States and a Plan: The A.I. of F.E.A.R."
3. Booth, M. (2009). "The AI Systems of Left 4 Dead."
4. Butcher, C., & Griesemer, J. (2002). "The Illusion of Intelligence."

### 書籍
1. Millington, I., & Funge, J. (2009). *Artificial Intelligence for Games*. Morgan Kaufmann.
2. Rabin, S. (Ed.). *AI Game Programming Wisdom* series.
3. Bourg, D. M., & Seemann, G. (2004). *AI for Game Developers*. O'Reilly.
