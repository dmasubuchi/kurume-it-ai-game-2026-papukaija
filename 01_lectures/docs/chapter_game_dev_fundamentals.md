# ゲーム開発の基礎：要素分解と独自インタプリタの実装

エンジンを使わずに「ゲームとは何か」を理解する

---

## 序：なぜエンジンを使わないのか

### 0.1 ゲームエンジンの功罪

- Unity、Unreal Engine は強力なツール
- しかし「何が起きているか」が隠蔽されている
- ボタン一つで動く → 理解なき完成
- 問題が起きたとき、原因が分からない

### 0.2 ブラックボックス問題

- エンジンは「魔法の箱」になりやすい
- 入力 → ??? → 出力
- 中身を理解していないと応用が効かない
- デバッグができない

### 0.3 本講義のアプローチ

- ゲームを「要素分解」する
- 各要素を「自分で実装」する
- 理解した上でエンジンを使う
- 「なぜ動くか」を説明できるようになる

### 0.4 学習の順序

- Step 1：ゲームの要素分解（概念理解）
- Step 2：最小限のゲームループ実装
- Step 3：入力・状態・描画の分離
- Step 4：簡易インタプリタの実装
- Step 5：アルゴリズムの追加（AI、経路探索等）

---

## 第1章：ゲームとは何か（要素分解）

### 1.1 ゲームの定義

- ルールに基づく相互作用システム
- プレイヤーの入力に応じて状態が変化
- 状態の変化が視覚・聴覚でフィードバックされる
- 目標があり、達成/失敗の判定がある

### 1.2 ゲームの最小構成要素

- 入力（Input）：プレイヤーからの操作
- 状態（State）：ゲーム世界の「今」
- ロジック（Logic）：状態を変化させるルール
- 出力（Output）：状態の視覚化・音響化

### 1.3 ゲームループの概念

- ゲームは「無限ループ」で動く
- 毎フレーム同じ処理を繰り返す
- 入力取得 → 状態更新 → 描画
- このサイクルが1秒間に60回（60FPS）

### 1.4 ゲームループの疑似コード

```
while (game_is_running):
    input = get_input()
    state = update(state, input)
    render(state)
    wait_for_next_frame()
```

### 1.5 フレームレートとは

- FPS（Frames Per Second）：1秒間のフレーム数
- 60FPS = 16.67ms ごとに1フレーム
- 30FPS = 33.33ms ごとに1フレーム
- フレームレートが安定 = 滑らかな動き

### 1.6 固定フレームレート vs 可変フレームレート

- 固定：常に同じ間隔で更新（シンプル）
- 可変：経過時間に応じて更新（柔軟）
- 初学者は固定から始める
- delta time（経過時間）の概念は後で学ぶ

---

## 第2章：状態（State）の設計

### 2.1 状態とは何か

- ゲーム世界の「今この瞬間」を表すデータ
- プレイヤーの位置、体力、スコア
- 敵の位置、状態
- アイテムの有無
- 全てが「変数」として表現される

### 2.2 状態の例：シンプルなゲーム

```python
game_state = {
    "player": {
        "x": 5,
        "y": 3,
        "hp": 100,
        "score": 0
    },
    "enemies": [
        {"x": 10, "y": 5, "hp": 30},
        {"x": 15, "y": 8, "hp": 30}
    ],
    "items": [
        {"x": 7, "y": 2, "type": "coin"},
        {"x": 12, "y": 6, "type": "health"}
    ],
    "game_over": False,
    "frame_count": 0
}
```

### 2.3 状態の不変性と更新

- 状態は「上書き」ではなく「新しい状態を生成」が理想
- 古い状態を保持 → デバッグしやすい
- リプレイ機能の実装が容易
- 実際には効率のため上書きすることも多い

### 2.4 状態遷移図

- ゲームの状態を図で表現
- タイトル → プレイ中 → ゲームオーバー → タイトル
- 状態遷移を明確にすると設計がクリアになる

```
[Title] ---(Start)---> [Playing]
   ^                      |
   |                      v
   +----(Retry)---- [GameOver]
```

### 2.5 グローバル状態 vs ローカル状態

- グローバル状態：ゲーム全体で共有
- ローカル状態：特定のオブジェクトが持つ
- バランスが重要
- 全てグローバル → スパゲッティコード
- 全てローカル → 情報共有が困難

