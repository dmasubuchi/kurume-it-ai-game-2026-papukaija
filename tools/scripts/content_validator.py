#!/usr/bin/env python3
"""
コンテンツ検証スクリプト

スライドの情報密度をチェックし、薄いページを特定する。
"""

import json
import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Any, Optional


@dataclass
class SlideMetrics:
    """スライドの情報量メトリクス"""
    slide_number: int
    title: str
    bullet_count: int
    sub_bullet_count: int
    has_diagram: bool
    has_table: bool
    has_code: bool
    text_length: int
    density_score: float
    status: str
    warnings: List[str]


class ContentValidator:
    """コンテンツ検証クラス"""

    # スコアリング設定
    WEIGHTS = {
        'bullet': 1.0,          # 箇条書き1つあたり
        'sub_bullet': 0.5,      # サブ箇条書き1つあたり
        'diagram': 3.0,         # 図表あり
        'table': 3.0,           # 表あり
        'code': 2.0,            # コードブロックあり
        'text_per_100': 0.2,    # テキスト100文字あたり
    }

    # 閾値設定
    THRESHOLDS = {
        'minimum_score': 2.0,   # 最低スコア
        'warning_score': 3.0,   # 警告スコア
        'good_score': 5.0,      # 良好スコア
        'title_slide': 0.0,     # タイトルスライドの最低スコア（0でOK）
    }

    # 除外パターン（タイトルスライド等）
    TITLE_PATTERNS = [
        'タイトル', 'title', '章扉', '目次', 'まとめ', 'ワーク',
        '導入', '第1章', '第2章', '第3章', '第4章', '第5章', '第6章', '第7章', '第8章',
        'vs', 'VS'
    ]

    def __init__(self, project_root: Path):
        self.project_root = project_root

    def load_presentation_json(self, json_path: Path) -> Optional[Dict[str, Any]]:
        """presentation.jsonを読み込む"""
        if not json_path.exists():
            print(f"エラー: {json_path} が見つかりません")
            return None

        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def is_title_slide(self, slide: Dict[str, Any]) -> bool:
        """タイトルスライドかどうかを判定"""
        # タイトルの抽出（複数のフォーマットに対応）
        title = slide.get('title', '')
        if not title:
            # elementsからタイトルを探す
            for elem in slide.get('elements', []):
                if elem.get('type') == 'title':
                    title = elem.get('content', '')
                    break

        title = title.lower()
        slide_type = slide.get('type', '').lower()
        layout = slide.get('layout', '').lower()

        # レイアウトが title または section の場合
        if layout in ['title', 'section']:
            return True

        if slide_type == 'title':
            return True

        for pattern in self.TITLE_PATTERNS:
            if pattern.lower() in title:
                return True

        return False

    def count_bullets(self, content_list: List[Any]) -> tuple:
        """箇条書きの数をカウント"""
        bullet_count = 0
        sub_bullet_count = 0

        def count_recursive(items, level=0):
            nonlocal bullet_count, sub_bullet_count
            if not items:
                return
            for item in items:
                if isinstance(item, dict):
                    if level == 0:
                        bullet_count += 1
                    else:
                        sub_bullet_count += 1
                    # 子要素をカウント
                    children = item.get('children', [])
                    if children:
                        count_recursive(children, level + 1)
                elif isinstance(item, str):
                    if level == 0:
                        bullet_count += 1
                    else:
                        sub_bullet_count += 1

        count_recursive(content_list)
        return bullet_count, sub_bullet_count

    def calculate_text_length(self, slide: Dict[str, Any]) -> int:
        """テキストの総文字数を計算"""
        total = 0

        def extract_text(obj):
            nonlocal total
            if isinstance(obj, str):
                total += len(obj)
            elif isinstance(obj, dict):
                for value in obj.values():
                    extract_text(value)
            elif isinstance(obj, list):
                for item in obj:
                    extract_text(item)

        extract_text(slide)
        return total

    def analyze_slide(self, slide: Dict[str, Any], slide_number: int) -> SlideMetrics:
        """単一スライドを分析"""
        # タイトルの抽出（複数のフォーマットに対応）
        title = slide.get('title', '')
        if not title:
            # elementsからタイトルを探す
            for elem in slide.get('elements', []):
                if elem.get('type') == 'title':
                    title = elem.get('content', '')
                    break
        if not title:
            title = f'スライド {slide_number}'

        # コンテンツの抽出
        content = slide.get('content', [])
        if not content and 'elements' in slide:
            # elementsフォーマットからbullet_listを抽出
            for elem in slide.get('elements', []):
                if elem.get('type') == 'bullet_list':
                    content = elem.get('content', [])
                    break

        # 箇条書きカウント
        bullet_count, sub_bullet_count = self.count_bullets(content)

        # 図表・表・コードの有無
        has_diagram = slide.get('diagram') is not None or slide.get('image') is not None
        has_table = slide.get('table') is not None
        has_code = slide.get('code') is not None

        # elementsから図表等をチェック
        for elem in slide.get('elements', []):
            elem_type = elem.get('type', '')
            if elem_type in ['image', 'diagram', 'mermaid']:
                has_diagram = True
            elif elem_type == 'table':
                has_table = True
            elif elem_type == 'code':
                has_code = True

        # Mermaid図もチェック
        content_str = json.dumps(slide, ensure_ascii=False)
        if 'mermaid' in content_str.lower() or 'diagram_' in content_str.lower():
            has_diagram = True

        # テキスト長
        text_length = self.calculate_text_length(slide)

        # スコア計算
        score = (
            bullet_count * self.WEIGHTS['bullet'] +
            sub_bullet_count * self.WEIGHTS['sub_bullet'] +
            (self.WEIGHTS['diagram'] if has_diagram else 0) +
            (self.WEIGHTS['table'] if has_table else 0) +
            (self.WEIGHTS['code'] if has_code else 0) +
            (text_length / 100) * self.WEIGHTS['text_per_100']
        )

        # 状態判定
        warnings = []
        is_title = self.is_title_slide(slide)
        threshold = self.THRESHOLDS['title_slide'] if is_title else self.THRESHOLDS['minimum_score']

        if score < threshold:
            status = "ERROR"
            warnings.append(f"情報量不足: スコア {score:.1f} < 閾値 {threshold}")
        elif score < self.THRESHOLDS['warning_score'] and not is_title:
            status = "WARNING"
            warnings.append(f"情報量が少なめ: スコア {score:.1f}")
        else:
            status = "OK"

        # 具体的な改善提案
        if bullet_count < 3 and not is_title:
            warnings.append("箇条書きを3つ以上追加することを推奨")
        if not has_diagram and not has_table and not is_title:
            warnings.append("図表または表の追加を検討")

        return SlideMetrics(
            slide_number=slide_number,
            title=title,
            bullet_count=bullet_count,
            sub_bullet_count=sub_bullet_count,
            has_diagram=has_diagram,
            has_table=has_table,
            has_code=has_code,
            text_length=text_length,
            density_score=score,
            status=status,
            warnings=warnings
        )

    def validate_presentation(self, json_path: Path) -> List[SlideMetrics]:
        """プレゼンテーション全体を検証"""
        data = self.load_presentation_json(json_path)
        if not data:
            return []

        # スライドの場所を探す（複数のフォーマットに対応）
        slides = data.get('slides', [])
        if not slides and 'presentation' in data:
            slides = data['presentation'].get('slides', [])
        results = []

        for i, slide in enumerate(slides, 1):
            metrics = self.analyze_slide(slide, i)
            results.append(metrics)

        return results

    def generate_report(self, results: List[SlideMetrics]) -> str:
        """検証レポートを生成"""
        lines = []
        lines.append("=" * 70)
        lines.append("スライド情報密度検証レポート")
        lines.append("=" * 70)
        lines.append("")

        # サマリー
        total = len(results)
        if total == 0:
            lines.append("スライドが見つかりませんでした。")
            return "\n".join(lines)

        errors = sum(1 for r in results if r.status == "ERROR")
        warnings = sum(1 for r in results if r.status == "WARNING")
        ok = sum(1 for r in results if r.status == "OK")

        lines.append(f"総スライド数: {total}")
        lines.append(f"  OK:      {ok} ({ok/total*100:.1f}%)")
        lines.append(f"  WARNING: {warnings} ({warnings/total*100:.1f}%)")
        lines.append(f"  ERROR:   {errors} ({errors/total*100:.1f}%)")
        lines.append("")

        # 問題のあるスライドの詳細
        if errors > 0 or warnings > 0:
            lines.append("-" * 70)
            lines.append("問題のあるスライド:")
            lines.append("-" * 70)

            for r in results:
                if r.status != "OK":
                    lines.append(f"\n[{r.status}] p.{r.slide_number}: {r.title}")
                    lines.append(f"  スコア: {r.density_score:.1f}")
                    lines.append(f"  箇条書き: {r.bullet_count} (サブ: {r.sub_bullet_count})")
                    lines.append(f"  図表: {'あり' if r.has_diagram else 'なし'}")
                    lines.append(f"  表: {'あり' if r.has_table else 'なし'}")
                    for warning in r.warnings:
                        lines.append(f"  → {warning}")

        # 全スライドの詳細
        lines.append("")
        lines.append("-" * 70)
        lines.append("全スライド詳細:")
        lines.append("-" * 70)
        lines.append(f"{'No':>3} | {'Status':<8} | {'Score':>5} | {'Bullet':>6} | {'Diag':>4} | {'Table':>5} | Title")
        lines.append("-" * 70)

        for r in results:
            diag = "Y" if r.has_diagram else "-"
            table = "Y" if r.has_table else "-"
            lines.append(
                f"{r.slide_number:>3} | {r.status:<8} | {r.density_score:>5.1f} | "
                f"{r.bullet_count:>6} | {diag:>4} | {table:>5} | {r.title[:30]}"
            )

        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def validate_and_report(self, json_path: Path) -> tuple:
        """検証を実行しレポートを生成"""
        results = self.validate_presentation(json_path)
        report = self.generate_report(results)
        return results, report


def main():
    parser = argparse.ArgumentParser(description='スライドコンテンツ検証スクリプト')
    parser.add_argument('--project', type=str, default='..',
                        help='プロジェクトルートディレクトリ')
    parser.add_argument('--json', type=str, required=True,
                        help='presentation.jsonのパス')
    parser.add_argument('--output', type=str, default=None,
                        help='レポート出力ファイル（省略時は標準出力）')

    args = parser.parse_args()

    project_root = Path(args.project).resolve()
    json_path = Path(args.json)
    if not json_path.is_absolute():
        json_path = project_root / args.json

    validator = ContentValidator(project_root)
    results, report = validator.validate_and_report(json_path)

    if args.output:
        output_path = Path(args.output)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"レポートを保存しました: {output_path}")
    else:
        print(report)

    # エラーがある場合は非ゼロで終了
    errors = sum(1 for r in results if r.status == "ERROR")
    if errors > 0:
        return 1
    return 0


if __name__ == "__main__":
    exit(main())
