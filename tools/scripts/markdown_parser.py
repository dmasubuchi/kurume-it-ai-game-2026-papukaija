#!/usr/bin/env python3
"""
Markdown Parser
Markdownファイルを解析してプレゼンテーション構造を抽出
"""

import re
import json
from pathlib import Path
from typing import Optional


class MarkdownParser:
    """Markdownを解析してスライド構造に変換"""

    def __init__(self):
        self.slides = []
        self.assets = {"diagrams": [], "images": []}
        self.metadata = {}
        self.processing_log = []
        self.diagram_counter = 0
        self.image_counter = 0

    def parse(self, markdown_text: str) -> dict:
        """Markdownテキストを解析"""
        lines = markdown_text.split("\n")
        current_slide = None
        current_elements = []
        in_mermaid = False
        mermaid_content = []
        in_code_block = False
        bullet_items = []

        for i, line in enumerate(lines):
            # メタデータコメント
            if line.strip().startswith("<!-- metadata:"):
                self._parse_metadata(line)
                continue

            # 画像生成指示
            if line.strip().startswith("<!-- generate:"):
                asset = self._parse_generate_directive(line)
                if asset:
                    self.assets["images"].append(asset)
                    current_elements.append({
                        "type": "image",
                        "asset_ref": asset["id"]
                    })
                continue

            # Mermaidコードブロック開始
            if line.strip().startswith("```mermaid"):
                in_mermaid = True
                mermaid_content = []
                continue

            # コードブロック終了
            if in_mermaid and line.strip() == "```":
                in_mermaid = False
                asset = self._create_mermaid_asset("\n".join(mermaid_content))
                self.assets["diagrams"].append(asset)
                current_elements.append({
                    "type": "diagram",
                    "asset_ref": asset["id"]
                })
                continue

            # Mermaid内容収集
            if in_mermaid:
                mermaid_content.append(line)
                continue

            # 通常のコードブロック
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                continue

            if in_code_block:
                continue

            # h1: タイトルスライドまたはセクション
            if line.startswith("# ") and not line.startswith("##"):
                # 前のスライドを保存
                if current_slide:
                    self._finalize_bullet_list(current_elements, bullet_items)
                    bullet_items = []
                    current_slide["elements"] = current_elements
                    self.slides.append(current_slide)

                title = line[2:].strip()
                if not self.slides:  # 最初のh1はタイトルスライド
                    current_slide = {
                        "layout": "title",
                        "elements": [{"type": "title", "content": title}]
                    }
                    self.metadata["title"] = title
                    self.processing_log.append(f"h1をタイトルスライドとして処理: {title}")
                else:  # 以降のh1はセクション
                    current_slide = {
                        "layout": "section",
                        "elements": [{"type": "title", "content": title}]
                    }
                    self.processing_log.append(f"h1をセクション区切りとして処理: {title}")
                current_elements = current_slide["elements"]
                continue

            # h2: 新規スライド
            if line.startswith("## "):
                # 前のスライドを保存
                if current_slide:
                    self._finalize_bullet_list(current_elements, bullet_items)
                    bullet_items = []
                    current_slide["elements"] = current_elements
                    self.slides.append(current_slide)

                title = line[3:].strip()
                current_slide = {
                    "layout": "content",
                    "elements": [{"type": "title", "content": title}]
                }
                current_elements = current_slide["elements"]
                self.processing_log.append(f"h2で新規スライド: {title}")
                continue

            # h3: 新規スライド（小見出しとして）
            if line.startswith("### "):
                # 前のスライドを保存
                if current_slide:
                    self._finalize_bullet_list(current_elements, bullet_items)
                    bullet_items = []
                    current_slide["elements"] = current_elements
                    self.slides.append(current_slide)

                title = line[4:].strip()
                current_slide = {
                    "layout": "content",
                    "elements": [{"type": "title", "content": title}]
                }
                current_elements = current_slide["elements"]
                self.processing_log.append(f"h3で新規スライド: {title}")
                continue

            # h4: 新規スライド（さらに下位の見出し）
            if line.startswith("#### "):
                # 前のスライドを保存
                if current_slide:
                    self._finalize_bullet_list(current_elements, bullet_items)
                    bullet_items = []
                    current_slide["elements"] = current_elements
                    self.slides.append(current_slide)

                title = line[5:].strip()
                current_slide = {
                    "layout": "content",
                    "elements": [{"type": "title", "content": title}]
                }
                current_elements = current_slide["elements"]
                self.processing_log.append(f"h4で新規スライド: {title}")
                continue

            # 箇条書き
            if line.strip().startswith("- ") or line.strip().startswith("* "):
                item = line.strip()[2:].strip()
                bullet_items.append(item)
                continue

            # 番号付きリスト
            if re.match(r"^\d+\.\s", line.strip()):
                item = re.sub(r"^\d+\.\s", "", line.strip())
                bullet_items.append(item)
                continue

            # 画像参照
            img_match = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", line.strip())
            if img_match:
                self._finalize_bullet_list(current_elements, bullet_items)
                bullet_items = []
                alt_text, path = img_match.groups()
                asset = self._create_file_image_asset(path, alt_text)
                self.assets["images"].append(asset)
                current_elements.append({
                    "type": "image",
                    "asset_ref": asset["id"]
                })
                continue

            # テーブル
            if line.strip().startswith("|") and "|" in line[1:]:
                # テーブル処理（簡易版）
                self._finalize_bullet_list(current_elements, bullet_items)
                bullet_items = []
                # TODO: テーブル解析の実装
                continue

            # 水平線（スキップ）
            if line.strip() == "---" or line.strip() == "***" or line.strip() == "___":
                continue

            # 通常のテキスト段落
            if line.strip() and current_slide:
                self._finalize_bullet_list(current_elements, bullet_items)
                bullet_items = []
                # Markdownの太字記法を除去
                text_content = self._strip_markdown_formatting(line.strip())
                if text_content:  # 空でない場合のみ追加
                    current_elements.append({
                        "type": "text",
                        "content": text_content
                    })

        # 最後のスライドを保存
        if current_slide:
            self._finalize_bullet_list(current_elements, bullet_items)
            current_slide["elements"] = current_elements
            self.slides.append(current_slide)

        return {
            "metadata": self.metadata,
            "assets": self.assets,
            "slides": self.slides,
            "processing_log": self.processing_log
        }

    def _parse_metadata(self, line: str):
        """メタデータコメントを解析"""
        match = re.search(r"<!-- metadata:\s*(.+?)\s*-->", line)
        if match:
            pairs = match.group(1).split(",")
            for pair in pairs:
                if "=" in pair:
                    key, value = pair.split("=", 1)
                    self.metadata[key.strip()] = value.strip()

    def _parse_generate_directive(self, line: str) -> Optional[dict]:
        """画像生成指示を解析"""
        match = re.search(r"<!-- generate:\s*(.+?)\s*-->", line)
        if match:
            self.image_counter += 1
            prompt = match.group(1)
            return {
                "id": f"image_{self.image_counter:03d}",
                "type": "generated",
                "prompt": prompt,
                "negative_prompt": "",
                "output_path": f"assets/images/image_{self.image_counter:03d}.png",
                "status": "pending"
            }
        return None

    def _create_mermaid_asset(self, content: str) -> dict:
        """Mermaidアセットを作成"""
        self.diagram_counter += 1
        return {
            "id": f"diagram_{self.diagram_counter:03d}",
            "type": "mermaid",
            "source": content,
            "output_path": f"assets/diagrams/diagram_{self.diagram_counter:03d}.png",
            "status": "pending"
        }

    def _create_file_image_asset(self, path: str, alt_text: str) -> dict:
        """ファイル画像アセットを作成"""
        self.image_counter += 1
        return {
            "id": f"image_{self.image_counter:03d}",
            "type": "file",
            "source_path": path,
            "alt_text": alt_text,
            "output_path": path,
            "status": "pending"
        }

    def _finalize_bullet_list(self, elements: list, items: list):
        """箇条書きリストを要素に追加"""
        if items:
            # 箇条書きの各項目からMarkdown記法を除去
            cleaned_items = [self._strip_markdown_formatting(item) for item in items]
            elements.append({
                "type": "bullet_list",
                "content": cleaned_items
            })

    def _strip_markdown_formatting(self, text: str) -> str:
        """Markdown記法をプレーンテキストに変換"""
        if not text:
            return text

        # 太字: **text** または __text__ → text
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
        text = re.sub(r'__([^_]+)__', r'\1', text)

        # 斜体: *text* または _text_ → text
        text = re.sub(r'\*([^*]+)\*', r'\1', text)
        text = re.sub(r'_([^_]+)_', r'\1', text)

        # 取り消し線: ~~text~~ → text
        text = re.sub(r'~~([^~]+)~~', r'\1', text)

        # インラインコード: `code` → code
        text = re.sub(r'`([^`]+)`', r'\1', text)

        # リンク: [text](url) → text
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)

        # 矢印などの装飾的なテキストをそのまま残す
        # → や ← は意味があるので除去しない

        return text.strip()


def parse_markdown_file(input_path: str) -> dict:
    """Markdownファイルを解析"""
    path = Path(input_path)
    if not path.exists():
        raise FileNotFoundError(f"入力ファイルが見つかりません: {input_path}")

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    parser = MarkdownParser()
    return parser.parse(content)


if __name__ == "__main__":
    import argparse

    arg_parser = argparse.ArgumentParser(description="Markdown Parser")
    arg_parser.add_argument("--input", "-i", required=True, help="入力Markdownファイル")
    arg_parser.add_argument("--output", "-o", help="出力JSONファイル（省略時は標準出力）")

    args = arg_parser.parse_args()

    result = parse_markdown_file(args.input)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"出力完了: {args.output}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