### 2.6 状態の永続化

- セーブ/ロード機能
- 状態を JSON や バイナリで保存
- 再開時に状態を復元
- 状態が整理されていると実装が容易

---

## 第3章：入力（Input）の処理

### 3.1 入力の種類

- キーボード：キーの押下/解放
- マウス：位置、クリック、ドラッグ
- ゲームパッド：ボタン、スティック
- タッチ：タップ、スワイプ、ピンチ

### 3.2 入力の状態

- 押された瞬間（Press / Down）
- 押し続けている（Hold）
- 離された瞬間（Release / Up）
- これらを区別することが重要

### 3.3 入力状態の管理

```python
class InputManager:
    def __init__(self):
        self.current_keys = set()   # 今フレームで押されているキー
        self.previous_keys = set()  # 前フレームで押されていたキー

    def update(self, pressed_keys):
        self.previous_keys = self.current_keys.copy()
        self.current_keys = pressed_keys

    def is_pressed(self, key):
        """押し続けている"""
        return key in self.current_keys

    def is_just_pressed(self, key):
        """今フレームで押された"""
        return key in self.current_keys and key not in self.previous_keys

    def is_just_released(self, key):
        """今フレームで離された"""
        return key not in self.current_keys and key in self.previous_keys
```

### 3.4 入力のバッファリング

- 入力は「いつ」処理されるかが重要
- 格闘ゲーム：コマンド入力のバッファ
- アクションゲーム：先行入力
- バッファサイズと猶予フレーム

### 3.5 入力の抽象化

- 具体的なキー → 抽象的なアクション
- 「Wキー」→「上に移動」
- 「スペースキー」→「ジャンプ」
- キーコンフィグが実装しやすくなる

```python
input_mapping = {
    "move_up": ["W", "UP_ARROW"],
    "move_down": ["S", "DOWN_ARROW"],
    "jump": ["SPACE"],
    "attack": ["Z", "ENTER"]
}
```

### 3.6 入力遅延と応答性

- 入力から反映までの時間
- 遅延が大きい → 操作が「重い」
- 目標：1-2フレーム以内の応答
- 入力処理はゲームループの最初に

---

## 第4章：ロジック（Logic）の実装

### 4.1 ロジックとは

- 状態を変化させるルール
- 入力に基づく変化（プレイヤー操作）
- 時間に基づく変化（敵の移動、タイマー）
- イベントに基づく変化（衝突、アイテム取得）

### 4.2 更新関数の基本構造

```python
def update(state, input, delta_time):
    # プレイヤーの更新
    state = update_player(state, input, delta_time)

    # 敵の更新
    state = update_enemies(state, delta_time)

    # 衝突判定
    state = check_collisions(state)

    # ゲーム状態の判定
    state = check_game_conditions(state)

    return state
```

### 4.3 プレイヤー移動のロジック

```python
def update_player(state, input, delta_time):
    player = state["player"]
    speed = 5  # 1秒間に5マス移動

    dx, dy = 0, 0
    if input.is_pressed("move_up"):
        dy = -1
    if input.is_pressed("move_down"):
        dy = 1
    if input.is_pressed("move_left"):
        dx = -1
    if input.is_pressed("move_right"):
        dx = 1

    # 正規化（斜め移動が速くならないように）
    if dx != 0 and dy != 0:
        dx *= 0.707  # 1/√2
        dy *= 0.707

    player["x"] += dx * speed * delta_time
    player["y"] += dy * speed * delta_time

    return state
```

### 4.4 衝突判定の基礎

- AABB（Axis-Aligned Bounding Box）
- 矩形同士の重なり判定
- 最も基本的で高速な方法

```python
def check_aabb_collision(a, b):
    """2つの矩形が重なっているか判定"""
    return (a["x"] < b["x"] + b["width"] and
            a["x"] + a["width"] > b["x"] and
            a["y"] < b["y"] + b["height"] and
            a["y"] + a["height"] > b["y"])
```

### 4.5 円形の衝突判定

```python
def check_circle_collision(a, b):
    """2つの円が重なっているか判定"""
    dx = a["x"] - b["x"]
    dy = a["y"] - b["y"]
    distance = math.sqrt(dx * dx + dy * dy)
    return distance < a["radius"] + b["radius"]
```

