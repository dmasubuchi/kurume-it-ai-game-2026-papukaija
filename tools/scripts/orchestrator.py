#!/usr/bin/env python3
"""
Orchestrator - PowerPoint自動生成システム
メイン制御スクリプト
"""

import json
import argparse
import yaml
import shutil
from pathlib import Path
from datetime import datetime

from markdown_parser import parse_markdown_file, MarkdownParser
from asset_generator import AssetGenerator
from pptx_renderer import PowerPointRenderer


class Orchestrator:
    """PowerPoint生成オーケストレーター"""

    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.config_dir = self.project_root / "config"
        self.input_dir = self.project_root / "input"
        self.intermediate_dir = self.project_root / "intermediate"
        self.assets_dir = self.project_root / "assets"
        self.output_dir = self.project_root / "powerpoint-output"

        self.theme = {}
        self.processing_log = []

    def load_theme(self, theme_path: str = None):
        """テーマ設定を読み込み"""
        if theme_path:
            theme_file = Path(theme_path)
        else:
            theme_file = self.config_dir / "theme.yaml"

        if theme_file.exists():
            with open(theme_file, "r", encoding="utf-8") as f:
                self.theme = yaml.safe_load(f)
            self.processing_log.append(f"テーマ読み込み: {theme_file}")
        else:
            self.processing_log.append("デフォルトテーマを使用")

    def create_build_directory(self) -> Path:
        """タイムスタンプ付きビルドディレクトリを作成"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        build_dir = self.output_dir / timestamp

        build_dir.mkdir(parents=True, exist_ok=True)

        # サブディレクトリも作成
        (build_dir / "intermediate").mkdir(exist_ok=True)
        (build_dir / "assets" / "diagrams").mkdir(parents=True, exist_ok=True)
        (build_dir / "assets" / "images").mkdir(parents=True, exist_ok=True)

        self.processing_log.append(f"ビルドディレクトリ作成: {build_dir}")
        return build_dir

    def run_from_markdown(
        self,
        input_path: str,
        theme_path: str = None
    ) -> dict:
        """Markdownからフル処理を実行"""
        print("=" * 60)
        print("PowerPoint自動生成システム")
        print("=" * 60)

        # テーマ読み込み
        self.load_theme(theme_path)

        # ビルドディレクトリ作成
        build_dir = self.create_build_directory()

        # Phase 1: Markdown解析
        print("\n[Phase 1] Markdown解析...")
        parsed = parse_markdown_file(input_path)

        # 中間JSON生成
        intermediate_data = {
            "presentation": {
                "metadata": {
                    **parsed["metadata"],
                    "generated_at": datetime.now().isoformat()
                },
                "theme": self.theme,
                "assets": parsed["assets"],
                "slides": parsed["slides"],
                "processing_log": parsed["processing_log"]
            }
        }

        json_path = build_dir / "intermediate" / "presentation.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(intermediate_data, f, ensure_ascii=False, indent=2)

        print(f"  中間JSON出力: {json_path}")
        print(f"  スライド数: {len(parsed['slides'])}")

        # Phase 2: 素材生成
        print("\n[Phase 2] 素材生成...")
        # アセットディレクトリをビルドディレクトリ内に設定
        asset_generator = AssetGenerator(str(build_dir), self.theme)
        asset_result = asset_generator.generate_all(parsed["assets"])

        # JSONを更新
        intermediate_data["presentation"]["assets"] = asset_result["assets"]
        intermediate_data["presentation"]["processing_log"].extend(
            asset_result["processing_log"]
        )

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(intermediate_data, f, ensure_ascii=False, indent=2)

        for log in asset_result["processing_log"]:
            print(f"  {log}")

        # Phase 3: PowerPoint生成
        print("\n[Phase 3] PowerPoint生成...")
        output_config = self.theme.get("output", {})
        filename_prefix = output_config.get("filename_prefix", "presentation")
        filename_suffix = output_config.get("filename_suffix", "")

        if output_config.get("include_timestamp", True):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"{filename_prefix}_{timestamp}{filename_suffix}.pptx"
        else:
            output_filename = f"{filename_prefix}{filename_suffix}.pptx"

        output_path = build_dir / output_filename

        renderer = PowerPointRenderer(self.theme, str(build_dir))
        render_result = renderer.render(
            intermediate_data["presentation"],
            str(output_path)
        )

        # ビルドログを保存
        build_log = {
            "build_time": datetime.now().isoformat(),
            "input_file": str(input_path),
            "theme_file": str(theme_path) if theme_path else None,
            "output_file": str(output_path),
            "slide_count": render_result["slide_count"],
            "processing_log": (
                self.processing_log +
                parsed["processing_log"] +
                asset_result["processing_log"] +
                render_result["processing_log"]
            )
        }

        log_path = build_dir / "build_log.json"
        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(build_log, f, ensure_ascii=False, indent=2)

        # 完了メッセージ
        print("\n" + "=" * 60)
        print("生成完了")
        print("=" * 60)
        print(f"出力ディレクトリ: {build_dir}")
        print(f"PowerPointファイル: {output_path}")
        print(f"中間JSON: {json_path}")
        print(f"ビルドログ: {log_path}")
        print(f"総スライド数: {render_result['slide_count']}")

        # ファイル場所確認処理
        self._verify_output_file(output_path)

        return {
            "build_dir": str(build_dir),
            "output_path": str(output_path),
            "json_path": str(json_path),
            "slide_count": render_result["slide_count"]
        }

    def _verify_output_file(self, output_path: Path):
        """出力ファイルの場所と存在を確認"""
        print("\n" + "-" * 60)
        print("【ファイル場所確認】")
        print("-" * 60)

        # 絶対パスに変換
        abs_path = output_path.resolve()

        if abs_path.exists():
            file_size = abs_path.stat().st_size
            file_size_kb = file_size / 1024
            print(f"  ステータス: OK - ファイルが存在します")
            print(f"  ファイルサイズ: {file_size_kb:.1f} KB")
        else:
            print(f"  ステータス: ERROR - ファイルが見つかりません")

        print(f"\n  【絶対パス】")
        print(f"  {abs_path}")
        print("-" * 60)

    def run_from_json(
        self,
        json_path: str,
        theme_path: str = None
    ) -> dict:
        """既存JSONからPowerPointを生成"""
        print("=" * 60)
        print("PowerPoint生成（JSONから）")
        print("=" * 60)

        # テーマ読み込み
        self.load_theme(theme_path)

        # ビルドディレクトリ作成
        build_dir = self.create_build_directory()

        # JSON読み込み
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # JSONをビルドディレクトリにコピー
        dest_json = build_dir / "intermediate" / "presentation.json"
        shutil.copy(json_path, dest_json)

        # PowerPoint生成
        output_config = self.theme.get("output", {})
        filename_prefix = output_config.get("filename_prefix", "presentation")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"{filename_prefix}_{timestamp}.pptx"
        output_path = build_dir / output_filename

        renderer = PowerPointRenderer(self.theme, str(build_dir))

        # presentationキーがある場合は展開
        if "presentation" in data:
            render_data = data["presentation"]
        else:
            render_data = data

        render_result = renderer.render(render_data, str(output_path))

        print(f"\n出力: {output_path}")
        print(f"スライド数: {render_result['slide_count']}")

        # ファイル場所確認処理
        self._verify_output_file(output_path)

        return {
            "build_dir": str(build_dir),
            "output_path": str(output_path),
            "slide_count": render_result["slide_count"]
        }


def main():
    parser = argparse.ArgumentParser(
        description="PowerPoint自動生成システム",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # Markdownからフル生成
  python orchestrator.py --input input/content.md --theme config/theme.yaml

  # 既存JSONからPowerPoint生成
  python orchestrator.py --json intermediate/presentation.json

  # 出力JSONのみ生成（PowerPoint生成なし）
  python orchestrator.py --input input/content.md --output-json intermediate/presentation.json
        """
    )

    parser.add_argument(
        "--input", "-i",
        help="入力Markdownファイル"
    )
    parser.add_argument(
        "--json", "-j",
        help="既存JSONファイルからPowerPoint生成"
    )
    parser.add_argument(
        "--theme", "-t",
        help="テーマYAMLファイル"
    )
    parser.add_argument(
        "--project", "-p",
        default=".",
        help="プロジェクトルートディレクトリ"
    )
    parser.add_argument(
        "--output-json",
        help="中間JSONのみを出力（PowerPoint生成なし）"
    )

    args = parser.parse_args()

    orchestrator = Orchestrator(args.project)

    if args.input:
        if args.output_json:
            # JSONのみ出力
            orchestrator.load_theme(args.theme)
            parsed = parse_markdown_file(args.input)

            output_data = {
                "presentation": {
                    "metadata": parsed["metadata"],
                    "theme": orchestrator.theme,
                    "assets": parsed["assets"],
                    "slides": parsed["slides"],
                    "processing_log": parsed["processing_log"]
                }
            }

            with open(args.output_json, "w", encoding="utf-8") as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)

            print(f"JSON出力完了: {args.output_json}")
        else:
            # フル処理
            orchestrator.run_from_markdown(args.input, args.theme)

    elif args.json:
        orchestrator.run_from_json(args.json, args.theme)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
