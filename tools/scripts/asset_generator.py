#!/usr/bin/env python3
"""
Asset Generator
Mermaid図とAI画像の生成を担当
"""

import json
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Optional
from PIL import Image, ImageDraw, ImageFont


class AssetGenerator:
    """素材生成クラス"""

    def __init__(self, project_root: str, theme: dict):
        self.project_root = Path(project_root)
        self.theme = theme
        self.mermaid_available = self._check_mermaid()
        self.processing_log = []

    def _check_mermaid(self) -> bool:
        """Mermaid CLIの存在確認"""
        try:
            result = subprocess.run(
                ["which", "mmdc"],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except Exception:
            return False

    def generate_all(self, assets: dict) -> dict:
        """全素材を生成"""
        # 出力ディレクトリ確保
        diagrams_dir = self.project_root / "assets" / "diagrams"
        images_dir = self.project_root / "assets" / "images"
        diagrams_dir.mkdir(parents=True, exist_ok=True)
        images_dir.mkdir(parents=True, exist_ok=True)

        # Mermaid図生成
        for diagram in assets.get("diagrams", []):
            self._generate_mermaid(diagram)

        # 画像処理
        for image in assets.get("images", []):
            if image["type"] == "generated":
                self._generate_image(image)
            elif image["type"] == "file":
                self._verify_image(image)

        return {
            "assets": assets,
            "processing_log": self.processing_log
        }

    def _generate_mermaid(self, diagram: dict):
        """Mermaid図を生成"""
        if not self.mermaid_available:
            self.processing_log.append(f"Mermaid CLI未検出、スキップ: {diagram['id']}")
            diagram["status"] = "skipped"
            self._create_placeholder_image(
                self.project_root / diagram["output_path"],
                "[Mermaid図]",
                800, 600
            )
            return

        try:
            # 一時ファイルにMermaidソースを書き込み
            with tempfile.NamedTemporaryFile(
                mode="w",
                suffix=".mmd",
                delete=False,
                encoding="utf-8"
            ) as f:
                f.write(diagram["source"])
                temp_input = f.name

            output_path = self.project_root / diagram["output_path"]
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Mermaid CLI設定
            mermaid_config = self.theme.get("mermaid", {})
            mermaid_theme = mermaid_config.get("theme", "default")
            mermaid_bg = mermaid_config.get("background", "white")
            mermaid_scale = mermaid_config.get("scale", 2)

            # mmdc実行
            cmd = [
                "mmdc",
                "-i", temp_input,
                "-o", str(output_path),
                "-t", mermaid_theme,
                "-b", mermaid_bg,
                "-s", str(mermaid_scale)
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0 and output_path.exists():
                diagram["status"] = "generated"
                self.processing_log.append(f"Mermaid図生成成功: {diagram['id']}")
            else:
                raise Exception(result.stderr)

        except Exception as e:
            self.processing_log.append(f"Mermaid図生成失敗: {diagram['id']} - {str(e)}")
            diagram["status"] = "failed"
            self._create_placeholder_image(
                self.project_root / diagram["output_path"],
                "[Mermaid図生成エラー]",
                800, 600
            )
        finally:
            # 一時ファイル削除
            try:
                Path(temp_input).unlink()
            except Exception:
                pass

    def _generate_image(self, image: dict):
        """AI画像を生成（プレースホルダーで代替）"""
        # 現時点ではプレースホルダーを生成
        # 将来的にはOllama/Stable Diffusion連携を実装
        output_path = self.project_root / image["output_path"]
        output_path.parent.mkdir(parents=True, exist_ok=True)

        img_config = self.theme.get("image_generation", {})
        width = img_config.get("default_width", 1024)
        height = img_config.get("default_height", 768)

        self._create_placeholder_image(
            output_path,
            f"[AI生成画像]\n{image.get('prompt', '')[:50]}...",
            width, height
        )

        image["status"] = "placeholder"
        self.processing_log.append(
            f"画像プレースホルダー生成: {image['id']} (AI生成未実装)"
        )

    def _verify_image(self, image: dict):
        """既存画像ファイルを検証"""
        source_path = self.project_root / image["source_path"]

        if source_path.exists():
            image["status"] = "verified"
            self.processing_log.append(f"画像ファイル確認: {image['id']}")
        else:
            image["status"] = "missing"
            self.processing_log.append(f"画像ファイル未検出: {image['id']} - {source_path}")

            # プレースホルダー生成
            output_path = self.project_root / image["output_path"]
            self._create_placeholder_image(
                output_path,
                f"[画像未検出]\n{image.get('alt_text', '')}",
                800, 600
            )

    def _create_placeholder_image(
        self,
        output_path: Path,
        text: str,
        width: int,
        height: int
    ):
        """プレースホルダー画像を生成"""
        output_path.parent.mkdir(parents=True, exist_ok=True)

        img_config = self.theme.get("image_generation", {})
        bg_color = img_config.get("placeholder_color", "#EEEEEE")

        # PIL画像生成
        img = Image.new("RGB", (width, height), bg_color)
        draw = ImageDraw.Draw(img)

        # テキスト描画（システムフォント使用）
        try:
            # macOS/Linux用フォント検索
            font_paths = [
                "/System/Library/Fonts/Helvetica.ttc",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "/usr/share/fonts/TTF/DejaVuSans.ttf"
            ]
            font = None
            for fp in font_paths:
                if Path(fp).exists():
                    font = ImageFont.truetype(fp, 24)
                    break
            if not font:
                font = ImageFont.load_default()
        except Exception:
            font = ImageFont.load_default()

        # テキスト中央配置
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        x = (width - text_width) // 2
        y = (height - text_height) // 2

        draw.text((x, y), text, fill="#666666", font=font)

        # 枠線
        draw.rectangle(
            [(10, 10), (width - 10, height - 10)],
            outline="#CCCCCC",
            width=2
        )

        img.save(output_path, "PNG")


def generate_assets(json_path: str, project_root: str, theme: dict) -> dict:
    """JSONから素材を生成"""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    generator = AssetGenerator(project_root, theme)
    result = generator.generate_all(data.get("assets", {}))

    # JSONを更新
    data["assets"] = result["assets"]
    if "processing_log" not in data:
        data["processing_log"] = []
    data["processing_log"].extend(result["processing_log"])

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return result


if __name__ == "__main__":
    import argparse
    import yaml

    parser = argparse.ArgumentParser(description="Asset Generator")
    parser.add_argument("--json", "-j", required=True, help="中間JSONファイル")
    parser.add_argument("--project", "-p", default=".", help="プロジェクトルート")
    parser.add_argument("--theme", "-t", help="テーマYAMLファイル")

    args = parser.parse_args()

    theme = {}
    if args.theme and Path(args.theme).exists():
        with open(args.theme, "r", encoding="utf-8") as f:
            theme = yaml.safe_load(f)

    result = generate_assets(args.json, args.project, theme)

    print("素材生成完了")
    for log in result["processing_log"]:
        print(f"  - {log}")