### 4.6 衝突応答

- 衝突を検出したら何をするか
- 押し戻し（物理的な衝突）
- ダメージ処理（攻撃の衝突）
- アイテム取得（アイテムとの衝突）

```python
def handle_collision(state, entity_a, entity_b):
    if entity_a["type"] == "player" and entity_b["type"] == "enemy":
        # プレイヤーがダメージを受ける
        state["player"]["hp"] -= entity_b["damage"]
    elif entity_a["type"] == "player" and entity_b["type"] == "item":
        # アイテムを取得
        if entity_b["item_type"] == "coin":
            state["player"]["score"] += 10
        entity_b["collected"] = True
    return state
```

### 4.7 ゲームオーバー判定

```python
def check_game_conditions(state):
    # HPが0以下でゲームオーバー
    if state["player"]["hp"] <= 0:
        state["game_over"] = True
        state["result"] = "lose"

    # 全ての敵を倒したらクリア
    alive_enemies = [e for e in state["enemies"] if e["hp"] > 0]
    if len(alive_enemies) == 0:
        state["game_over"] = True
        state["result"] = "win"

    return state
```

---

## 第5章：出力（Output）/ 描画（Rendering）

### 5.1 描画の基本概念

- 状態を視覚化する
- 毎フレーム画面をクリアして再描画
- レイヤー順（背景 → オブジェクト → UI）
- 座標系の理解（左上原点 vs 中央原点）

### 5.2 描画の基本手順

```python
def render(state, screen):
    # 1. 画面クリア
    screen.clear()

    # 2. 背景描画
    render_background(screen)

    # 3. ゲームオブジェクト描画
    render_items(state["items"], screen)
    render_enemies(state["enemies"], screen)
    render_player(state["player"], screen)

    # 4. UI描画
    render_ui(state, screen)

    # 5. 画面更新
    screen.flip()
```

### 5.3 スプライトとは

- 2Dゲームの基本描画単位
- 画像 + 位置 + サイズ
- アニメーション = スプライトの切り替え

```python
class Sprite:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y
        self.width = image.width
        self.height = image.height

    def draw(self, screen):
        screen.blit(self.image, self.x, self.y)
```

### 5.4 アニメーションの実装

```python
class AnimatedSprite:
    def __init__(self, frames, frame_duration):
        self.frames = frames  # 画像のリスト
        self.frame_duration = frame_duration  # 各フレームの表示時間
        self.current_frame = 0
        self.elapsed_time = 0

    def update(self, delta_time):
        self.elapsed_time += delta_time
        if self.elapsed_time >= self.frame_duration:
            self.elapsed_time = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def draw(self, screen, x, y):
        screen.blit(self.frames[self.current_frame], x, y)
```

### 5.5 カメラ（ビューポート）

- ゲーム世界は画面より大きいことが多い
- カメラ = 「どこを見ているか」
- ワールド座標 vs スクリーン座標

```python
class Camera:
    def __init__(self, width, height):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height

    def follow(self, target):
        # ターゲット（プレイヤー）を中央に
        self.x = target["x"] - self.width // 2
        self.y = target["y"] - self.height // 2

    def world_to_screen(self, world_x, world_y):
        return world_x - self.x, world_y - self.y
```

### 5.6 テキスト描画

```python
def render_ui(state, screen):
    # スコア表示
    score_text = f"Score: {state['player']['score']}"
    screen.draw_text(score_text, x=10, y=10, color="white")

    # HP表示
    hp_text = f"HP: {state['player']['hp']}"
    screen.draw_text(hp_text, x=10, y=30, color="red")
```

### 5.7 描画の最適化（基礎）

- 画面外のオブジェクトは描画しない（カリング）
- 静的な背景は事前にレンダリング
- 描画順序の最適化（バッチング）

---

## 第6章：簡易インタプリタの設計

### 6.1 インタプリタとは

- プログラムを1行ずつ解釈・実行する
- コンパイラとの違い
- ゲームエンジンは「ゲーム記述言語のインタプリタ」とも言える

### 6.2 なぜインタプリタを作るのか

