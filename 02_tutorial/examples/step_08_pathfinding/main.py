#!/usr/bin/env python3
"""
Step 08: A*経路探索の動作例

グリッドマップ上で最短経路を見つける様子を可視化します。
"""

import sys
from pathlib import Path

# src をインポートパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.state import Position
from src.core.renderer import TextGrid
from src.algorithms.pathfinding import (
    find_path,
    get_next_step,
    create_walkability_checker,
    manhattan_distance,
    euclidean_distance,
)


def visualize_path(
    width: int,
    height: int,
    start: Position,
    goal: Position,
    obstacles: set[tuple[int, int]],
    path: tuple[Position, ...],
) -> str:
    """経路を可視化"""
    grid = TextGrid(width=width, height=height, fill=".")

    # 障害物を描画
    for ox, oy in obstacles:
        grid.set(ox, oy, "#")

    # 経路を描画
    for i, pos in enumerate(path):
        if pos == start:
            grid.set(pos.x, pos.y, "S")
        elif pos == goal:
            grid.set(pos.x, pos.y, "G")
        else:
            grid.set(pos.x, pos.y, "*")

    # 開始と終了が経路になくても描画
    if start not in path:
        grid.set(start.x, start.y, "S")
    if goal not in path:
        grid.set(goal.x, goal.y, "G")

    return grid.render()


def demo_basic() -> None:
    """基本的な経路探索のデモ"""
    print("=== Basic Pathfinding ===")
    print()

    width, height = 15, 10
    start = Position(1, 1)
    goal = Position(13, 8)
    obstacles: set[tuple[int, int]] = set()

    is_walkable = create_walkability_checker(obstacles, width, height)
    result = find_path(start, goal, is_walkable, width, height)

    print(f"Start: ({start.x}, {start.y})")
    print(f"Goal: ({goal.x}, {goal.y})")
    print(f"Found: {result.found}")
    print(f"Path length: {len(result.path)}")
    print(f"Cost: {result.cost:.2f}")
    print(f"Explored nodes: {result.explored_count}")
    print()
    print(visualize_path(width, height, start, goal, obstacles, result.path))
    print()


def demo_obstacles() -> None:
    """障害物回避のデモ"""
    print("=== Obstacle Avoidance ===")
    print()

    width, height = 15, 10
    start = Position(1, 5)
    goal = Position(13, 5)

    # 縦の壁を作成
    obstacles = {(7, y) for y in range(2, 8)}

    is_walkable = create_walkability_checker(obstacles, width, height)
    result = find_path(start, goal, is_walkable, width, height)

    print(f"Start: ({start.x}, {start.y})")
    print(f"Goal: ({goal.x}, {goal.y})")
    print(f"Obstacles: vertical wall at x=7")
    print(f"Found: {result.found}")
    print(f"Path length: {len(result.path)}")
    print(f"Cost: {result.cost:.2f}")
    print()
    print(visualize_path(width, height, start, goal, obstacles, result.path))
    print()


def demo_maze() -> None:
    """迷路探索のデモ"""
    print("=== Maze Solving ===")
    print()

    width, height = 15, 10
    start = Position(1, 1)
    goal = Position(13, 8)

    # 迷路の壁
    obstacles = set()
    # 壁1
    for y in range(0, 7):
        obstacles.add((4, y))
    # 壁2
    for y in range(3, 10):
        obstacles.add((8, y))
    # 壁3
    for y in range(0, 6):
        obstacles.add((11, y))

    is_walkable = create_walkability_checker(obstacles, width, height)
    result = find_path(start, goal, is_walkable, width, height)

    print(f"Start: ({start.x}, {start.y})")
    print(f"Goal: ({goal.x}, {goal.y})")
    print(f"Found: {result.found}")
    print(f"Path length: {len(result.path)}")
    print(f"Cost: {result.cost:.2f}")
    print(f"Explored nodes: {result.explored_count}")
    print()
    print(visualize_path(width, height, start, goal, obstacles, result.path))
    print()


