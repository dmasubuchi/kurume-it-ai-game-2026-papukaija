"""
README表示機能

README_1PAGE.md を読み込んで表示する。
"""

from pathlib import Path


def read_readme(base_path: Path | None = None) -> str:
    """
    README_1PAGE.md を読み込む

    Args:
        base_path: 02_tutorial/ のパス

    Returns:
        READMEの内容（見つからない場合はデフォルトメッセージ）
    """
    if base_path is None:
        base_path = Path(__file__).parent.parent.parent

    readme_path = base_path / "README_1PAGE.md"

    if not readme_path.exists():
        return """
# チュートリアルへようこそ

README_1PAGE.md が見つかりませんでした。

このチュートリアルでは、ターン制ゲームの実装を学びます。
Steps 00〜06 を順番に進めてください。
"""

    return readme_path.read_text(encoding="utf-8")


def display_readme(base_path: Path | None = None) -> None:
    """READMEを表示"""
    content = read_readme(base_path)
    print()
    print("=" * 60)
    print(content)
    print("=" * 60)
    print()
    input("Press Enter to continue...")