- ゲームの動作を「データ」として記述できる
- コードを変更せずにゲーム内容を変更
- モッディング、レベルエディタの基礎
- スクリプト言語の仕組みを理解

### 6.3 簡易ゲーム記述言語の設計

```
# ゲーム定義ファイル例
GAME_TITLE "My First Game"
SCREEN_SIZE 800 600

# エンティティ定義
ENTITY player
  POSITION 100 300
  SIZE 32 32
  SPRITE "player.png"
  SPEED 5
END

ENTITY enemy
  POSITION 600 300
  SIZE 32 32
  SPRITE "enemy.png"
  SPEED 2
  AI patrol
END

# ルール定義
RULE player_enemy_collision
  WHEN player COLLIDES enemy
  THEN player DAMAGE 10
END
```

### 6.4 レクサー（字句解析器）

- テキストを「トークン」に分割
- トークン = 意味のある最小単位

```python
def tokenize(text):
    tokens = []
    lines = text.strip().split('\n')

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        parts = line.split()
        for part in parts:
            if part.startswith('"') and part.endswith('"'):
                tokens.append(('STRING', part[1:-1]))
            elif part.isdigit():
                tokens.append(('NUMBER', int(part)))
            else:
                tokens.append(('KEYWORD', part))

    return tokens
```

### 6.5 パーサー（構文解析器）

- トークン列を構造化されたデータに変換
- AST（抽象構文木）を生成

```python
def parse(tokens):
    game_data = {
        "title": "",
        "screen_size": (800, 600),
        "entities": [],
        "rules": []
    }

    i = 0
    while i < len(tokens):
        token_type, token_value = tokens[i]

        if token_value == "GAME_TITLE":
            game_data["title"] = tokens[i+1][1]
            i += 2
        elif token_value == "ENTITY":
            entity, i = parse_entity(tokens, i+1)
            game_data["entities"].append(entity)
        elif token_value == "RULE":
            rule, i = parse_rule(tokens, i+1)
            game_data["rules"].append(rule)
        else:
            i += 1

    return game_data
```

### 6.6 エンティティのパース

```python
def parse_entity(tokens, start):
    entity = {
        "name": tokens[start][1],
        "position": (0, 0),
        "size": (32, 32),
        "sprite": None,
        "speed": 0,
        "ai": None
    }

    i = start + 1
    while i < len(tokens):
        token_type, token_value = tokens[i]

        if token_value == "END":
            return entity, i + 1
        elif token_value == "POSITION":
            entity["position"] = (tokens[i+1][1], tokens[i+2][1])
            i += 3
        elif token_value == "SIZE":
            entity["size"] = (tokens[i+1][1], tokens[i+2][1])
            i += 3
        elif token_value == "SPRITE":
            entity["sprite"] = tokens[i+1][1]
            i += 2
        elif token_value == "SPEED":
            entity["speed"] = tokens[i+1][1]
            i += 2
        elif token_value == "AI":
            entity["ai"] = tokens[i+1][1]
            i += 2
        else:
            i += 1

    return entity, i
```

### 6.7 インタプリタの実行

```python
class GameInterpreter:
    def __init__(self, game_data):
        self.game_data = game_data
        self.state = self.initialize_state()

    def initialize_state(self):
        state = {
            "entities": {},
            "rules": self.game_data["rules"]
        }

        for entity_def in self.game_data["entities"]:
            entity = {
                "x": entity_def["position"][0],
                "y": entity_def["position"][1],
                "width": entity_def["size"][0],
                "height": entity_def["size"][1],
                "speed": entity_def["speed"],
                "ai": entity_def["ai"]
            }
            state["entities"][entity_def["name"]] = entity

        return state

    def update(self, input_state, delta_time):
        # 入力処理
        self.process_input(input_state, delta_time)

        # AI処理
        self.process_ai(delta_time)

        # ルール評価
        self.evaluate_rules()

        return self.state
```

### 6.8 ルールエンジン

```python
def evaluate_rules(self):
    for rule in self.state["rules"]:
        if self.check_condition(rule["condition"]):
            self.execute_action(rule["action"])

def check_condition(self, condition):
    if condition["type"] == "collision":
        entity_a = self.state["entities"][condition["entity_a"]]
        entity_b = self.state["entities"][condition["entity_b"]]
        return self.check_collision(entity_a, entity_b)
    return False

def execute_action(self, action):
    if action["type"] == "damage":
        target = self.state["entities"][action["target"]]
        target["hp"] = target.get("hp", 100) - action["amount"]
```