def demo_no_path() -> None:
    """経路なしのデモ"""
    print("=== No Path Available ===")
    print()

    width, height = 10, 10
    start = Position(1, 1)
    goal = Position(8, 8)

    # 目標を完全に囲む
    obstacles = set()
    for x in range(7, 10):
        for y in range(7, 10):
            if (x, y) != (8, 8):
                obstacles.add((x, y))

    is_walkable = create_walkability_checker(obstacles, width, height)
    result = find_path(start, goal, is_walkable, width, height)

    print(f"Start: ({start.x}, {start.y})")
    print(f"Goal: ({goal.x}, {goal.y}) (surrounded by obstacles)")
    print(f"Found: {result.found}")
    print(f"Explored nodes: {result.explored_count}")
    print()
    print(visualize_path(width, height, start, goal, obstacles, result.path))
    print()


def demo_ai_chase() -> None:
    """AI追跡のデモ"""
    print("=== AI Chase Simulation ===")
    print("Enemy (E) chasing Player (P)")
    print()

    width, height = 15, 10
    player_pos = Position(12, 8)
    enemy_pos = Position(2, 2)

    obstacles = {(7, y) for y in range(2, 8)}
    is_walkable = create_walkability_checker(obstacles, width, height)

    # 5ステップシミュレーション
    for step in range(6):
        grid = TextGrid(width=width, height=height, fill=".")

        # 障害物
        for ox, oy in obstacles:
            grid.set(ox, oy, "#")

        # プレイヤーと敵
        grid.set(player_pos.x, player_pos.y, "P")
        grid.set(enemy_pos.x, enemy_pos.y, "E")

        print(f"Step {step}:")
        print(grid.render())

        if enemy_pos == player_pos:
            print("Enemy caught the player!")
            break

        # 敵が次の一歩を計算
        next_pos = get_next_step(
            enemy_pos, player_pos, is_walkable, width, height
        )
        if next_pos:
            enemy_pos = next_pos
        else:
            print("Enemy cannot find a path!")
            break

        print()


def demo_compare_heuristics() -> None:
    """ヒューリスティック比較のデモ"""
    print("=== Heuristic Comparison ===")
    print()

    width, height = 20, 15
    start = Position(1, 1)
    goal = Position(18, 13)
    obstacles: set[tuple[int, int]] = set()

    is_walkable = create_walkability_checker(obstacles, width, height)

    # マンハッタン距離（4方向）
    result_manhattan = find_path(
        start, goal, is_walkable, width, height,
        allow_diagonal=False,
        heuristic=manhattan_distance,
    )

    # ユークリッド距離（8方向）
    result_euclidean = find_path(
        start, goal, is_walkable, width, height,
        allow_diagonal=True,
        heuristic=euclidean_distance,
    )

    print("4-direction (Manhattan):")
    print(f"  Path length: {len(result_manhattan.path)}")
    print(f"  Cost: {result_manhattan.cost:.2f}")
    print(f"  Explored: {result_manhattan.explored_count}")
    print()

    print("8-direction (Euclidean):")
    print(f"  Path length: {len(result_euclidean.path)}")
    print(f"  Cost: {result_euclidean.cost:.2f}")
    print(f"  Explored: {result_euclidean.explored_count}")
    print()


def main() -> None:
    """メインエントリーポイント"""
    print("Step 08: A*経路探索の動作例")
    print()

    print("1. Basic（基本）")
    print("2. Obstacles（障害物回避）")
    print("3. Maze（迷路）")
    print("4. No Path（経路なし）")
    print("5. AI Chase（AI追跡）")
    print("6. Heuristics（ヒューリスティック比較）")
    print()

    choice = input("Select mode (1-6): ").strip()

    if choice == "1":
        demo_basic()
    elif choice == "2":
        demo_obstacles()
    elif choice == "3":
        demo_maze()
    elif choice == "4":
        demo_no_path()
    elif choice == "5":
        demo_ai_chase()
    elif choice == "6":
        demo_compare_heuristics()
    else:
        demo_basic()


if __name__ == "__main__":
    main()
