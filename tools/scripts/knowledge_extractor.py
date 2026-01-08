#!/usr/bin/env python3
"""
ナレッジ抽出スクリプト

共有ナレッジファイルから章ごとに関連セクションを抽出し、
中間レポートを生成する。
"""

import re
import argparse
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass, field


@dataclass
class ChapterConfig:
    """章ごとの抽出設定"""
    title: str
    page_range: str
    keywords: List[str]
    section_patterns: List[str]
    sources: List[str]
    description: str


# 章ごとの抽出設定
CHAPTER_CONFIGS: Dict[str, ChapterConfig] = {
    "chapter01_introduction": ChapterConfig(
        title="導入・問題提起",
        page_range="p.1-10",
        keywords=[
            "増幅器", "Vibe Coding", "バイブコーディング", "3層モデル",
            "2025→2026", "2026の変化", "生成AI", "LLM", "ChatGPT",
            "能力の錯覚", "Illusion of Competence", "ゴール", "ロードマップ"
        ],
        section_patterns=[
            r"## 1\) まず前提",
            r"### 1\.1 生成AI",
            r"### 1\.2 ゲーム開発",
            r"バイブコーディングの台頭",
            r"序論",
            r"AI時代.*スキル",
        ],
        sources=["スライド戦略.md", "AI授業ネタ.md", "全体のタイトル案.md"],
        description="講義の導入。Vibe Codingの台頭、AIは増幅器、3層モデルの先出し"
    ),

    "chapter02_game_and_ai": ChapterConfig(
        title="ゲームとAIの関係",
        page_range="p.11-20",
        keywords=[
            "GPU", "リアルタイム", "レンダリング", "状態管理", "State Management",
            "幻覚", "ハルシネーション", "Unity", "Unreal", "物理エンジン",
            "リアルタイム制約", "LLMの限界", "ゲーム開発", "空間論理"
        ],
        section_patterns=[
            r"ゲーム開発における特異点",
            r"状態管理",
            r"空間論理",
            r"リアルタイム",
            r"GPU",
            r"LLM.*ゲーム",
        ],
        sources=["AI授業ネタ.md", "自動化、LLM、AIを用いた、実験的なGameデザイン.md"],
        description="GPUの役割、リアルタイム制約、なぜLLMがゲーム実行時に難しいか"
    ),

    "chapter03_game_ai_basics": ChapterConfig(
        title="ゲームAIの基礎",
        page_range="p.21-40",
        keywords=[
            "FSM", "有限ステートマシン", "ビヘイビアツリー", "BT",
            "GOAP", "ゴール指向", "HTN", "階層型タスク", "強化学習", "RL",
            "ナビゲーション", "パスファインディング", "A*", "意思決定"
        ],
        section_patterns=[
            r"ゲームAIの進化",
            r"FSM",
            r"ビヘイビアツリー",
            r"GOAP",
            r"HTN",
            r"強化学習",
            r"意思決定",
        ],
        sources=["AI授業ネタ.md", "全体のタイトル案.md"],
        description="ゲームAI技術の解説：FSM、BT、GOAP、HTN、強化学習"
    ),

    "chapter04_case_studies": ChapterConfig(
        title="事例研究",
        page_range="p.41-52",
        keywords=[
            "Halo 2", "F.E.A.R.", "Left 4 Dead", "AI Director", "Suphx",
            "麻雀", "AlphaGo", "AlphaStar", "OpenAI Five", "Dota",
            "ゲームAI事例", "実装", "ケーススタディ"
        ],
        section_patterns=[
            r"Halo",
            r"F\.E\.A\.R",
            r"Left 4 Dead",
            r"AI Director",
            r"Suphx",
            r"AlphaGo",
            r"ケーススタディ",
        ],
        sources=["AI授業ネタ.md", "世の中のAIとGameの組み合わせ.md"],
        description="具体的なゲームAI実装事例の深掘り"
    ),

    "chapter05_generative_ai": ChapterConfig(
        title="生成AIの限界と可能性",
        page_range="p.53-72",
        keywords=[
            "生成的負債", "Generative Debt", "能力の錯覚", "Illusion of Competence",
            "認知科学", "Comprehension-Performance Gap", "理解", "パフォーマンス",
            "プロンプト", "出力の質", "検証", "デバッグ"
        ],
        section_patterns=[
            r"能力の錯覚",
            r"生成的負債",
            r"認知科学",
            r"Comprehension.*Performance",
            r"プロンプト",
            r"検証",
        ],
        sources=["AI授業ネタ.md", "スライド戦略.md"],
        description="生成AIの落とし穴、能力の錯覚、生成的負債の3分類"
    ),

    "chapter06_human_ai": ChapterConfig(
        title="人間×AI協働",
        page_range="p.73-88",
        keywords=[
            "因数分解", "明確化", "判断", "3層モデル", "Human×AI",
            "タスク分解", "要件定義", "意思決定", "ワーク", "演習"
        ],
        section_patterns=[
            r"因数分解",
            r"明確化",
            r"判断",
            r"Human.*AI",
            r"3層モデル",
            r"ワーク",
            r"12枚スライド",
        ],
        sources=["スライド戦略.md", "AI授業ネタ.md"],
        description="3層モデルの詳細：因数分解・明確化・判断の実践"
    ),

    "chapter07_production": ChapterConfig(
        title="AIと制作工程",
        page_range="p.89-104",
        keywords=[
            "技術的負債", "セキュリティ", "QA", "テスト", "自動化",
            "UniGen", "IGE", "GameGPT", "ワークフロー", "工程", "産業構造"
        ],
        section_patterns=[
            r"技術的負債",
            r"セキュリティ",
            r"QA",
            r"UniGen",
            r"IGE",
            r"GameGPT",
            r"工程",
            r"産業",
        ],
        sources=["AI授業ネタ.md", "自動化、LLM、AIを用いた、実験的なGameデザイン.md"],
        description="AI導入による制作工程の変化、QA、産業構造への影響"
    ),

    "chapter08_learning": ChapterConfig(
        title="学び方と進路",
        page_range="p.105-120",
        keywords=[
            "サンドイッチ方式", "学習戦略", "苦闘", "基礎", "進路",
            "キャリア", "スキル", "熟練者", "初学者", "学び方"
        ],
        section_patterns=[
            r"サンドイッチ",
            r"学習戦略",
            r"苦闘",
            r"基礎",
            r"進路",
            r"キャリア",
            r"学び方",
        ],
        sources=["AI授業ネタ.md", "スライド戦略.md"],
        description="AI時代の学習戦略、サンドイッチ方式、進路指導"
    ),
}