---

## 第7章：段階的なゲーム実装

### 7.1 Step 1：最小限のゲームループ

```python
import time

def main():
    # 初期化
    state = {"x": 0, "frame": 0}
    running = True

    # ゲームループ
    while running:
        # 入力（簡略化）
        # 実際はキーボード入力を取得

        # 更新
        state["x"] += 1
        state["frame"] += 1

        # 描画（コンソール出力で代用）
        print(f"Frame {state['frame']}: x = {state['x']}")

        # フレームレート制御
        time.sleep(1/60)  # 60FPS

        if state["frame"] >= 100:
            running = False

if __name__ == "__main__":
    main()
```

### 7.2 Step 2：入力の追加

```python
import sys
import tty
import termios
import select

def get_key():
    """非ブロッキングでキー入力を取得"""
    if select.select([sys.stdin], [], [], 0)[0]:
        return sys.stdin.read(1)
    return None

def main():
    # ターミナル設定
    old_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())

    try:
        state = {"x": 10, "y": 5}
        running = True

        while running:
            key = get_key()

            if key == 'w':
                state["y"] -= 1
            elif key == 's':
                state["y"] += 1
            elif key == 'a':
                state["x"] -= 1
            elif key == 'd':
                state["x"] += 1
            elif key == 'q':
                running = False

            # 描画
            print(f"\033[2J\033[H")  # 画面クリア
            print(f"Position: ({state['x']}, {state['y']})")
            print("WASD to move, Q to quit")

            time.sleep(1/30)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
```

### 7.3 Step 3：テキストベースの描画

```python
def render_text_grid(state, width=20, height=10):
    """テキストでグリッドを描画"""
    grid = [['.' for _ in range(width)] for _ in range(height)]

    # プレイヤーを配置
    px, py = state["player"]["x"], state["player"]["y"]
    if 0 <= px < width and 0 <= py < height:
        grid[py][px] = '@'

    # 敵を配置
    for enemy in state["enemies"]:
        ex, ey = enemy["x"], enemy["y"]
        if 0 <= ex < width and 0 <= ey < height:
            grid[ey][ex] = 'E'

    # アイテムを配置
    for item in state["items"]:
        ix, iy = item["x"], item["y"]
        if 0 <= ix < width and 0 <= iy < height:
            grid[iy][ix] = '*'

    # グリッドを文字列に変換
    result = ""
    result += "+" + "-" * width + "+\n"
    for row in grid:
        result += "|" + "".join(row) + "|\n"
    result += "+" + "-" * width + "+\n"

    return result
```

### 7.4 Step 4：衝突判定の追加

```python
def update_with_collision(state, input_state):
    # プレイヤー移動
    new_x = state["player"]["x"]
    new_y = state["player"]["y"]

    if input_state.get("up"):
        new_y -= 1
    if input_state.get("down"):
        new_y += 1
    if input_state.get("left"):
        new_x -= 1
    if input_state.get("right"):
        new_x += 1

    # 境界チェック
    new_x = max(0, min(new_x, 19))
    new_y = max(0, min(new_y, 9))

    state["player"]["x"] = new_x
    state["player"]["y"] = new_y

    # アイテム衝突チェック
    for item in state["items"]:
        if item["x"] == new_x and item["y"] == new_y and not item.get("collected"):
            item["collected"] = True
            state["player"]["score"] += 10

    # 敵衝突チェック
    for enemy in state["enemies"]:
        if enemy["x"] == new_x and enemy["y"] == new_y:
            state["player"]["hp"] -= 10

    return state
```

### 7.5 Step 5：敵AIの追加

```python
def update_enemy_ai(state, delta_time):
    player = state["player"]

    for enemy in state["enemies"]:
        if enemy.get("ai") == "chase":
            # プレイヤーを追跡
            dx = player["x"] - enemy["x"]
            dy = player["y"] - enemy["y"]

            # 簡易的な移動（1マスずつ）
            if abs(dx) > abs(dy):
                enemy["x"] += 1 if dx > 0 else -1
            elif dy != 0:
                enemy["y"] += 1 if dy > 0 else -1

        elif enemy.get("ai") == "patrol":
            # パトロール（左右往復）
            if not enemy.get("direction"):
                enemy["direction"] = 1

            enemy["x"] += enemy["direction"]

            # 端で反転
            if enemy["x"] <= 0 or enemy["x"] >= 19:
                enemy["direction"] *= -1

    return state
```

### 7.6 Step 6：ゲーム状態の管理

```python
class Game:
    def __init__(self):
        self.state = "title"
        self.game_state = None

    def update(self, input_state):
        if self.state == "title":
            if input_state.get("start"):
                self.state = "playing"
                self.game_state = self.create_initial_state()

        elif self.state == "playing":
            self.game_state = self.update_gameplay(input_state)

            if self.game_state["player"]["hp"] <= 0:
                self.state = "gameover"
            elif self.check_win_condition():
                self.state = "win"

        elif self.state == "gameover" or self.state == "win":
            if input_state.get("restart"):
                self.state = "title"

    def render(self):
        if self.state == "title":
            return "=== MY GAME ===\nPress SPACE to start"
        elif self.state == "playing":
            return render_text_grid(self.game_state)
        elif self.state == "gameover":
            return "GAME OVER\nPress R to restart"
        elif self.state == "win":
            return "YOU WIN!\nPress R to restart"
```

---

## 第8章：アルゴリズムの追加

### 8.1 経路探索（A*）の追加

```python
import heapq

def a_star(grid, start, goal):
    """A*経路探索"""
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def neighbors(pos):
        x, y = pos
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
                if grid[ny][nx] != '#':  # 壁でなければ
                    yield (nx, ny)

    open_set = [(0, start)]
    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            # パスを再構築
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        for neighbor in neighbors(current):
            tentative_g = g_score[current] + 1

            if tentative_g < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score, neighbor))

    return []  # パスなし
```

### 8.2 賢い敵AIへの統合

```python
def update_smart_enemy(enemy, player, grid):
    """A*を使った賢い敵AI"""
    start = (enemy["x"], enemy["y"])
    goal = (player["x"], player["y"])

    path = a_star(grid, start, goal)

    if path:
        # パスの最初の位置に移動
        next_pos = path[0]
        enemy["x"] = next_pos[0]
        enemy["y"] = next_pos[1]
```

### 8.3 FSM（有限状態機械）の追加

```python
class EnemyFSM:
    def __init__(self):
        self.state = "patrol"
        self.patrol_points = [(5, 5), (15, 5), (15, 8), (5, 8)]
        self.patrol_index = 0

    def update(self, enemy, player, grid):
        distance = abs(enemy["x"] - player["x"]) + abs(enemy["y"] - player["y"])

        if self.state == "patrol":
            if distance < 5:
                self.state = "chase"
            else:
                self.do_patrol(enemy)

        elif self.state == "chase":
            if distance > 10:
                self.state = "patrol"
            elif distance < 2:
                self.state = "attack"
            else:
                self.do_chase(enemy, player, grid)

        elif self.state == "attack":
            if distance > 2:
                self.state = "chase"
            else:
                self.do_attack(enemy, player)

    def do_patrol(self, enemy):
        target = self.patrol_points[self.patrol_index]
        if enemy["x"] == target[0] and enemy["y"] == target[1]:
            self.patrol_index = (self.patrol_index + 1) % len(self.patrol_points)
        else:
            # ターゲットに向かって移動
            if enemy["x"] < target[0]:
                enemy["x"] += 1
            elif enemy["x"] > target[0]:
                enemy["x"] -= 1
            elif enemy["y"] < target[1]:
                enemy["y"] += 1
            elif enemy["y"] > target[1]:
                enemy["y"] -= 1

    def do_chase(self, enemy, player, grid):
        path = a_star(grid, (enemy["x"], enemy["y"]), (player["x"], player["y"]))
        if path:
            enemy["x"], enemy["y"] = path[0]

    def do_attack(self, enemy, player):
        player["hp"] -= 5
```

### 8.4 ビヘイビアツリーの追加