class KnowledgeExtractor:
    """ナレッジ抽出クラス"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.knowledge_dir = project_root
        self.output_dir = project_root / "intermediate-reports"

    def load_knowledge_file(self, filename: str) -> str:
        """ナレッジファイルを読み込む"""
        filepath = self.knowledge_dir / filename
        if not filepath.exists():
            print(f"  警告: {filename} が見つかりません")
            return ""
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()

    def extract_by_keywords(self, content: str, keywords: List[str], context_lines: int = 5) -> List[Dict[str, Any]]:
        """キーワードを含む段落を抽出"""
        results = []
        lines = content.split('\n')

        for i, line in enumerate(lines):
            for keyword in keywords:
                if keyword.lower() in line.lower():
                    # 前後のコンテキストを取得
                    start = max(0, i - context_lines)
                    end = min(len(lines), i + context_lines + 1)
                    context = '\n'.join(lines[start:end])

                    results.append({
                        'keyword': keyword,
                        'line_number': i + 1,
                        'match_line': line,
                        'context': context
                    })
                    break  # 同じ行で複数マッチを避ける

        return results

    def extract_sections(self, content: str, patterns: List[str]) -> List[Dict[str, Any]]:
        """指定パターンにマッチするセクションを抽出"""
        results = []

        for pattern in patterns:
            # セクションヘッダーを探す
            section_regex = rf'(#{1,4}\s*.*{pattern}.*?)(?=\n#{1,4}\s|\Z)'
            matches = re.findall(section_regex, content, re.DOTALL | re.IGNORECASE)

            for match in matches:
                # セクションの最初の200文字程度を抽出
                preview = match[:500] + "..." if len(match) > 500 else match
                results.append({
                    'pattern': pattern,
                    'content': match,
                    'preview': preview
                })

        return results

    def extract_bullet_lists(self, content: str, keywords: List[str]) -> List[str]:
        """キーワードを含む箇条書きを抽出"""
        results = []

        # 箇条書きパターン
        bullet_pattern = r'^[\s]*[-*•]\s+.+$'
        lines = content.split('\n')

        in_relevant_section = False
        current_list = []

        for line in lines:
            # キーワードがあるセクションをマーク
            if any(kw.lower() in line.lower() for kw in keywords):
                in_relevant_section = True

            # 見出しで切り替え
            if line.startswith('#'):
                if current_list:
                    results.extend(current_list)
                    current_list = []
                in_relevant_section = any(kw.lower() in line.lower() for kw in keywords)

            # 箇条書きを収集
            if in_relevant_section and re.match(bullet_pattern, line):
                current_list.append(line.strip())

        if current_list:
            results.extend(current_list)

        return results

    def extract_for_chapter(self, chapter_id: str) -> Dict[str, Any]:
        """特定の章のナレッジを抽出"""
        if chapter_id not in CHAPTER_CONFIGS:
            raise ValueError(f"Unknown chapter: {chapter_id}")

        config = CHAPTER_CONFIGS[chapter_id]
        print(f"\n{'='*60}")
        print(f"章: {config.title} ({config.page_range})")
        print(f"{'='*60}")

        extraction_result = {
            'chapter_id': chapter_id,
            'title': config.title,
            'page_range': config.page_range,
            'description': config.description,
            'keywords_used': config.keywords,
            'sources_used': config.sources,
            'extracted_sections': [],
            'keyword_matches': [],
            'bullet_points': [],
        }

        # 各ソースファイルから抽出
        for source in config.sources:
            print(f"\n  処理中: {source}")
            content = self.load_knowledge_file(source)
            if not content:
                continue

            # セクション抽出
            sections = self.extract_sections(content, config.section_patterns)
            for section in sections:
                section['source'] = source
            extraction_result['extracted_sections'].extend(sections)
            print(f"    - セクション抽出: {len(sections)}件")

            # キーワードマッチ
            matches = self.extract_by_keywords(content, config.keywords)
            for match in matches:
                match['source'] = source
            extraction_result['keyword_matches'].extend(matches)
            print(f"    - キーワードマッチ: {len(matches)}件")

            # 箇条書き抽出
            bullets = self.extract_bullet_lists(content, config.keywords)
            extraction_result['bullet_points'].extend(bullets)
            print(f"    - 箇条書き: {len(bullets)}件")

        return extraction_result

    def generate_knowledge_markdown(self, extraction: Dict[str, Any]) -> str:
        """抽出結果をMarkdown形式で出力"""
        lines = []

        # ヘッダー
        lines.append(f"# {extraction['title']} - ナレッジ抽出結果")
        lines.append("")
        lines.append(f"**ページ範囲**: {extraction['page_range']}")
        lines.append(f"**概要**: {extraction['description']}")
        lines.append("")
        lines.append(f"## 使用したソース")
        for source in extraction['sources_used']:
            lines.append(f"- {source}")
        lines.append("")

        # 抽出したセクション
        lines.append("## 抽出したセクション")
        lines.append("")

        seen_previews = set()
        for i, section in enumerate(extraction['extracted_sections'], 1):
            preview_key = section['preview'][:100]
            if preview_key in seen_previews:
                continue
            seen_previews.add(preview_key)

            lines.append(f"### セクション {i} (from {section['source']})")
            lines.append(f"**パターン**: `{section['pattern']}`")
            lines.append("")
            lines.append("```")
            lines.append(section['content'][:2000])  # 長すぎる場合は切り詰め
            if len(section['content']) > 2000:
                lines.append("... (省略)")
            lines.append("```")
            lines.append("")

        # キーワードマッチの要約
        lines.append("## キーワードマッチ要約")
        lines.append("")

        keyword_counts = {}
        for match in extraction['keyword_matches']:
            kw = match['keyword']
            keyword_counts[kw] = keyword_counts.get(kw, 0) + 1

        for kw, count in sorted(keyword_counts.items(), key=lambda x: -x[1]):
            lines.append(f"- **{kw}**: {count}件")
        lines.append("")

        # 重要な箇条書き
        lines.append("## 抽出した重要ポイント（箇条書き）")
        lines.append("")

        unique_bullets = list(set(extraction['bullet_points']))[:50]  # 重複除去、50件まで
        for bullet in unique_bullets:
            lines.append(bullet)
        lines.append("")

        return '\n'.join(lines)

    def save_extraction(self, chapter_id: str, extraction: Dict[str, Any]):
        """抽出結果を保存"""
        output_path = self.output_dir / chapter_id / "knowledge_extraction.md"
        markdown = self.generate_knowledge_markdown(extraction)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown)

        print(f"\n保存完了: {output_path}")
        return output_path

    def run_all(self):
        """全章のナレッジを抽出"""
        results = {}
        for chapter_id in CHAPTER_CONFIGS:
            extraction = self.extract_for_chapter(chapter_id)
            self.save_extraction(chapter_id, extraction)
            results[chapter_id] = extraction
        return results

    def run_single(self, chapter_id: str):
        """単一章のナレッジを抽出"""
        extraction = self.extract_for_chapter(chapter_id)
        self.save_extraction(chapter_id, extraction)
        return extraction


def main():
    parser = argparse.ArgumentParser(description='ナレッジ抽出スクリプト')
    parser.add_argument('--project', type=str, default='..',
                        help='プロジェクトルートディレクトリ')
    parser.add_argument('--chapter', type=str, default=None,
                        help='抽出する章ID（省略時は全章）')
    parser.add_argument('--list', action='store_true',
                        help='利用可能な章を一覧表示')

    args = parser.parse_args()

    if args.list:
        print("利用可能な章:")
        for chapter_id, config in CHAPTER_CONFIGS.items():
            print(f"  {chapter_id}: {config.title} ({config.page_range})")
        return

    project_root = Path(args.project).resolve()
    extractor = KnowledgeExtractor(project_root)

    if args.chapter:
        extractor.run_single(args.chapter)
    else:
        extractor.run_all()


if __name__ == "__main__":
    main()