```python
class BTNode:
    def tick(self, context):
        raise NotImplementedError

class Selector(BTNode):
    def __init__(self, children):
        self.children = children

    def tick(self, context):
        for child in self.children:
            result = child.tick(context)
            if result != "FAILURE":
                return result
        return "FAILURE"

class Sequence(BTNode):
    def __init__(self, children):
        self.children = children

    def tick(self, context):
        for child in self.children:
            result = child.tick(context)
            if result != "SUCCESS":
                return result
        return "SUCCESS"

class Condition(BTNode):
    def __init__(self, check_func):
        self.check_func = check_func

    def tick(self, context):
        return "SUCCESS" if self.check_func(context) else "FAILURE"

class Action(BTNode):
    def __init__(self, action_func):
        self.action_func = action_func

    def tick(self, context):
        return self.action_func(context)
```

### 8.5 ビヘイビアツリーの使用例

```python
def create_enemy_bt():
    return Selector([
        # 低HPなら逃げる
        Sequence([
            Condition(lambda ctx: ctx["enemy"]["hp"] < 20),
            Action(lambda ctx: flee(ctx))
        ]),
        # プレイヤーが近ければ攻撃
        Sequence([
            Condition(lambda ctx: distance(ctx["enemy"], ctx["player"]) < 2),
            Action(lambda ctx: attack(ctx))
        ]),
        # プレイヤーが見えれば追跡
        Sequence([
            Condition(lambda ctx: distance(ctx["enemy"], ctx["player"]) < 10),
            Action(lambda ctx: chase(ctx))
        ]),
        # それ以外はパトロール
        Action(lambda ctx: patrol(ctx))
    ])
```

### 8.6 影響マップの追加

```python
def calculate_influence_map(state, width, height):
    """影響マップを計算"""
    influence = [[0.0 for _ in range(width)] for _ in range(height)]

    # プレイヤーの影響（正）
    player = state["player"]
    for y in range(height):
        for x in range(width):
            dist = abs(x - player["x"]) + abs(y - player["y"])
            influence[y][x] += 10.0 / (1 + dist)

    # 敵の影響（負）
    for enemy in state["enemies"]:
        for y in range(height):
            for x in range(width):
                dist = abs(x - enemy["x"]) + abs(y - enemy["y"])
                influence[y][x] -= 5.0 / (1 + dist)

    return influence

def find_safe_position(influence_map, current_pos):
    """最も安全な隣接位置を見つける"""
    x, y = current_pos
    best_pos = current_pos
    best_value = influence_map[y][x]

    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(influence_map[0]) and 0 <= ny < len(influence_map):
            if influence_map[ny][nx] > best_value:
                best_value = influence_map[ny][nx]
                best_pos = (nx, ny)

    return best_pos
```

---

## 第9章：完成形：統合されたゲームエンジン

### 9.1 エンジンの全体構成

```python
class SimpleGameEngine:
    def __init__(self, config):
        self.config = config
        self.input_manager = InputManager()
        self.state = None
        self.running = False
        self.fps = config.get("fps", 60)

    def load_game(self, game_file):
        """ゲーム定義ファイルを読み込む"""
        with open(game_file, 'r') as f:
            content = f.read()

        tokens = tokenize(content)
        game_data = parse(tokens)
        self.interpreter = GameInterpreter(game_data)
        self.state = self.interpreter.state

    def run(self):
        """メインゲームループ"""
        self.running = True
        last_time = time.time()

        while self.running:
            # 時間計測
            current_time = time.time()
            delta_time = current_time - last_time
            last_time = current_time

            # 入力更新
            self.input_manager.update(self.get_raw_input())

            # ゲーム更新
            self.state = self.interpreter.update(
                self.input_manager,
                delta_time
            )

            # 描画
            self.render()

            # フレームレート制御
            frame_time = 1.0 / self.fps
            sleep_time = frame_time - (time.time() - current_time)
            if sleep_time > 0:
                time.sleep(sleep_time)

    def render(self):
        """描画処理"""
        output = render_text_grid(self.state)
        print("\033[2J\033[H" + output)
```

### 9.2 設定ファイル例

```yaml
# game_config.yaml
game:
  title: "Simple Adventure"
  fps: 30
  screen:
    width: 20
    height: 10

player:
  start_position: [1, 1]
  speed: 5
  hp: 100

enemies:
  - type: "chaser"
    position: [15, 5]
    ai: "chase"
  - type: "patroller"
    position: [10, 8]
    ai: "patrol"
    patrol_points: [[8, 8], [12, 8]]

items:
  - type: "coin"
    position: [5, 3]
    value: 10
  - type: "health"
    position: [12, 2]
    heal: 20
```

### 9.3 モジュール構成

```
simple_game_engine/
├── engine/
│   ├── __init__.py
│   ├── core.py          # メインループ
│   ├── input.py         # 入力管理
│   ├── state.py         # 状態管理
│   └── renderer.py      # 描画
├── interpreter/
│   ├── __init__.py
│   ├── lexer.py         # 字句解析
│   ├── parser.py        # 構文解析
│   └── executor.py      # 実行
├── ai/
│   ├── __init__.py
│   ├── fsm.py           # 有限状態機械
│   ├── behavior_tree.py # ビヘイビアツリー
│   ├── pathfinding.py   # 経路探索
│   └── influence_map.py # 影響マップ
├── physics/
│   ├── __init__.py
│   └── collision.py     # 衝突判定
└── games/
    ├── adventure.game   # ゲーム定義ファイル
    └── config.yaml      # 設定ファイル
```

---

## 第10章：演習課題

### 10.1 演習1：ゲームループの実装（Level 1）

- 課題：最小限のゲームループを実装
- 要件：フレームカウントを表示、60FPSで動作
- 学習目標：ゲームループの基本構造を理解

### 10.2 演習2：入力処理の実装（Level 1-2）

- 課題：キーボード入力で文字を移動
- 要件：WASD で上下左右に移動
- 学習目標：入力状態の管理を理解

### 10.3 演習3：衝突判定の実装（Level 2）

- 課題：プレイヤーとアイテムの衝突判定
- 要件：衝突時にスコア加算、アイテム消滅
- 学習目標：AABB衝突判定を理解

### 10.4 演習4：敵AIの実装（Level 2-3）

- 課題：追跡型とパトロール型の敵を実装
- 要件：プレイヤーとの距離に応じて行動変化
- 学習目標：シンプルなAIロジックを理解

### 10.5 演習5：FSMの実装（Level 3）

- 課題：敵AIをFSMで再実装
- 要件：Patrol、Chase、Attack、Flee状態
- 学習目標：状態機械の概念を理解

### 10.6 演習6：A*の実装（Level 3）

- 課題：障害物を避ける経路探索
- 要件：壁を避けてプレイヤーを追跡
- 学習目標：グラフ探索アルゴリズムを理解

### 10.7 演習7：インタプリタの実装（Level 3-4）

- 課題：簡易ゲーム記述言語のインタプリタ
- 要件：エンティティ定義、ルール定義を解釈
- 学習目標：言語処理の基礎を理解

### 10.8 演習8：ビヘイビアツリー（Level 4）

- 課題：BTフレームワークを実装
- 要件：Selector、Sequence、条件、アクション
- 学習目標：木構造による行動制御を理解

### 10.9 演習9：オリジナルゲーム（Level 4）

- 課題：学んだ要素を組み合わせてゲームを作成
- 要件：ゲームループ、入力、AI、衝突判定を含む
- 学習目標：統合的な理解と実装力

### 10.10 演習10：エンジン拡張（Level 5）

- 課題：エンジンに新機能を追加
- 選択肢：サウンド、パーティクル、セーブ/ロード
- 学習目標：拡張性のある設計を理解

---

## 第11章：まとめ

### 11.1 学んだこと

- ゲームは入力・状態・ロジック・出力の組み合わせ
- ゲームループが全ての基盤
- 状態管理が複雑さを制御する鍵
- アルゴリズムは段階的に追加できる

### 11.2 エンジンを使う前に理解すべきこと

- フレームレートと時間管理
- 入力の状態管理
- 衝突判定の基礎
- 状態遷移の概念

### 11.3 次のステップ

- グラフィカルなレンダリング（Pygame、SDL）
- 物理エンジンの基礎
- ネットワーク通信
- 商用エンジン（Unity、Unreal）への移行

### 11.4 最終メッセージ

- エンジンは「魔法の箱」ではない
- 中身を理解していれば、応用が効く
- 基礎を固めてから、便利なツールを使う
- 「なぜ動くか」を常に問い続ける
