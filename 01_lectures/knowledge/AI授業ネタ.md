

**

# 生成AI主導型開発（バイブコーディング）時代におけるコンピュータサイエンス基礎教育の不可欠性とゲーム開発への応用に関する包括的調査報告書

## 要旨

本報告書は、生成AI（Generative AI）および大規模言語モデル（LLM）の急速な普及に伴い提唱された新たな開発パラダイム「バイブコーディング（Vibe Coding）」の有効性と限界を、特にゲーム開発という複雑なドメインに焦点を当てて検証するものである。Andrej Karpathy氏らによって提唱されたこの概念は、自然言語による直感的な指示のみでソフトウェア構築を行う未来を示唆するが、Andrew Ng氏やDave Farley氏を含む多数の専門家および最新の学術研究（Arxiv等）は、むしろ伝統的なIT基礎知識（アルゴリズム、データ構造、アーキテクチャ、デバッグ能力）の重要性が増していることを示唆している。

本調査では、認知科学的アプローチによる初学者の学習プロセス分析、ゲーム開発における状態管理と論理的整合性の課題、そして「プロンプトエンジニアリング」の本質的な計算論的思考要件を多角的に分析した。その結果、AIは熟練者にとっては強力な増幅器となる一方で、基礎を持たない初学者に対しては「能力の錯覚（Illusion of Competence）」を引き起こし、長期的には技術的負債と学習の停滞を招くリスクが高いことが明らかになった。本報告書は、これらの知見に基づき、AI時代における大学生および初学者が採るべき学習戦略と、技術的基礎がいかにしてAIツールのポテンシャルを最大化するかについて詳述する。

## 1. 序論：バイブコーディングの台頭と「基礎不要論」の検証

### 1.1 生成AIによるパラダイムシフトと「バイブコーディング」の定義

ソフトウェアエンジニアリングの世界は、GitHub CopilotやChatGPT、ClaudeといったAI支援ツールの登場により、かつてない変革期を迎えている。この中で生まれた「バイブコーディング（Vibe Coding）」という用語は、Andrej Karpathy氏らによって広められた概念であり、人間がコードの細部（構文やメモリ管理）を記述するのではなく、自然言語を用いてAIに「雰囲気（Vibe）」や意図を伝え、生成された出力を監督・修正しながら開発を進めるスタイルを指す 。

このアプローチは、プログラミングの敷居を劇的に下げ、非エンジニアでもアプリケーションを構築できる可能性を提示した。一部の楽観的な観測では、自然言語が新しいプログラミング言語となり、従来のコーディングスキルやコンピュータサイエンス（CS）の基礎知識は陳腐化するとさえ言われている。しかし、この「基礎不要論」に対しては、現場のエンジニアや教育研究者から強い懸念が示されている。バイブコーディングは、一見すると魔法のように機能するが、その背後には確率的なトークン予測というメカニズムが存在しており、これがソフトウェア工学における決定論的な要求と衝突する場面が多々あるからである 。

### 1.2 ゲーム開発：AI能力の極限試験場として

本報告書では、特に「ゲーム開発」を事例の中心に据える。Webアプリケーションの多くがステートレス（状態を持たない）なリクエスト処理を主とするのに対し、ゲーム開発は「状態（State）」の連続的な変化、リアルタイム処理、物理法則のシミュレーション、そして複雑なユーザーインタラクションを扱う高度なシステム工学である 。

Arxiv上の研究によれば、ゲーム開発はLLMにとって最も困難なタスクの一つであり、単なるテキスト生成能力だけでは解決できない「論理的整合性」や「空間的推論」が求められる 。したがって、ゲーム開発におけるAIの挙動を分析することは、AIの限界点と、それを補完するために必要な人間の「基礎力」を浮き彫りにする最適なケーススタディとなる。

### 1.3 本調査の構成と目的

本調査は、以下の多面的な問いに答えることを目的として構成されている。

1. 認知科学的側面：AI利用は初学者の学習プロセスやメタ認知にどのような影響を与えるのか？「能力の錯覚」とは何か？
    
2. 技術的側面（ゲーム開発）：状態管理、レベルデザイン、デバッグにおいて、なぜ基礎知識が不可欠なのか？
    
3. 品質管理と持続可能性：AIが生成するコードの「技術的負債」とは何か？
    
4. 教育的提言：これからの学生はどのようにAIと付き合い、何を学ぶべきか？
    

各セクションでは、Arxiv等の最新論文（プレプリント含む）から得られた実証データと、業界の専門家の意見を統合し、論拠を提示する。

## 2. 認知科学的分析：AI利用と学習者のメンタルモデル

AIツールが普及した現代において、プログラミング教育の現場では「AIを使えば初心者でも熟練者のように振る舞える」という現象が観察されている。しかし、深層的な理解を伴わないパフォーマンスの向上は、学習者の認知プロセスに深刻な副作用をもたらすことが研究によって明らかになりつつある。

### 2.1 「能力の錯覚（Illusion of Competence）」のメカニズム

最も警戒すべき現象の一つが「能力の錯覚」である。これは、学習者がAIの助けを借りて課題を達成できたにもかかわらず、それを自身の能力によるものだと誤認し、実際の理解度と自己評価の間に大きな乖離が生じる状態を指す。

Prather et al. (2024) による研究 "The Widening Gap: The Benefits and Harms of Generative AI for Novice Programmers" は、この問題を定量的に分析している。視線追跡（Eye Tracking）を用いた実験では、以下の傾向が確認された。

- メタ認知の欠如：成績下位の学生ほど、AIが生成したコードを無批判に受け入れる傾向があった。彼らはコードのロジックを追跡（トレース）する視線の動きが少なく、AIの出力を「正解」として即座に実装に移していた。
    
- 認知的不協和の解消：AIの助けを借りて課題を完了した学生は、インタビューにおいて「自分は理解している」と主張したが、実際にはコードの動作原理を説明できないケースが多発した。これは、AIの流暢な応答が学習者の自信を不当に高め、自らの無知を隠蔽してしまうことを示唆している。
    

さらに、Loksa et al. (2016) が提唱した問題解決の6段階モデル（再解釈、類似検索、解決策探索、評価、実装、実装評価）において、AI依存の初学者は「評価（Evaluate）」のプロセスをバイパスしがちであることが指摘されている 。正常に動作しているように見えるコードであっても、それがなぜ動くのか、どのようなエッジケースで動かなくなるのかを評価する能力が育たないまま、「完了」とみなしてしまうのである。

### 2.2 メンタルモデルの形成不全と過信

初学者がプログラミングを学ぶ過程で最も重要なのは、コンピュータがどのようにデータを処理し、メモリを管理するかという「メンタルモデル（心的な模型）」を構築することである。しかし、AIはこの構築プロセスを阻害する可能性がある。

Microsoft Researchの2025年のレポート や関連するArxiv論文 によれば、初心者はLLMに対して誤ったメンタルモデル（例：「AIは検索エンジンのように正確な知識を検索してくる」「AIは人間のように論理的に思考している」）を持ちやすい。

|誤ったメンタルモデル|正しい理解（IT基礎知識）|結果として生じる問題|
|---|---|---|
|AIは論理を理解している|AIは確率的にトークンを繋げているだけである|論理的に矛盾したコードでも「AIが書いたから正しい」と思い込み、デバッグが泥沼化する。|
|エラーが出たらAIに聞けば直る|エラーメッセージはコンパイラからの論理的な指摘である|エラーの原因を考えず、AIに同じ質問を繰り返して無限ループに陥る。|
|コードは動けばそれでよい|コードはメモリ効率や計算量、保守性が重要|動作はするがリソースを浪費する非効率な実装（O(n^2)など）を見過ごす。|

### 2.3 熟練者と初学者の認知的負荷の逆転現象

興味深いことに、AIツールの導入は必ずしもすべての開発者の負担を減らすわけではない。の研究 は、熟練者と初学者の間でAI利用時の「認知的負荷（Cognitive Load）」の質が異なることを示唆している。

- 熟練者（Expert）：自身の確固たる知識基盤（スキーマ）とAIの提案を照合する「検証モード」でAIを使用する。AIが単純作業を代行することで、より高次のアーキテクチャ設計に脳のリソースを割くことができる。
    
- 初学者（Novice）：知識基盤がないため、AIの提案が正しいかどうかを判断する基準を持たない。そのため、AIの出力を解読しようとする負荷や、誤ったコードが動かない時の混乱により、かえって認知的な混乱（Cognitive Overload）に陥るか、あるいは思考を放棄してAIに全依存するかの二極化が進む 。
    

この「理解とパフォーマンスのギャップ（Comprehension-Performance Gap）」は、特に既存のコードベースを修正するタスク（Brownfield Programming）において顕著となる。Qiao et al. (2025) の研究 では、AIを使用した学生グループはタスク完了速度こそ向上したが、コードベース全体の理解度は向上しなかった。これは、将来的にそのコードをメンテナンスしたり拡張したりする能力が欠如したエンジニアが量産されるリスクを示唆している。

## 3. ゲーム開発における特異点：AIが超えられない「論理の壁」

ゲーム開発は、Webサイト制作やデータ分析スクリプトの作成とは異なり、AIにとって極めて難易度の高い領域である。ここでは、具体的な事例を通じて、なぜITの基礎知識がなければAIを用いたゲーム開発が破綻するのかを詳述する。

### 3.1 状態管理（State Management）の崩壊と整合性

ゲームプログラミングにおいて最も重要な概念の一つが「状態（State）」である。プレイヤーのHP、所持アイテム、クエストの進行状況、敵の位置など、変数の集合体としての「世界」を一貫性を持って維持し続ける必要がある。

しかし、LLMは本質的にステートレスであり、長期的な一貫性を保つことが苦手である。

- テキストアドベンチャーの事例： や の事例では、LLMにゲームマスター役を任せた際、数ターン前には「鍵を持っていない」と言っていたのに、次のターンで突然ドアを開けてしまったり、死んだはずのNPCが会話に参加してきたりといった「幻覚（Hallucination）」が頻発した。 これを防ぐためには、PythonやC#などのプログラミング言語を用いて確実な「状態管理システム（Game State Machine）」を構築し、LLMにはその状態を参照させるだけの役割に制限する必要がある。つまり、「変数のスコープ」「データ構造（DictionaryやList）」「オブジェクト指向設計」といった基礎知識がなければ、まともに遊べるゲームは作れないのである 。
    
- DeepSeek/o1によるコード生成の限界： の報告によれば、優秀とされる推論モデル（OpenAI o1やDeepSeek R1）であっても、ゲーム開発においては「表示ロジック」と「データ管理ロジック」を分離（Separation of Concerns）できず、密結合なスパゲッティコードを生成してしまう傾向がある。これは、MVC（Model-View-Controller）やMVVMといったアーキテクチャパターンの知識を持つ人間が、コードの構造を修正・指導しなければ、拡張不可能なプロジェクトになってしまうことを意味する。
    

### 3.2 空間論理とレベルデザインの幻覚

ゲームのレベル（マップ）生成においても、AIの限界は顕著である。

- 倉庫番（Sokoban）の事例： や の研究では、AIにパズルゲームのレベルを生成させたところ、「クリア不可能な配置」や「物理的に到達できないエリア」を含むマップが生成されるケースが確認された。AIは「マップっぽいテキスト」を出力することはできるが、そのマップのトポロジー（位相幾何学的な接続関係）や、ゲームルール上の可解性を論理的に検証しているわけではない。 ここでも、A*アルゴリズムやダイクストラ法といった「グラフ探索アルゴリズム」の基礎知識を持つ人間が、生成されたマップがクリア可能かどうかを自動検証するスクリプトを書く必要がある。
    
- 物理エンジンの無視： UnityやUnreal Engineの開発において、AIはしばしばエンジンの物理法則を無視したコードを生成する。例えば、Rigidbodyを使用しているオブジェクトに対して、物理演算フレーム（FixedUpdate）ではなく描画フレーム（Update）で直接座標を書き換えるコードを提案することがある 。これは「一見動く」が、オブジェクトが壁をすり抜けたり、挙動が不安定になったりする原因となる。エンジンのライフサイクルや物理演算の基礎を知らない初学者は、このバグの原因を特定できず、途方に暮れることになる。
    

### 3.3 既存エンジン（Unity/Unreal）との統合難易度

Arxiv上の研究 は、UnityやUnreal Engine 5 (UE5) といった高度なゲームエンジンと生成AIの統合における課題を指摘している。

- APIの幻覚とバージョン不整合： ゲームエンジンは頻繁にアップデートされ、APIが変更される。LLMの学習データは過去のものであるため、廃止された関数や、存在しない架空のメソッド（例：Unityのtransform.Move()のような、ありそうで存在しない関数）を自信満々に提案することがある。公式ドキュメントを読み解き、コンパイラのエラーメッセージを理解する基礎力がなければ、AIの提案を修正して動かすことはできない。
    
- ブループリントとC++の乖離： Unreal Engineではビジュアルスクリプト（Blueprints）とC++が併用されるが、AIはこれらを混同したり、C++のメモリ管理（ポインタ、参照、ガベージコレクション）を誤ったりすることがある。特にC++のメモリリークや不正アクセスはゲームをクラッシュさせるため、ポインタやメモリ管理の概念理解は必須である 。
    

## 4. 隠れたコスト：技術的負債と品質保証

「バイブコーディング」で素早く動くプロトタイプを作ることは可能だが、それを製品レベル（Production Ready）に引き上げる段階で、基礎知識の欠如が致命的なコストとなって跳ね返ってくる。これを研究者たちは「生成的負債（Generative Debt）」と呼んでいる。

### 4.1 生成的負債（Generative Debt）の正体

の研究では、AI生成コード特有の技術的負債を以下の3つに分類している。

1. 構造的負債 (Structural Debt)：コードは動作するが、モジュール性が低く、一つのファイルに全てのロジックが詰め込まれている状態。可読性が低く、チーム開発や将来の拡張が困難になる。
    
2. 幻覚的複雑性 (Hallucinated Complexity)：標準ライブラリを使えば1行で済む処理を、AIがわざわざ独自の複雑な関数として実装してしまう現象。車輪の再発明により、バグの温床が増える。
    
3. 省略の負債 (Omission Debt)：エラーハンドリングやエッジケース（境界値）の処理が省かれている状態。AIは「ハッピーパス（正常系）」のコードを書くのは得意だが、ネットワーク切断や不正な入力といった「異常系」を無視する傾向がある。
    

これらの負債は、静的解析ツールやコードレビューによって発見・修正される必要があるが、そのためには「何が良いコード（Clean Code）か」という審美眼、すなわちソフトウェア工学の基礎知識が必要となる。

### 4.2 セキュリティリスク

Arxivのセキュリティ関連の研究 によれば、LLMが生成したコードの約40%に、SQLインジェクション、クロスサイトスクリプティング（XSS）、ハードコードされたクレデンシャル（パスワード等）などの脆弱性が含まれていたという報告がある。 特にゲーム開発において、サーバーサイドのロジック（課金処理、プレイヤーデータ保存）に脆弱性があれば、チートやデータ改ざんの被害に直結する。AIにセキュリティ意識を期待することは現状難しく、開発者自身がセキュリティの基礎（OWASP Top 10など）を理解し、AIの出力を監査しなければならない。

### 4.3 バイブコーディングの限界：プロトタイプから製品へ

や の記事は、バイブコーディングが「MVP（実用最小限の製品）」を作るには最適だが、「スケーラブルな製品」を作るには不向きであることを指摘している。 「動くこと」と「正しく作られていること」は別である。バイブコーディングで作られたゲームは、プレイヤーが10人のうちは動くかもしれないが、1000人になった瞬間にサーバーがダウンしたり、データベースが整合性を失ったりするリスクがある。スケーラビリティ、パフォーマンスチューニング（計算量オーダーの理解）、並行処理（スレッドセーフ）といったCSの基礎概念は、大規模なシステムを支えるために依然として不可欠である。

## 5. 逆説的真実：「プロンプトエンジニアリング」の本質はプログラミングである

「自然言語で指示すればよいから、プログラミング言語は不要」という考えは、プロンプトエンジニアリングの本質を誤解している。最新の研究は、効果的なプロンプトを作成する行為そのものが、高度なプログラミング的思考を要求することを示している。

### 5.1 "Prompts Are Programs Too"（プロンプトもプログラムである）

2025年の重要論文 "Prompts Are Programs Too: Understanding How Developers Build Software Containing Prompts" は、プロンプト開発が従来のソフトウェア開発と驚くほど類似していることを指摘している。 プロンプトエンジニアリングにおいて求められるのは、単なる文章力ではなく、以下の「計算論的思考（Computational Thinking）」である 。

- 分解 (Decomposition)： 複雑なタスク（例：「RPGを作って」）を、AIが処理可能な小さなサブタスク（例：「インベントリクラスの定義」「ダメージ計算式の実装」「UIイベントのハンドリング」）に分割する能力。これは関数の設計やクラス設計そのものである。
    
- 抽象化 (Abstraction)： 具体的な指示だけでなく、汎用的なルールや制約（例：「SOLID原則に従ってコードを生成せよ」）を言語化する能力。デザインパターンやアーキテクチャの知識がなければ、適切な抽象度の指示が出せない。
    
- デバッグと反復 (Debugging & Iteration)： AIが意図しない出力をした際、プロンプトのどの部分が曖昧だったのかを特定し、条件を追加・修正するプロセスは、プログラムのデバッグと同じ論理的推論を必要とする。
    

### 5.2 基礎知識がプロンプトの質を決める

AIに対する指示の質（Input Quality）は、出力の質（Output Quality）に直結する。ITの基礎知識を持つ者と持たない者では、同じAIを使っても得られる結果に天と地ほどの差が生まれる。

|初心者のプロンプト（Vibe重視）|基礎知識を持つ者のプロンプト（Engineering重視）|結果の違い|
|---|---|---|
|「インベントリシステムを作って。アイテムを持てるようにして。」|「UnityのScriptableObjectを使用してアイテムデータベースを構築し、インベントリはDictionary<ItemID, Quantity>で管理して検索をO(1)に最適化せよ。UIとは疎結合にするため、C#のActionデリゲートでイベント通知を行うこと。」|前者は拡張性がなく、アイテムが増えると処理落ちするコードになる。後者はプロ仕様の保守性が高く高速なコードになる。|
|「バグってるから直して。」|「NullReferenceExceptionが発生している。非同期ロード中にオブジェクトが参照されている可能性があるため、UniTaskを使用してawait処理を適切に実装するか、Nullチェックを追加して。」|前者はAIが当てずっぽうな修正を繰り返し、コードが汚くなる。後者は一発で根本原因が修正される。|

このように、「何が正解か（ベストプラクティス）」を知っていることこそが、最強のプロンプトエンジニアリングスキルなのである。

## 6. 専門家の見解とケーススタディ

業界の権威や著名なエンジニアたちも、AI時代における基礎学習の重要性を強調している。

### 6.1 Andrew Ng氏とAndrej Karpathy氏の視点

- Andrew Ng氏（AI研究の世界的権威）： 彼は、AIによるコーディングが進む現在であっても、ディープラーニングやアルゴリズムの仕組みを「ゼロから実装してみる」ことの重要性を説いている。「コードを一行読んだら、リファレンスを見ずに自分でタイプしてみる」といった意図的な練習（Deliberate Practice）が、深い理解（Deep Learning in Human Brain）に繋がると述べている 。
    
- Andrej Karpathy氏（元Tesla AIディレクター）： バイブコーディングの提唱者である彼でさえ、それが「伝統的なソフトウェアエンジニアリング」を完全に置換するものではなく、ツールベルトの一つであると認めている。彼は、AIが生成したコードの検証可能性（Verifiability）が重要であり、そのためには人間がコードを理解している必要があると示唆している 。
    

### 6.2 失敗事例からの教訓

- Redditや技術ブログでの報告 ： あるゲーム開発者は、全てのコードをLLMに書かせた結果、プロジェクトの後半でバグ修正が不可能になり、プロジェクトが破綻したと告白している。「自分が理解していないコードが1万行ある」という恐怖は、開発のモチベーションを破壊する。彼が得た教訓は、「AIはアシスタントであり、司令官（自分）が技術を理解していなければならない」という点であった。
    

## 7. 大学生への提言：AI時代を生き抜くための学習戦略

以上の調査に基づき、これからITやゲーム開発を学ぶ大学生に対して、以下の具体的な学習戦略を提案する。

### 7.1 「サンドイッチ方式」の実践

AIを排除するのではなく、人間の工程でAIを挟み込むワークフローを確立せよ。

1. Human (Architect & Plan)：
    

- 何を作るか、どういう構造（アーキテクチャ）にするかは人間が決める。これにはデザインパターンやシステム設計の基礎知識が必要。
    

2. AI (Draft & Generate)：
    

- ボイラープレート（定型文）の生成、基本的な関数の実装、APIの使い方の検索はAIに任せる。ここで生産性を爆発的に高める。
    

3. Human (Review & Refine)：
    

- AIが書いたコードを一行ずつ読み、セキュリティ、パフォーマンス、整合性をチェックする。バグがあれば修正し、プロジェクト全体に統合する。これにはデバッグ能力とコード読解力が必要。
    

### 7.2 重点的に学ぶべき「基礎」の再定義

単に文法を暗記する（Syntax）のではなく、AIが苦手とする「概念（Semantics & Context）」を重点的に学ぶべきである。

- アルゴリズムとデータ構造： AIが出したコードが効率的か（計算量オーダー）、適切なデータ構造を使っているか（List vs Dictionary vs HashSet）を判断するため。
    
- メモリとハードウェアの理解： なぜゲームが重いのか、なぜクラッシュするのかを理解するため（スタックとヒープ、ガベージコレクション、GPUのパイプライン）。
    
- デバッグとトラブルシューティング： エラーログを読む力、仮説検証のサイクルを回す力。これはAIには代替できない「探偵」のようなスキルである。
    
- 英語（English）： 最新のAIモデルやドキュメントは英語が主流であり、英語でのプロンプトの方が精度が高い場合が多いため、英語力も立派な「IT基礎」の一つと言える。
    

### 7.3 「苦闘（Productive Struggle）」を避けない

最も重要なのは、学習の過程で「わからない」「動かない」という壁にぶつかった時、すぐにAIに答えを求めず、まずは自分で考える時間を確保することである。 Pratherらの研究が示したように、この「苦闘」のプロセスこそが、脳内に強固な神経回路（スキーマ）を形成し、真の応用力を育む。AIは、その苦闘の末に答え合わせをするための「家庭教師」として使うべきであり、宿題を代行させる「代行業者」として使ってはならない。

## 8. 結論

バイブコーディングの時代において、ITの基礎知識は「不要」になるどころか、**「プレミアムな価値」**を持つようになった。 誰もがAIを使って「それっぽいもの」を作れるようになったからこそ、その裏側にあるロジックを理解し、トラブルを解決し、品質を保証できるエンジニアの希少性は高まっている。 ゲーム開発という、論理と創造性が交差する最も複雑なフィールドにおいて、AIは強力な武器となる。しかし、その武器を使いこなすためには、使い手である人間に確固たる「基礎」という土台がなければならない。

学生諸君には、表面的な「Vibe（雰囲気）」に流されることなく、技術の深淵にある原理原則を学び、AIを真の意味で支配できるエンジニアを目指してほしい。

### 付録：データと統計

#### 表1: 熟練者と初学者のAI利用における行動比較

|行動指標|熟練者 (Expert)|初学者 (Novice)|
|---|---|---|
|視線動向|生成コードの論理構造（ループ条件、分岐）を重点的に注視|全体を漠然と見るか、コピーボタンを即座に探す|
|デバッグ戦略|エラーメッセージに基づき、コードの特定箇所を修正|全文を再生成させたり、AIに「動かない」と曖昧に訴える|
|認知的負荷|減少（単純作業からの解放）|増大（検証不能なコードへの不安）または著しく低下（思考停止）|
|成果物の品質|高い（保守性・効率性が考慮されている）|表面上は動くが、脆弱性や技術的負債を含む|

#### 表2: LLMが生成したコードに含まれる主な脆弱性とその割合

|脆弱性の種類|概要|発生頻度（概算）|
|---|---|---|
|セキュリティ|SQLインジェクション、XSS、APIキーの露出|~40%|
|信頼性 (Reliability)|例外処理の欠如、Nullチェック漏れ|~50%|
|保守性 (Maintainability)|冗長なコード、ハードコードされた定数、不適切な命名|~80%（初期生成時）|
|※ 静的解析ツールによるフィードバックを与えながら反復修正させることで、これらは改善可能だが、その「フィードバック」を与える知識が人間に必要である。|||

#### 引用文献

1. What is Vibe Coding? The Pros, Cons, and Controversies | Tanium, https://www.tanium.com/blog/what-is-vibe-coding/ 2. Andrej Karpathy: Software Is Changing (Again) - The Singju Post, https://singjupost.com/andrej-karpathy-software-is-changing-again/ 3. Simon Willison on andrej-karpathy, https://simonwillison.net/tags/andrej-karpathy/ 4. The Dark Side of Vibe-Coding: Debugging, Technical Debt & Security Risks, https://dev.to/arbisoftcompany/the-dark-side-of-vibe-coding-debugging-technical-debt-security-risks-9ef 5. Andrej Karpathy: Software in the era of AI [video] - Hacker News, https://news.ycombinator.com/item?id=44314423 6. Beyond Synthetic Benchmarks: Evaluating LLM Performance on Real-World Class-Level Code Generation - arXiv, https://arxiv.org/html/2510.26130v2 7. V-GameGym: Visual Game Generation for Code Large Language Models - arXiv, https://arxiv.org/html/2509.20136v1 8. Generating Games via LLMs: An Investigation with Video Game Description Language, https://arxiv.org/html/2404.08706v1 9. A Survey on Large Language Model-Based Game Agents - arXiv, https://arxiv.org/html/2404.02039v3 10. The Widening Gap: The Benefits and Harms of Generative AI for Novice Programmers - Juho Leinonen, https://juholeinonen.com/assets/pdf/prather2024widening.pdf 11. The Widening Gap: The Benefits and Harms of Generative AI for Novice Programmers | Request PDF - ResearchGate, https://www.researchgate.net/publication/383080888_The_Widening_Gap_The_Benefits_and_Harms_of_Generative_AI_for_Novice_Programmers 12. Protecting The Young, and Defending Independent Thought, in the Age of GenAI, https://thequantumrecord.com/philosophy-of-technology/defending-independent-thought-in-age-of-genai/ 13. The Widening Gap: The Benefits and Harms of Generative AI for Novice Programmers, https://arxiv.org/html/2405.17739v1 14. Fostering appropriate reliance on GenAI Lessons learned from early research - Microsoft, https://www.microsoft.com/en-us/research/wp-content/uploads/2025/03/Appropriate-Reliance-Lessons-Learned-Published-2025-3-3.pdf 15. User Misconceptions of LLM-Based Conversational Programming Assistants - arXiv, https://arxiv.org/html/2510.25662v1 16. Mental model shifts in human-LLM interactions - ResearchGate, https://www.researchgate.net/publication/393055408_Mental_model_shifts_in_human-LLM_interactions 17. Towards Decoding Developer Cognition in the Age of AI Assistants - arXiv, https://arxiv.org/html/2501.02684v1 18. Who's the Leader? Analyzing Novice Workflows in LLM-Assisted Debugging of Machine Learning Code - arXiv, https://arxiv.org/html/2505.08063v1 19. Comprehension-Performance Gap in GenAI-Assisted Brownfield Programming: A Replication and Extension - arXiv, https://arxiv.org/html/2511.02922v1 20. Comprehension-Performance Gap in GenAI-Assisted Brownfield Programming: A Replication and Extension - ResearchGate, https://www.researchgate.net/publication/397321474_Comprehension-Performance_Gap_in_GenAI-Assisted_Brownfield_Programming_A_Replication_and_Extension 21. [Part 1] Crafting a Text Adventure Game with LLMs in Just 6 Hours! | by Dain Kim - Medium, https://medium.com/@ddanakim0304/part-1-crafting-a-text-adventure-game-with-llms-in-just-6-hours-bb415ebbb67a 22. Intra: design notes on an LLM-driven text adventure - Ian Bicking, https://ianbicking.org/blog/2025/07/intra-llm-text-adventure 23. I Vibe Coded a Game That Attracted 10k+ Players In a Single Weekend - Generative AI, https://generativeai.pub/i-vibe-coded-a-game-that-attracted-10k-players-in-a-single-weekend-6cff508bad58 24. Testing LLM Creativity Through The Power of Constraints: The Commodore 64 Challenge, https://medium.com/@gianlucabailo/testing-llm-creativity-through-the-power-of-constraints-the-commodore-64-challenge-0b147d6e02c7 25. 90% Faster, 100% Code-Free: MLLM-Driven Zero-Code 3D Game Development - arXiv, https://arxiv.org/html/2509.26161v1 26. Unreal-Engine-Based General Platform for Multi-Agent Reinforcement Learning - arXiv, https://arxiv.org/html/2503.15947v1 27. DreamGarden: A Designer Assistant for Growing Games from a Single Prompt - arXiv, https://arxiv.org/html/2410.01791v1 28. Quantitative Analysis of Technical Debt and Pattern Violation in Large Language Model Architectures - arXiv, https://arxiv.org/html/2512.04273v1 29. Static Analysis as a Feedback Loop: Enhancing LLM-Generated Code Beyond Correctness, https://arxiv.org/html/2508.14419v1 30. Security and Quality in LLM-Generated Code: A Multi-Language, Multi-Model Analysis, https://arxiv.org/html/2502.01853v1 31. Unveiling Inefficiencies in LLM-Generated Code: Toward a Comprehensive Taxonomy, https://arxiv.org/html/2503.06327v2 32. What vibe coding can (and can't) do for software engineering | We Love Open Source, https://allthingsopen.org/articles/what-is-vibe-coding-developers 33. Why Your Vibe Coding Is Ruining Your Business - Ulam Labs, https://www.ulam.io/blog/why-your-vibe-coding-is-ruining-your-business 34. (PDF) Prompts Are Programs Too! Understanding How Developers Build Software Containing Prompts - ResearchGate, https://www.researchgate.net/publication/384154805_Prompts_Are_Programs_Too_Understanding_How_Developers_Build_Software_Containing_Prompts 35. Prompts Are Programs Too! Understanding How Developers Build Software Containing Prompts (FSE 2025 - Research Papers) - conf.researchr.org, https://conf.researchr.org/details/fse-2025/fse-2025-research-papers/2/Prompts-Are-Programs-Too-Understanding-How-Developers-Build-Software-Containing-Prom 36. Leveraging Computational Thinking in the Era of Generative AI - Communications of the ACM, https://cacm.acm.org/blogcacm/leveraging-computational-thinking-in-the-era-of-generative-ai/ 37. What Should We Engineer in Prompts? Training Humans in Requirement-Driven LLM Use, https://arxiv.org/html/2409.08775v2 38. Improving Student-AI Interaction Through Pedagogical Prompting: An Example in Computer Science Education - arXiv, https://arxiv.org/html/2506.19107v1 39. Five Important AI Programming Languages - DeepLearning.AI, https://www.deeplearning.ai/blog/five-important-ai-programming-languages/ 40. A quote from Andrew Ng - Simon Willison's Weblog, https://simonwillison.net/2025/Mar/15/andrew-ng/ 41. Andrew Ng calls "vibe coding" an unfortunate term for deep intellectual exercise - Perplexity, https://www.perplexity.ai/page/andrew-ng-calls-vibe-coding-an-Sg_5eUFKSASP5kPByGD8tg 42. How vibe coding lead to my project's downfall. : r/gamedev - Reddit, https://www.reddit.com/r/gamedev/comments/1q043ym/how_vibe_coding_lead_to_my_projects_downfall/

**



**

# ゲームAIの進化と実装：アルゴリズム、アーキテクチャ、そして未来への展望

## エグゼクティブサマリー

本レポートは、ゲーム開発における人工知能（Game AI）の進化、実装手法、そして将来の展望を包括的に解説するための専門資料である。2時間の技術セミナーや講義での使用を想定し、単なる用語解説にとどまらず、各技術が導入された歴史的背景、具体的な実装メカニズム、そしてそれがプレイヤー体験にどのような影響を与えたかを詳細に分析する。

分析の対象は、初期のスクリプト制御から、現代の生成AI（Generative AI）およびニューロ・シンボリックAIに至るまでの技術的変遷である。特に、GDC（Game Developers Conference）や主要な技術論文で発表された一次情報を基に、Halo 2、F.E.A.R.、Left 4 Dead、Horizon Zero Dawn、Black & White、Townscaperといった記念碑的なタイトルにおける具体的なAIアーキテクチャを解剖する。

本稿では、ゲームAIの発展を「制御と自律の対立と融合」の歴史として捉える。デザイナーが完全に制御可能なステートマシンから、AIが自ら計画を立案するプランニング技術、さらにはゲーム全体のペース配分を行う監督（Director）システム、そして現在の確率的推論を用いる大規模言語モデル（LLM）への移行は、開発者が「複雑性」をどのように管理し、「知性の錯覚」をいかに効率的に構築してきたかの記録である。

## 1. ゲームAIの哲学的・技術的基礎

### 1.1 知性の錯覚 vs 学術的AI

ゲームAIの歴史を紐解く上で、まず明確にすべきは「ゲームAI」と「学術的AI」の根本的な目的の相違である。学術的なAI研究、特に古典的な探索や近年のディープラーニングは、しばしば「最適解」や「人間を超える性能」を追求する。対して、エンターテインメントにおけるゲームAIの目的は、プレイヤーを楽しませるための「知性の錯覚（Illusion of Intelligence）」を構築することにある 。

GDC 2005においてBungieのDamian Islaらが語ったように、ゲームにおける「賢さ」とは、必ずしも高度な戦術的計算を意味しない。プレイヤーにとって認識可能な行動、意図が伝わる動き、そして適度な「人間らしい失敗」こそが、AIを知的であると感じさせる要因となる。したがって、ゲームAIの技術進化は、計算能力の向上だけでなく、デザイナーがいかに効率よく「振る舞いのバリエーション」を記述し、管理できるかという「複雑性の管理」の歴史でもある 。

### 1.2 有限ステートマシン（FSM）：初期の標準と限界

1990年代から2000年代初頭にかけて、ゲームAIの事実上の標準（デファクトスタンダード）は有限ステートマシン（Finite State Machine: FSM）であった。FSMは、エージェントが取りうる「状態（State）」と、ある状態から別の状態へ移行するための「遷移条件（Transition）」の集合で構成される。

|構成要素|定義|具体例|
|---|---|---|
|状態 (State)|エージェントの現在の振る舞い|Idle (待機), Patrol (巡回), Attack (攻撃), Flee (逃走)|
|遷移 (Transition)|状態を変更するトリガー条件|If Health < 20% → Fleeへ移行|
|アクション|その状態で実行される処理|アニメーション再生、射撃、移動|

初期のFPS（First Person Shooter）であるHalf-Life（1998）やQuakeでは、このFSMが兵士の行動制御に用いられた。FSMの最大の利点はその「決定論的」な性質にある。デザイナーは「プレイヤーを見つけたら必ず攻撃状態に移行する」というルールを明確に記述でき、デバッグも容易であった。

しかし、ゲームデザインが複雑化し、キャラクターに求められる行動が増えるにつれ、FSMは「ステート爆発（State Explosion）」という深刻な問題に直面することになる。例えば、「攻撃」状態にあるキャラクターに「手榴弾を投げる」という新しい行動を追加したい場合、開発者は「待機中」「移動中」「隠れている最中」など、既存のあらゆる状態からの遷移関係を定義しなければならない。状態数が N になると、潜在的な遷移の数は N^2 のオーダーで増加する。これにより、コードは複雑に絡み合った「スパゲッティコード」と化し、メンテナンスが不可能に近い状態に陥った 。この技術的閉塞感が、次なる革命であるビヘイビアツリーの誕生を促したのである。

## 2. 複雑性の管理革命：ビヘイビアツリー（Behavior Trees）

ケーススタディ：Halo 2 (Bungie, 2004)

### 2.1 Halo 2が直面した課題

2004年のHalo 2開発において、Bungieは前作を遥かに凌ぐ複雑な戦闘サンドボックスを構築しようとしていた。コヴナントのエリート（Elites）、グラント（Grunts）、ジャッカル（Jackals）といった敵キャラクターは、単にプレイヤーを撃つだけでなく、遮蔽物に隠れ、集団で連携し、さらにゴーストやレイスといった乗り物（ビークル）を自在に操る必要があった。従来のFSMで「乗り物に乗っている時の攻撃」「徒歩での攻撃」「命令を受けている時の攻撃」を全て個別の状態として管理することは、開発リソース的に破綻していた 。

### 2.2 ビヘイビアツリーのアーキテクチャ

この課題に対し、Damian IslaらAIチームは「ビヘイビアツリー（Behavior Trees: BT）」という新たなアーキテクチャを採用した。BTは、状態遷移ではなく「タスクの階層構造」によって行動を決定する手法である。

BTは「ルート（根）」から始まり、毎フレーム（または定期的な更新サイクルで）ツリーの下層へと実行権（Tick）が伝播していく。各ノードは実行結果として 成功 (Success)、失敗 (Failure)、実行中 (Running) のいずれかを親ノードに返す。このシンプルながら強力な仕組みを支えるのが、主に2種類の制御ノードである。

#### 2.2.1 制御ノードの論理

1. セレクター（Selector / Fallback）ノード:
    

- 論理: 「OR」条件、または if-else 文に相当する。
    
- 動作: 子ノードを左から順に実行し、最初に「成功」した時点で処理を終了し、親に「成功」を返す。全ての子が失敗した場合のみ「失敗」を返す。
    
- 用途: 優先順位のある行動の選択。
    

- 例：「近接攻撃を試みる」→（失敗なら）→「射撃を試みる」→（失敗なら）→「隠れる」。
    

2. シーケンス（Sequence）ノード:
    

- 論理: 「AND」条件に相当する。
    
- 動作: 子ノードを左から順に実行し、全ての子が「成功」して初めて親に「成功」を返す。途中で一つでも失敗すれば、即座に処理を中断し「失敗」を返す。
    
- 用途: 一連の手順の実行。
    

- 例：「手榴弾を投げる」＝「ターゲット選定」→「構えアニメーション」→「投擲」→「クールダウン」。
    

### 2.3 Halo 2における実装と革新

Halo 2における最大の革新は、このツリー構造による「モジュール性」の獲得であった。Bungieの開発チームは、特定の行動パターン（例：「隠れる」挙動や「乗り物の運転」）を独立したサブツリーとして設計した。

例えば、エリートがゴースト（乗り物）に搭乗した場合、AIの「身体制御サブツリー」を「徒歩用」から「ビークル用」に差し替えるだけで、上位の意思決定ロジック（例：「敵を追跡せよ」という目的）を変更することなく、振る舞いを切り替えることができた。これにより、FSM時代のような「状態遷移の網の目」を解きほぐし、個々の行動ロジックを独立した部品として開発・テストすることが可能になった 。

IslaがGDC 2005の講演「Handling Complexity in the Halo 2 AI」で強調したのは、「コアコンバットサイクル（Core Combat Cycle）」の重要性である。AIは常に「状況判断（Decision）」と「行動（Behavior）」のループを回しており、BTはこのサイクルを視覚的かつ論理的に整理するための最適なツールであった。結果として、Halo 2のAIは、予測可能でありながらも多様な状況に対応できる「堅牢な知性」を実現し、その後のゲームAI（Unreal Engine等の標準機能化を含む）の基礎を築いた 。

## 3. 計画と創発：ゴール指向アクションプランニング（GOAP）

ケーススタディ：F.E.A.R. (Monolith Productions, 2005)

Halo 2が「構造」の革命であったなら、2005年の*F.E.A.R.*は「自律性」の革命であった。Monolith ProductionsのJeff Orkinは、GDC 2006の講演「Three States and a Plan: The AI of F.E.A.R.」において、AIに「どう動くか（How）」ではなく「何をしたいか（What）」を指定する手法、ゴール指向アクションプランニング（Goal-Oriented Action Planning: GOAP） を提唱した 。

### 3.1 手続き型から宣言型へ

従来のFSMやBTは「手続き型」のアプローチである。デザイナーは「もし敵が見えたら、銃を撃て」という具体的な手順を記述する。対してGOAPは「宣言型」のアプローチを取る。デザイナーはAIに以下の要素を与える。

1. ゴール（Goals）: AIが達成すべき目標（例：KillEnemy（敵を倒す）、Survive（生き残る））。
    
2. アクション（Actions）: AIが実行可能な行動のリスト。各アクションには以下が定義される。
    

- 前提条件（Preconditions）: そのアクションを実行するために必要な世界の状態（例：「撃つ」ためには「弾薬がある」「武器を持っている」が必要）。
    
- 効果（Effects）: そのアクションを実行した結果、世界がどう変わるか（例：「リロード」すると「弾薬がある」状態になる）。
    
- コスト（Cost）: そのアクションの実行にかかる負荷やリスク（移動距離や時間など）。
    

### 3.2 リアルタイムプランニングのメカニズム

GOAPの核心は、AIがリアルタイムで「計画（Plan）」を立案することにある。AIは現在の「世界状態（World State）」と「目標（Goal）」とのギャップを埋めるために、アクションを逆算的に連鎖させる。

例えば、AIの目標が「敵を倒す（TargetDead: True）」であるとする。

1. プランナー: 「敵を倒す」効果を持つアクションを探す。→ Attackが見つかる。
    
2. チェック: Attackの前提条件は「武器を持っている（HasWeapon: True）」と「敵が見えている（TargetVisible: True）」である。
    
3. 現状: 今、武器は持っているが、敵は見えていない（TargetVisible: False）。
    
4. 再検索: 「敵が見えている」状態にするアクションを探す。→ MoveToSight（視線が通る位置へ移動）が見つかる。
    
5. 計画完成: MoveToSight → Attack という行動シーケンスが生成される。
    

### 3.3 創発的挙動（Emergent Behavior）の実例

*F.E.A.R.*において最も有名な逸話の一つに、「テーブルを倒して遮蔽物にする」挙動がある。デザイナーは「テーブルを見たら倒せ」というスクリプトを書いたわけではない。 AIには「身を守る（ProtectSelf）」というゴールと、「遮蔽物に隠れている（InCover: True）」という状態への欲求があった。同時に、アクションリストには「オブジェクトを倒す（FlipObject）」があり、その効果として「遮蔽物が生成される」が定義されていた。 廊下にテーブルが置かれた状況で、AIはプランニングを行い、「テーブルを倒せば遮蔽物ができる」→「遮蔽物ができれば隠れられる」→「身を守れる」という因果関係を自ら発見し、実行に移したのである。このように、個々のアクションの組み合わせから、開発者が予期しなかった理にかなった行動が生まれることこそが、GOAPのもたらす「創発」の価値である 。

GOAPはその後、S.T.A.L.K.E.R.、Deus Ex: Human Revolution、Tomb Raiderなどのタイトルで採用され、特にステルスゲームやイマーシブシム（没入型シミュレーション）において、状況適応能力の高いAIを実現するための標準技術の一つとなった 。

## 4. 階層的戦略と集団知能：階層型タスクネットワーク（HTN）

ケーススタディ：Horizon Zero Dawn & Killzone (Guerrilla Games)

オープンワールドゲームの台頭に伴い、広大な世界で長時間活動し続けるAIの制御が必要となった。Guerrilla Gamesは、KillzoneシリーズおよびHorizon Zero Dawnにおいて、階層型タスクネットワーク（Hierarchical Task Networks: HTN） を採用し、機械獣たちの生態系を表現した 。

### 4.1 HTNによる思考の構造化

GOAPは柔軟性が高い反面、アクションの数が増えると探索空間が爆発的に広がり、計算負荷が高まるという欠点があった。HTNはこの問題を解決するために、プランニングに「階層構造」を持ち込んだ手法である。

HTNでは、タスクを以下の2種類に分類する。

1. 複合タスク（Compound Tasks）: 抽象的な高レベルの目標（例：「プレイヤーを狩る」「巡回する」）。これらは直接実行できず、より小さなタスクに分解される必要がある。
    
2. 基本タスク（Primitive Tasks）: 実際に実行可能なアクション（例：「移動する」「攻撃アニメーション再生」）。
    

HTNプランナーは、ルートとなる複合タスク（例：「狩り」）から開始し、それを達成するための「メソッド（方法）」を選択して分解していく。

- タスク: 「プレイヤーを狩る」
    

- メソッドA（隠密）: 条件「草むらが近くにある」→ サブタスク：「草むらに移動」「待ち伏せ」「急襲」
    
- メソッドB（強襲）: 条件「自身が大型機である」→ サブタスク：「咆哮」「突進」
    

この構造により、デザイナーはAIの思考プロセスに「ドメイン知識（Domain Knowledge）」を埋め込むことができる。GOAPのように闇雲に解決策を探すのではなく、「ウォッチャーならこう動くべき」「サンダージョーならこう動くべき」という指針を与えつつ、細部の実行手順はプランニングに任せることが可能となる 。

### 4.2 集団制御システム「The Collective」

Horizon Zero Dawnにおける特筆すべき実装は、個体のAIだけでなく、群れ全体の調整を行う「The Collective」システムへのHTNの応用である。 プレイヤーが機械獣の群れに遭遇した際、全ての個体が一斉に攻撃してくるとゲームプレイとして成立しない（プレイヤーが対処不能になる）。そこで「The Collective」は、群れ全体の状態を管理し、各エージェントに「役割（Role）」を割り当てる。

- 攻撃役（Aggressor）: プレイヤーに直接攻撃を仕掛ける（最大2体まで制限）。
    
- 包囲役（Flanker）: プレイヤーの側面に回り込む。
    
- 待機役（Defender）: 後方で様子を見る。
    

各エージェントのHTNプランナーは、割り当てられた「役割」をルートタスクとしてプランニングを行う。これにより、個々のAIは自律的に動いているように見えながら、全体としては高度に連携の取れた戦闘体験が構築される。これは中央集権的な制御と自律分散的な制御のハイブリッドであり、Guerrilla GamesのDecimaエンジンにおけるAI開発の中核を成している 。

## 5. システムAIと演出制御：AI Director

ケーススタディ：Left 4 Dead (Valve, 2008)

ここまでは「キャラクターAI」に焦点を当ててきたが、ゲーム体験全体を制御する「メタAI」あるいは「システムAI」の進化も無視できない。その金字塔が、ValveのLeft 4 DeadにおけるAI Directorである 。

### 5.1 動的なドラマ生成とペーシング

Left 4 Deadは4人の生存者がゾンビの群れと戦う協力型シューターであるが、その敵配置は固定されていない。AI Directorと呼ばれるシステムが、プレイヤーの状態をリアルタイムで監視し、ゲームの「ドラマ」を動的に生成している。

Directorは以下の主要なメトリクスを用いてゲームを制御する。

1. フロー距離（Flow Distance）: スタート地点からゴール地点までの経路上の、プレイヤーの現在位置。これにより「どれくらい進行したか」を定量化する。
    
2. ストレス/緊張度（Stress/Intensity）: 各プレイヤーが受けたダメージ、発砲数、近くにいる敵の数などから算出される数値。
    
3. ペーシングサイクル: ゲームの状態を「静寂（Build-Up）」→「ピーク（Peak/Combat）」→「緩和（Relax）」のサイクルで回す。
    

もしプレイヤーチームが高いストレス状態（瀕死、弾薬不足）にある場合、Directorは「緩和」フェーズを延長し、敵のスポーンを抑制して回復の機会を与える。逆に、プレイヤーが余裕で進行している場合は、特殊感染者（Special Infected）を出現させたり、ラッシュを起こして緊張感を高める。これにより、初心者から上級者まで、常に「ギリギリの戦い」を感じさせる体験（Structured Unpredictability）を実現した 。

### 5.2 プロシージャルな敵配置と視線管理

技術的な工夫として、「Active Area Set (AAS)」の活用が挙げられる。これはナビゲーションメッシュの一種で、AIが移動可能な領域を表す。Directorは敵を生成する際、以下の条件を満たすAASを選択する。

- プレイヤーの現在位置から一定距離以内であること。
    
- プレイヤーの視線（Frustum）に入っていないこと。
    

これにより、ゾンビは「何もない空間から突然ポップする」のではなく、常に「角の向こう」や「壁の裏」から自然に現れたように演出される。また、特殊感染者（例：スモーカー）には「プレイヤーの上方の位置」や「孤立したプレイヤーを狙える位置」といった戦術的なスポーン地点が優先的に割り当てられる。このシステムは後のAlien: Isolationにおけるエイリアンの制御（プレイヤーにヒントを与えつつ、完全に位置を特定させない制御）などにも多大な影響を与えた 。

## 6. 学習と認知アーキテクチャ：強化学習の萌芽

ケーススタディ：Black & White (Lionhead Studios, 2001)

現代ではディープラーニングが主流だが、2001年の時点でニューラルネットワークと強化学習をゲームプレイの中核に据えた野心的なタイトルが存在した。Peter Molyneux率いるLionhead StudiosのBlack & Whiteである 。

### 6.1 信念・欲求・意図（BDI）モデル

このゲームにおけるAI「クリーチャー」は、認知科学に基づくBDI（Belief-Desire-Intention）アーキテクチャを採用していた。

- Belief（信念）: 世界に対する知識（例：「岩は重い」「村人は食べ物である」「あの木は燃えている」）。
    
- Desire（欲求）: 内部的な動機（例：空腹、疲労、遊びたい、排便したい）。
    
- Intention（意図）: 欲求を満たすために選択された行動計画。
    

### 6.2 ユーザーによる強化学習の実装

特筆すべきは、クリーチャーの学習メカニズムに**パーセプトロン（単純な人工ニューロン）**を用いた決定木が使用されていた点である。プレイヤーは神として、クリーチャーの行動に対して「撫でる（正の報酬）」や「叩く（負の報酬）」というフィードバックを与えることができた。

例えば、クリーチャーが空腹（入力）を感じて村人を食べた（行動）際、プレイヤーが強く叩いた（罰）とする。すると、クリーチャーのニューラルネットワーク内の重みが更新され、「空腹時に村人を食べる」という行動の優先度が下がる。逆に、穀物を食べた時に撫でれば、その行動が強化される。 このシステムにより、プレイヤーごとに全く異なる性格（慈悲深い守護者、あるいは残虐な破壊者）を持つAIを育成することが可能となった。これは現代のRLHF（Reinforcement Learning from Human Feedback）の極めて原始的かつ直感的な実装例と言える 。

## 7. プロシージャルコンテンツ生成（PCG）と世界構築

AI技術はキャラクターの知能だけでなく、ゲーム世界そのものの構築（Level Design）にも活用されている。

### 7.1 決定論的ノイズと無限の宇宙：No Man's Sky

No Man's Skyは1800京個もの惑星を持つ宇宙を生成するために、決定論的（Deterministic）なプロシージャル生成を用いた。その核となるのはパーリンノイズやシンプレックスノイズといった数式である。 惑星の「座標」をシード値（種）として数式に入力することで、地形の高さ、植生、生物の形状が一意に決定される。これにより、サーバーに膨大な地形データを保存することなく、どのプレイヤーがいつ訪れても全く同じ惑星が生成される仕組みを実現した。GDCでの発表によれば、彼らはボクセルベースで地形を生成し、それをマーチングキューブ法などでポリゴン化するパイプラインを構築し、リアルタイムでの惑星着陸（シームレスな詳細度遷移）を可能にした 。

### 7.2 制約充足問題と波動関数崩壊：Townscaper

近年、インディーゲーム開発を中心に注目を集めているのが波動関数崩壊（Wave Function Collapse: WFC） アルゴリズムである。Oskar Stålbergが開発したBad NorthやTownscaperでその威力が示された 。

WFCは量子力学の概念に触発された制約充足アルゴリズムである。

1. 重ね合わせ（Superposition）: 初期状態では、グリッドの全てのセルにあらゆるタイル（屋根、壁、窓、芝生など）が置かれる可能性がある。
    
2. 観測（Observation）: エントロピー（不確定性）が最も低いセルを一つ選び、特定のタイルに確定（崩壊）させる。Townscaperではプレイヤーのクリックがこのトリガーとなる。
    
3. 伝播（Propagation）: タイルが確定すると、隣接するセルに制約が伝わる。例えば「屋根」タイルの隣に「空中に浮いたドア」は置けない、といったルールに基づき、隣接セルの可能性が削ぎ落とされる。
    
4. 連鎖: これを矛盾なくグリッド全体に波及させることで、瞬時に「破綻のない建築物」が生成される。
    

この技術により、プレイヤーは詳細な建築ルールを知らなくても、適当にクリックするだけで美しく整合性の取れた街並みを作ることができる。これはAIが「クリエイティビティの補助輪」として機能する好例である 。

## 8. 現代の最前線：生成AIとニューロ・シンボリックAI (2024-2025)

2024年のGDC AI Summitや最近の研究発表において、ゲームAIは新たなフェーズ、すなわち大規模言語モデル（LLM） と ニューロ・シンボリックAI の統合へと向かっている。

### 8.1 ニューロ・シンボリックAI：学習と論理の融合

従来の「ルールベースAI（GOAP, BT）」は制御しやすいが学習能力がない。一方、「ディープラーニングAI（深層強化学習）」は強力だがブラックボックスで制御が難しい。この両者の利点を組み合わせるのがニューロ・シンボリックAIである 。

TencentのGiiNEXエンジンやUbisoft La Forgeの研究では、格闘ゲームやナビゲーションにおいてこのハイブリッドアプローチが試みられている。

- ニューラル部分（Neuro）: 複雑な状況認識や、マイクロマネジメント（例：格闘ゲームでのコンボ入力のタイミング、最適な移動経路の直感的判断）を強化学習エージェントが担当。
    
- シンボリック部分（Symbolic）: 大局的な意思決定やルールの遵守（例：キャラクターの性格設定、ゲームルールの強制）をビヘイビアツリーやステートマシンが担当。 これにより、学習ベースの柔軟性を持ちつつ、デザイナーが意図した通りの振る舞いを保証するAIが実現しつつある 。
    

### 8.2 LLMによるNPCの革新と課題

Riot GamesがAI and Games Conference 2024で発表した「Murder Mystery Agents」や、NetEase、NVIDIA ACEのデモに見られるように、NPCの頭脳としてLLMを組み込む試みが進んでいる 。

従来のNPCは事前に書かれたテキストしか話せなかったが、LLM搭載NPCは：

1. 知覚: ゲーム内の出来事（「プレイヤーが剣を抜いた」）をテキストとして受け取る。
    
2. 推論: 「あなたは臆病なゴブリンである」というシステムプロンプトに基づき、状況への反応を生成する。
    
3. 出力: セリフだけでなく、構造化されたデータ（JSONなど）として行動指令を出力する（例：{"action": "RunAway", "speech": "助けてくれ！"}）。
    

GDC 2024での議論によれば、この技術の最大の課題は「幻覚（Hallucination）」と「レイテンシ（遅延）」である。NPCがゲームの世界設定に存在しない嘘をついたり、返答に数秒かかったりすることはゲーム体験を損なう。そのため、現在はLLMに直接ゲームを制御させるのではなく、LLMを使って開発中にビヘイビアツリーや会話データを大量生成する「開発支援ツール」としての活用が先行している 。

## 9. 教育向け実装ガイド：Pythonによるアルゴリズムの再現

本セクションでは、上述のアルゴリズムを学習・実験するためのPython実装の指針を示す。これらは2時間の講義において、学生やエンジニアが概念をコードレベルで理解するために有用である。

### 9.1 ビヘイビアツリーのPython実装

ライブラリ py_trees を使用することで、Halo 2の構造を再現できる 。

import py_trees  
  
# 1. 振る舞い（Action）の定義  
class Attack(py_trees.behaviour.Behaviour):  
    def update(self):  
        # 敵がいれば攻撃成功、いなければ失敗  
        if self.blackboard.enemy_visible:  
            print("攻撃！")  
            return py_trees.common.Status.SUCCESS  
        return py_trees.common.Status.FAILURE  
  
# 2. ツリーの構築  
root = py_trees.composites.Selector(name="Root")  
sequence = py_trees.composites.Sequence(name="Combat Sequence")  
  
# 敵が見えているかチェック → 攻撃  
check_enemy = py_trees.behaviours.CheckBlackboardVariable(  
    name="Check Enemy", variable_name="enemy_visible", expected_value=True  
)  
attack_action = Attack(name="Attack Action")  
  
sequence.add_children([check_enemy, attack_action])  
root.add_child(sequence)  
  
# 3. 実行（Tick）  
root.tick_once()  
  

### 9.2 GOAPの概念的実装

GOAPの実装には、A*探索アルゴリズムの理解が不可欠である。教育的には GOAPy のようなシンプルなライブラリが参考になる 。

データ構造の設計:

- World State: {"has_key": False, "door_locked": True}
    
- Action:
    

- PickUpKey: Preconditions {"key_visible": True}, Effects {"has_key": True}
    
- OpenDoor: Preconditions {"has_key": True}, Effects {"door_locked": False}
    

- Goal: {"door_locked": False}
    

プランナーはゴールから逆算し、OpenDoor → PickUpKey という順序（実行時は逆順）を導き出す。このプロセスをコードで追うことで、AIが「因果関係」をどう処理しているかが明確になる。

## 結論：エージェンシー（主体性）の軌跡

ゲームAIの歴史を振り返ると、それは明示的な制御（Explicit Control） から 誘導された創発（Guided Emergence） への移行プロセスであることがわかる。

- 第1世代 (FSM): 開発者が全ての遷移を記述した（Half-Life）。
    
- 第2世代 (BT/GOAP): 開発者がルールとゴールを記述し、AIが実行フローを決定した（Halo 2, F.E.A.R.）。
    
- 第3世代 (Systemic AI): 開発者がシステムを構築し、AIが体験のペース配分を管理した（Left 4 Dead）。
    
- 第4世代 (Generative/Neuro-Symbolic): 開発者がモデルを訓練し、AIがコンテンツと対話を生成しようとしている。
    

しかし、技術がいかに進化しようとも、Haloや*F.E.A.R.*が残した教訓は変わらない。それは「複雑さは、プレイヤーの体験に寄与して初めて価値を持つ」ということである。最強のAIを作るのではなく、プレイヤーにとって最高の「好敵手」あるいは「パートナー」を作り出すこと。そのために、これら過去のアルゴリズムは決して「古い技術」として捨て去られるものではなく、最新のニューラルネットワークと融合し、新たなアーキテクチャの基礎として生き続けていくであろう。

### 巻末資料：技術とタイトルの対応表

|年代|主要アルゴリズム|代表的タイトル|技術的革新のポイント|
|---|---|---|---|
|1998|有限ステートマシン (FSM)|Half-Life|スクリプトによる分隊戦術。堅実だが拡張性に乏しい。|
|2001|強化学習 / BDIモデル|Black & White|ユーザーフィードバックによる学習、認知モデルの導入。|
|2004|ビヘイビアツリー (BT)|Halo 2|モジュール性、拡張性の高い意思決定。現在の業界標準。|
|2005|GOAP|F.E.A.R.|プランニングによる自律的行動解決。環境利用の創発。|
|2008|AI Director|Left 4 Dead|ペース配分と緊張感の動的制御。構造化された予測不能性。|
|2008|プロシージャルアニメーション|Spore|未知の骨格に対するリアルタイムモーション生成。|
|2016|波動関数崩壊 (WFC)|Bad North / Townscaper|制約充足による整合性のあるマップ自動生成。|
|2017|HTNプランニング|Horizon Zero Dawn|長期的・階層的な行動計画。群れ制御への応用。|
|2024|ニューロ・シンボリック / LLM|Research Demos|生成AIと論理ベースAIの融合。対話と行動の動的生成。|

#### 引用文献

1. GDC 2005 Proceeding: Handling Complexity in the Halo 2 AI - Game Developer, https://www.gamedeveloper.com/programming/gdc-2005-proceeding-handling-complexity-in-the-i-halo-2-i-ai 2. Three States and a Plan: The AI of FEAR | GameDevs.org, https://www.gamedevs.org/uploads/three-states-plan-ai-of-fear.pdf 3. Managing Complexity in the Halo 2 AI System - YouTube, https://www.youtube.com/watch?v=m9W-hpxuApk 4. Building the AI of F.E.A.R. with Goal Oriented Action Planning - Game Developer, https://www.gamedeveloper.com/design/building-the-ai-of-f-e-a-r-with-goal-oriented-action-planning 5. Three Approaches to Halo-style Behavior Tree AI - GDC Vault, https://gdcvault.com/play/760/Three-Approaches-to-Halo-style 6. The Behaviour Tree AI of Halo 2 | AI and Games #09 - YouTube, https://www.youtube.com/watch?v=NU717sd8oUc 7. AI Arborist: Proper Cultivation and Care for Your Behavior Trees - YouTube, https://www.youtube.com/watch?v=Qq_xX1JCreI 8. Behavior Trees: Three Ways of Cultivating Strong AI - GDC Vault, https://gdcvault.com/play/1012744/Behavior-Trees-Three-Ways-of 9. Goal-Oriented Action Planning: Ten Years Old and No Fear! - GDC Vault, https://www.gdcvault.com/play/1022019/Goal-Oriented-Action-Planning-Ten 10. The A.I. of F.E.A.R. Paper(GDC 2006) : r/gamedev - Reddit, https://www.reddit.com/r/gamedev/comments/8zaybb/the_ai_of_fear_papergdc_2006/ 11. Building the AI of F.E.A.R. with Goal Oriented Action Planning | AI 101 - YouTube, https://www.youtube.com/watch?v=PaOLBOuyswI 12. Game AI Summit: Combining GOAP and MBTs to Create NPCs' Behaviors for 'Kingdom Come: Deliverance II' - GDC Vault, https://gdcvault.com/play/1035576/Game-AI-Summit-Combining-GOAP 13. Behind The AI of Horizon Zero Dawn (Part 1) - Game Developer, https://www.gamedeveloper.com/design/behind-the-ai-of-horizon-zero-dawn-part-1- 14. Behind The AI of Horizon Zero Dawn (Part 2) - Game Developer, https://www.gamedeveloper.com/design/behind-the-ai-of-horizon-zero-dawn-part-2- 15. HTN Planning in Decima - Guerrilla Games, https://www.guerrilla-games.com/read/htn-planning-in-decima 16. Example HTN Planner: Pyhop, http://ozark.hendrix.edu/~ferrer/courses/335/f13/lectures/htnPlanning.html 17. Decima - Guerrilla Games, https://www.guerrilla-games.com/tags?jsonPath=TaxonomyPart.Terms%5B4%5D&before=638268441000000000 18. The AI Systems of Left 4 Dead - Akamaihd.net, https://steamcdn-a.akamaihd.net/apps/valve/2009/ai_systems_of_l4d_mike_booth.pdf 19. Replayable Cooperative Game Design: Left 4 Dead, https://cdn.fastly.steamstatic.com/apps/valve/2009/GDC2009_ReplayableCooperativeGameDesign_Left4Dead.pdf 20. 11 Secrets about LEFT 4 DEAD's AI Director and its Procedural Zombie Population | AiGameDev.com, https://www.cs.drexel.edu/~santi/teaching/2012/CS680/papers/11%20Secrets%20about%20LEFT%204%20DEAD%E2%80%99s%20AI%20Director%20and%20its%20Procedural%20Zombie%20Population%20%7C%20AiGameDev.com.pdf 21. Old GDC talk now public - Left 4 Dead's simple AI driven dialog system explained - Reddit, https://www.reddit.com/r/gamedev/comments/bdr1e5/old_gdc_talk_now_public_left_4_deads_simple_ai/ 22. Anyone remember the AI creature learning in Black & White (1&2)? Has any other game compare or surpass that level of AI? - Reddit, https://www.reddit.com/r/pcgaming/comments/8r7nmv/anyone_remember_the_ai_creature_learning_in_black/ 23. Black & White: A Game of Reinforcement Learning | by Rishab Borah - Medium, https://rishabnborah.medium.com/black-white-a-game-of-reinforcement-learning-3e0eacab936 24. The Creature A.I. of Black and White - SomeGamez, https://somegamez.com/wit/creature-ai-black-and-white 25. We, as an industry, need to focus on more human-like video game AI. : r/truegaming - Reddit, https://www.reddit.com/r/truegaming/comments/dawjyy/we_as_an_industry_need_to_focus_on_more_humanlike/ 26. Continuous World Generation in 'No Man's Sky' - GDC Vault, https://www.gdcvault.com/play/1024265/Continuous_World_Generation_in__No_Man_s_Sky_ 27. Building Worlds in No Man's Sky Using Math(s) - YouTube, https://www.youtube.com/watch?v=C9RyEiEzMiU 28. How Townscaper Works: A Story Four Games in the Making, https://www.gamedeveloper.com/game-platforms/how-townscaper-works-a-story-four-games-in-the-making 29. This uses the "wave function collapse" algorithm. Oskar Stalberg also made a gre... | Hacker News, https://news.ycombinator.com/item?id=29410695 30. mxgmn/WaveFunctionCollapse: Bitmap & tilemap generation from a single example with the help of ideas from quantum mechanics - GitHub, https://github.com/mxgmn/WaveFunctionCollapse 31. EPC2018 | Wave Function Collapse in Bad North | Oskar Stalberg - YouTube, https://www.youtube.com/watch?v=0bcZb-SsnrA 32. Unlocking the Potential of Generative AI through Neuro-Symbolic Architectures – Benefits and Limitations - arXiv, https://arxiv.org/html/2502.11269v1 33. Neuro-symbolic AI - Wikipedia, https://en.wikipedia.org/wiki/Neuro-symbolic_AI 34. Tencent Games to Showcase Latest Tech at the GDC 2024, https://www.tencent.com/en-us/articles/2201793.html 35. Tencent provided insights into new technologies and innovations | Gamelight, https://www.gamelight.io/news/tencent-provided-insights-into-new-technologies-and-innovations 36. Ubisoft La Forge News, https://www.ubisoft.com/en-us/studio/laforge/news 37. Generative AI in game development - Arm Community, https://developer.arm.com/community/arm-community-blogs/b/mobile-graphics-and-gaming-blog/posts/generative-ai-game-development 38. Who speaks next? Multi-party AI discussion leveraging the systematics of turn-taking in Murder Mystery games - Frontiers, https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2025.1582287/full 39. LLM Reasoner and Automated Planner: A new NPC approach - arXiv, https://arxiv.org/html/2501.10106v1 40. Narrative-Driven Generation: Story to Game World using LLMs | AI and Games Conference 2024 - YouTube, https://www.youtube.com/watch?v=Kf0a7q4q2VY 41. py-trees - PyPI, https://pypi.org/project/py-trees/ 42. Hands-On Py Trees — Part 1 - Medium, https://medium.com/@thehummingbird/hands-on-py-trees-part-1-1df1910128e4 43. flags/GOAPy: Pure-Python implementation of Goal-Oriented Action Planning. - GitHub, https://github.com/flags/GOAPy

**

**

# ゲーム開発における数学的・工学的基盤の深化：3年制専門課程のための包括的カリキュラムと実装戦略

## エグゼクティブサマリー

現代のゲーム開発教育は重大な岐路に立たされています。一方ではUnityやUnreal Engineといった商用エンジンの普及により、ゲーム制作の民主化が進み、初学者でも容易にリッチなコンテンツを作成できるようになりました。しかし、その一方で、エンジンの機能をブラックボックスとして扱う「オペレーター」的な技能にとどまり、その背後にある数学的原理やアルゴリズムの深層構造を理解しないまま卒業する学生が増加しているという課題も浮き彫りになっています。

本報告書は、ゲーム専門学校における3年制の「ゲームエンジニアリング・スペシャリストコース」を想定し、既存のツールを使用するだけでなく、それらを「自作」する過程を通じて、数学的・アカデミックなアプローチ（AI、物理、PCG等）を体系的に習得するための網羅的カリキュラムを提案します。本提案は、有限ステートマシン（FSM）から階層型タスクネットワーク（HTN）、そして最新のニューロシンボリックAIに至る技術の歴史的変遷と実応用（『F.E.A.R.』、『Horizon Zero Dawn』、『Townscaper』等）を紐解きながら、学生が自らの手で物理エンジンやAIプランナーを設計・実装することの教育的意義と実現可能性を論じます。

この「グラスボックス（Glass Box）」アプローチは、学生に対し、単なる実装力だけでなく、システムの挙動を予測し制御するための「メンタルモデル」を構築させ、将来的にAAAタイトルのコアシステム開発や、未知の技術トレンド（生成AIとシンボリックAIの融合等）に適応できる真のエンジニアリング能力を養成することを目的としています。

## 第1部：教育哲学と工学的アプローチ

### 1.1 「車輪の再発明」の教育的価値とシステム思考

ソフトウェアエンジニアリングの現場において、「車輪の再発明（既存のライブラリがあるにもかかわらず、自ら同様の機能を作成すること）」は生産性の観点から忌避される傾向にあります。しかし、教育的文脈、特に高度な専門職を育成する過程において、この格言は逆転します。既存の物理エンジンやAIライブラリをブラックボックスとして利用するだけでは、その内部で発生している数値計算の不安定性や、メモリ管理の複雑さ、アルゴリズムの計算量オーダー（Big O notation）の実感を伴った理解には到達し得ないからです。

例えば、物理エンジンを自作する過程で、学生は数値積分におけるオイラー法の誤差がどのようにゲーム内の「オブジェクトの振動」として現れるかを体験します。この失敗体験こそが、将来商用エンジンを使用した際に遭遇する物理バグの原因を直感的に特定する能力、すなわち「メンタル物理エンジン」の形成に寄与します。NASAの教育プログラム「The Stellar Story」においても、既存の解決策を適応させる能力と同時に、基礎的な構成要素を深く理解することの重要性が強調されており、エンジニアリング教育における「根本からの構築」は、システム全体を俯瞰し、要素間の相互作用を理解する「システム思考（Systems Thinking）」を養うために不可欠です。

### 1.2 数学的リテラシーと「学術的」ゲーム開発

本カリキュラムでは、ゲーム開発を「応用数学の実践」と定義します。AIの行動決定はグラフ理論と述語論理の応用であり、物理シミュレーションは微分方程式の数値解法であり、プロシージャルコンテンツ生成（PCG）は確率論と制約充足問題（CSP）の視覚化です。

多くの専門学校カリキュラムでは、数学を「ゲームプログラミングのための数学」として断片的に教える傾向がありますが、本提案では数学を「エンジンの仕様を決定する言語」として扱います。例えば、線形代数を学ぶことは、単にキャラクターを動かすためではなく、独自のレンダリングパイプラインや衝突判定アルゴリズムを設計するための基礎として位置づけられます。これにより、学生は『Killzone 2』におけるインフルエンスマップや、『Bad North』におけるWave Function Collapse（波動関数の崩壊）アルゴリズムといった、高度な数学的概念を要する技術に対しても、基礎原理からアプローチする力を身につけることができます。

## 第2部：3年制カリキュラムの詳細設計

本カリキュラムは、基礎から応用、そして最先端技術への統合を目指す3段階のフェーズで構成されています。各学年は明確なテーマを持ち、数学的理論の学習と、それを実装するライブラリ制作プロジェクトが並行して進行します。

### 1年次：決定論的システムと数学的基礎

テーマ： 「世界の法則を記述する」 目標： 数学（線形代数・解析学）の基礎を固め、決定論的な挙動を示すシステム（物理エンジン、基礎AI）をゼロから実装する。

#### 第1セメスター：空間と運動の数学

この学期では、ゲーム世界を構成する「空間」と、その中での「運動」を数学的に定義することに集中します。商用エンジンは一切使用せず、C++またはPythonを用いて、描画ライブラリ（SDLやSFML、またはPyGame）のみを使用した環境で開発を行います。

- モジュール1.1：線形代数と座標系
    

- 講義内容： ベクトル空間、基底、行列演算（積、転置、逆行列）、アフィン変換、クォータニオン。
    
- アカデミックな視点： 3Dグラフィックスにおける「ワールド変換」「ビュー変換」「プロジェクション変換」を行列計算として手動で実装し、GPUが内部で行っている計算プロセスを理解します。
    
- 演習課題： エンジンに頼らない2Dレンダラーの実装。行列スタックを用いた階層構造（親子関係）の構築。
    

- モジュール1.2：微積分と数値積分
    

- 講義内容： ニュートンの運動方程式、微分方程式の離散化、数値積分法（オイラー法、シンプレクティックオイラー法、ベレ法、ルンゲ・クッタ法）。
    
- 実応用： 『Pong』のような単純な反射から、『アングリーバード』のような弾道計算への進化。
    
- プロジェクトA：剛体物理エンジンの自作（Physics Engine 1.0）
    

- 学生はPythonまたはC++を用いて、独自の2D物理エンジンを構築します。
    
- 要件：
    

- 質量（Mass）と力（Force）、加速度（Acceleration）を管理するBodyクラスの実装。
    
- 固定タイムステップ（Fixed Timestep）によるゲームループの実装。
    
- 重力と空気抵抗のシミュレーション。
    

#### 第2セメスター：衝突と状態遷移

物理的な干渉と、キャラクターの基本的な意思決定（ステートマシン）を扱います。

- モジュール2.1：衝突判定のアルゴリズム（幾何学）
    

- 講義内容： 衝突検出（Collision Detection）におけるブロードフェーズとナローフェーズ。
    
- アルゴリズム詳細：
    

- 分離軸判定法（SAT: Separating Axis Theorem）： 凸多角形同士の衝突判定における数学的基礎。法線ベクトルの射影を用いた判定ロジック。
    
- GJKアルゴリズム（Gilbert-Johnson-Keerthi）： ミンコフスキー和を用いた、より汎用的かつ高速な衝突判定手法。
    

- 実装課題： 自作物理エンジンへの衝突判定システムの実装。AABB（軸平行境界ボックス）によるブロードフェーズ最適化（四分木の実装）。
    

- モジュール2.2：オートマトンと有限ステートマシン（FSM）
    

- 講義内容： オートマトン理論、決定性有限オートマトン（DFA）、Mealy型とMoore型マシン。
    
- 歴史的実応用：
    

- 『パックマン』（1980）： ゴーストのAI（「追いかけ」「待ち伏せ」「逃走」）の分析。単純なルールベースAIがどのように複雑な挙動に見えるかの検証。
    
- 『スーパーマリオブラザーズ』： 敵キャラクターの状態遷移（パトロール→発見→攻撃）。
    

- プロジェクトB：FSMライブラリの構築
    

- switch文によるスパゲッティコードを脱却し、Stateパターン（GoFデザインパターン）を用いたオブジェクト指向的なFSMライブラリを実装します。これにより、状態の追加・削除が容易な拡張性の高いAIアーキテクチャを学びます。
    

### 2年次：自律性とプランニング、アーキテクチャ

テーマ： 「エージェントに知能を与える」 目標： 反応的なAI（FSM）から、目的指向的・計画的なAI（GOAP, HTN）への移行。複雑なシステムを管理するためのアーキテクチャ設計。

#### 第3セメスター：探索と意思決定の構造化

エージェントが環境を認識し、最適な行動を選択するためのアルゴリズムを学びます。

- モジュール3.1：グラフ理論と経路探索
    

- 講義内容： グラフデータ構造（ノード、エッジ、重み）、幅優先探索（BFS）、ダイクストラ法、A*アルゴリズム、ヒューリスティック関数の設計。
    
- アカデミックな視点： 経路探索を単なる移動手段としてではなく、「状態空間における探索」として抽象化して捉える視点の導入。これは後のGOAPの理解に直結します。
    
- 実応用： ナビゲーションメッシュ（NavMesh）の生成原理と、動的な障害物回避。
    

- モジュール3.2：ビヘイビアツリー（Behavior Trees: BT）
    

- 講義内容： ツリー構造による意思決定、装飾ノード（Decorators）、複合ノード（Composites: Sequence, Selector）、ブラックボード（データ共有）アーキテクチャ。
    
- 歴史的実応用：
    

- 『Halo 2』（2004）： Bungie社がFSMの限界（状態爆発問題）を解決するために大規模に導入した事例。
    
- 『Project Zomboid』： 複雑なNPCの生存行動を管理するためのJavaによる実装事例。
    

- プロジェクトC：ビヘイビアツリー・エディタとランタイムの実装
    

- XMLやJSONで記述されたツリー構造を読み込み、実行時にノードをトラバースするライブラリを作成します。視覚的なデバッグ環境の重要性についても学びます。
    

#### 第4セメスター：プランニングと効用理論

あらかじめ決められた行動ツリーを辿るのではなく、エージェント自身が目標を達成するためのプランを動的に生成する技術を学びます。

- モジュール4.1：ゴール指向アクションプランニング（GOAP）
    

- 講義内容： STRIPSプランニング、前提条件（Preconditions）と効果（Effects）、逆方向探索（Backward Chaining）。
    
- 歴史的実応用：
    

- 『F.E.A.R.』（2005）： Jeff Orkinによる画期的なAI。敵兵士が「テーブルを倒して遮蔽物にする」といった行動を、スクリプトではなく「遮蔽物が必要」というゴールから動的に導き出す仕組み。
    

- 実装課題： 「World State」をビットマスク等で効率的に管理し、A*アルゴリズムを用いてアクションの連鎖を計画するGOAPプランナーの実装。
    

- モジュール4.2：階層型タスクネットワーク（HTN）
    

- 講義内容： タスクの階層的分解（Decomposition）、プリミティブタスクとコンパウンドタスク。
    
- 歴史的実応用：
    

- 『Horizon Zero Dawn』・『Killzone』シリーズ： 機械獣や兵士が、戦術的なドクトリン（高レベルな方針）に従いつつ、具体的な行動（低レベルな移動・攻撃）を実行するためのHTNの活用事例。
    
- 『Transformers: Fall of Cybertron』： 変形（トランスフォーム）を含む複雑なアクションシークエンスの制御。
    

- モジュール4.3：ユーティリティAI（Utility AI）
    

- 講義内容： 効用関数（Utility Function）、ファジィ論理、ニーズベースの意思決定。
    
- 歴史的実応用：
    

- 『The Sims』シリーズ： 「空腹」「社交」などのニーズパラメータに基づき、オブジェクトが提供する「広告（Advertisement）」スコアを評価して行動を決定する「Smart Object」アーキテクチャ。
    

### 3年次：プロシージャル技術、最適化、そして未来

テーマ： 「創造性と効率性の融合」 目標： 数学的アルゴリズムを用いたコンテンツ生成（PCG）、最新のAIトレンド（ニューロシンボリックAI）、およびハードウェア性能を引き出す最適化技術の習得。

#### 第5セメスター：プロシージャルコンテンツ生成（PCG）

手作業によるレベルデザインから、アルゴリズムによる自動生成への拡張。

- モジュール5.1：ノイズとカオス理論
    

- 講義内容： 擬似乱数生成器（PRNG）、パーリンノイズ、シンプレックスノイズ、フラクタル（自己相似性）。
    
- 実応用： 『Minecraft』等に見られる地形生成。ノイズ関数を重ね合わせる（オクターブ）ことによる自然な地形の合成。
    

- モジュール5.2：セルオートマトンとL-System
    

- 講義内容： コンウェイのライフゲーム、ルールベースの反復処理、文字列書き換えシステム。
    
- 実応用： 洞窟の生成（セルオートマトン）、植生や樹木の生成（L-System）。
    

- モジュール5.3：波動関数の崩壊（Wave Function Collapse: WFC）
    

- 講義内容： 量子力学に着想を得た制約充足アルゴリズム。エントロピー最小化によるタイルの決定プロセス。
    
- 歴史的実応用：
    

- 『Townscaper』・『Bad North』： オスカー・スタルバーグ（Oskar Stålberg）による、不規則なグリッド上でのWFCの実装により、美しく整合性の取れた街並みや島を生成する技術。
    

- プロジェクトD：WFCによるレベルジェネレーター
    

- 入力されたサンプル（プロトタイプ）からルールを学習し、無限のマップを生成するソルバーの実装。
    

#### 第6セメスター：次世代AIとシステム最適化

卒業制作に向けた、最先端技術の統合とパフォーマンスチューニング。

- モジュール6.1：データ指向設計（Data-Oriented Design: DOD）とECS
    

- 講義内容： オブジェクト指向プログラミング（OOP）の弊害（キャッシュミス）、CPUキャッシュアーキテクチャ、AoS（Array of Structs）とSoA（Struct of Arrays）、Entity Component System（ECS）。
    
- 実応用： 大量のユニットを描画・更新する際のパフォーマンス向上。UnityのDOTSやUnrealのMass Entityへの理解。
    

- モジュール6.2：ニューロシンボリックAIとLLMの融合
    

- 講義内容： ニューラルネットワーク（学習・パターン認識）とシンボリックAI（論理・計画）の統合。大規模言語モデル（LLM）を「推論エンジン」や「ヒューリスティック生成器」として利用するアプローチ。
    
- 最新トレンド（GDC 2025/2026）：
    

- LLM-A：* A*探索のヒューリスティック関数としてLLMを使用し、意味的なコンテキストを考慮した経路探索を行う研究。
    
- 生成AIによるNPC制御： 自然言語での指示をビヘイビアツリーのパラメータや構造に変換するフレームワーク。
    

- 実応用： TencentやNetEaseなどの大手企業が進める、強化学習（RL）と従来のゲームAIのハイブリッドシステム。
    

## 第3部：主要技術の歴史的変遷と詳細解説

本セクションでは、カリキュラムの中核となるAIアルゴリズムについて、その歴史的背景、技術的詳細、および現代のゲーム開発における位置づけを深掘りします。

### 3.1 有限ステートマシン（FSM）から階層化への進化

#### 技術的詳細

FSMは、エージェントが取りうる「状態（State）」と、状態間の「遷移（Transition）」、そして遷移を引き起こす「条件（Condition）」の集合で定義されます。数学的には有向グラフとして表現され、現在の状態から次の状態への移動は決定論的に処理されます。

#### 歴史的文脈と課題

1980年代のアーケードゲーム（『パックマン』等）では、FSMは完璧に機能しました。しかし、ゲームが複雑化するにつれ、状態の数は指数関数的に増加しました（「状態爆発」）。例えば、単なる「攻撃」状態でも、「立って攻撃」「しゃがんで攻撃」「移動しながら攻撃」など無数のバリエーションが必要となり、それら全ての間の遷移を管理することは人間の認知限界を超え、バグの温床（スパゲッティコード）となりました。

#### 階層型有限ステートマシン（HFSM）

この問題を解決するために導入されたのがHFSMです。HFSMでは、複数の関連する状態（例：「パトロール」「待機」「調査」）を一つの親状態（「非戦闘モード」）にカプセル化します。これにより、上位レベルの状態遷移と下位レベルの挙動を分離し、再利用性と可読性を向上させました。『アサシン クリード』初期作などのアクションゲームで広く採用されました。

### 3.2 ビヘイビアツリー（BT）：モジュール性と可読性の革命

#### 技術的詳細

BTは、状態遷移ではなく「タスクの実行」に焦点を当てたツリー構造です。ルートノードから深さ優先探索（DFS）でノードを評価し、各ノードは「成功（Success）」「失敗（Failure）」「実行中（Running）」のいずれかのステータスを親に返します。

- Composite（複合）ノード:
    

- Sequence（シーケンス）: 子ノードを順番に実行し、全て成功したら成功を返す（AND論理）。
    
- Selector（セレクター）: 子ノードを順番に実行し、一つでも成功したら成功を返す（OR論理）。
    

- Decorator（装飾）ノード: 子ノードの結果を反転（Inverter）させたり、繰り返し実行（Repeater）させたりする。
    
- Leaf（葉）ノード: 実際のゲームロジック（「敵が見えるか？」という条件判定や、「移動する」というアクション）を実行する。
    

#### 歴史的実応用：『Halo 2』の衝撃

2004年、BungieのDamian Islaらは『Halo 2』においてBT（当時はまだその名称が定着していなかったものの、概念的に同等のもの）を大規模に採用しました。コヴナント（敵エイリアン）の複雑な連携や状況判断を、デザイナーが視覚的に調整可能なツリーとして表現することで、プログラマーの手を借りずにAIの挙動を調整できるパイプラインを確立しました。現在ではUnreal Engineの標準AIシステムとして採用されており、業界のデファクトスタンダードとなっています。

### 3.3 ゴール指向アクションプランニング（GOAP）：自律性の獲得

#### 技術的詳細

GOAPは、スタンフォード研究所で開発されたSTRIPS（Stanford Research Institute Problem Solver）プランニングをリアルタイムゲーム向けに軽量化したものです。

- 世界表現: 世界の状態をブール値や列挙型の集合（アトム）で表現します（例：HasWeapon=True, IsTargetDead=False）。
    
- アクション定義: 各アクションは、実行に必要な「前提条件（Preconditions）」と、実行後の「効果（Effects）」を持ちます。
    

- アクション「リロード」: 前提 HasAmmo=True, 効果 WeaponLoaded=True
    

- プランニング処理: エージェントは「ゴール（例：IsTargetDead=True）」を与えられると、現在の世界状態からゴールに至るアクションの連鎖（プラン）を、A*アルゴリズムを用いて逆算（または順方向探索）して構築します。
    

#### 歴史的実応用：『F.E.A.R.』の遺産

2005年のFPS『F.E.A.R.』は、GOAPの実用性を世界に知らしめました。敵兵士は「プレイヤーを倒す」というゴールのために、状況に応じて「遮蔽物に隠れる」「窓を割って飛び降りる」「棚を倒して遮蔽物を作る」といった行動を動的に組み合わせることができました。FSMのように「窓を割ったら飛び降りる」という遷移を明示的に書く必要がなく、環境にあるオブジェクトのアフォーダンスを利用して創発的な挙動を生み出せる点が革新的でした。

### 3.4 階層型タスクネットワーク（HTN）：ドクトリンと表現力

#### 技術的詳細

HTNは、GOAPと同じくプランニング技術の一種ですが、アプローチが異なります。GOAPがアクションの連鎖（Chain）を作るのに対し、HTNはタスクの分解（Decomposition）を行います。

- Compound Task（複合タスク）: 高レベルの抽象的な命令（例：「基地を制圧せよ」）。これ自体は直接実行できません。
    
- Method（メソッド）: 複合タスクを達成するための具体的な手順の候補（例：「正面突破プラン」または「裏口潜入プラン」）。
    
- Primitive Task（プリミティブタスク）: これ以上分解できない、実行可能なアクション（例：「移動」「発砲」）。
    

プランナーは、現在の状況に適用可能なメソッドを選択し、タスクを再帰的に分解していくことで、実行可能なプランを生成します。

#### 歴史的実応用：『Horizon Zero Dawn』と『Killzone』

Guerrilla Gamesは、HTNの強力な支持者です。『Killzone 2』や『Horizon Zero Dawn』では、機械獣や敵兵士の統率された動きを実現するためにHTNが採用されました。HTNの最大の利点は、デザイナーが「ドクトリン（戦術思想）」をAIに強制できる点です。GOAPは「最短でゴールを目指す」ため、時に人間らしくない（あるいは賢すぎる）行動をとる可能性がありますが、HTNは「まず警報を鳴らし、次に援護射撃を行い、その間に突撃兵が前進する」といった軍事的な手順を忠実に再現するのに適しています。

## 第4部：物理シミュレーションと数値計算の深淵

物理エンジンの自作は、本カリキュラムにおいて最も数学的密度が高い領域です。

### 4.1 数値積分とシミュレーションの安定性

物理シミュレーションの核となるのは、時間経過に伴う位置と速度の更新（積分）です。

- オイラー法（Euler Integration）: x_{t+1} = x_t + v_t \Delta t。最も単純ですが、誤差が累積しやすく、エネルギー保存則が満たされないため、バネや軌道のシミュレーションでは発散（爆発）しやすいという問題があります。
    
- シンプレクティック積分（Symplectic Integration）: エネルギー保存則を考慮した積分法（セミインプリシットオイラー法やベレ法）。ゲーム物理では、計算コストと安定性のバランスから、これらが好まれます。
    
- ルンゲ・クッタ法（RK4）: 高精度ですが計算コストが高く、リアルタイムゲームでの剛体物理にはオーバースペックとなる場合が多いです。しかし、このトレードオフを理解することが重要です。
    

### 4.2 衝突検出（Collision Detection）のアルゴリズム

- ブロードフェーズ（Broad Phase）: 全てのオブジェクト総当りで判定を行うと O(N^2) の計算量となり、破綻します。空間分割（四分木、八分木、BSP、BVH）や、スイープ＆プルーン（Sweep and Prune）アルゴリズムを用いて、計算量を O(N \log N) 程度に削減する手法を学びます。
    
- ナローフェーズ（Narrow Phase）:
    

- GJKアルゴリズム: 凸形状同士の距離計算において、ミンコフスキー差（Minkowski Difference）という概念を利用します。2つの凸形状 A と B が衝突していることは、そのミンコフスキー差 A - B が原点を含んでいることと同義です。GJKは、シンプレックス（単体）を反復的に更新しながら原点への最接近点を探索する、非常にエレガントかつ高速なアルゴリズムです。
    

## 第5部：ライブラリ自作の実現可能性と教育的意義

### 5.1 実現可能性：3年間という時間枠

個人で商用レベルの汎用エンジン（Unity等）を作ることは不可能に近いですが、特定の機能に特化したライブラリ（2D物理エンジン、GOAPプランナー等）を作成することは、3年間のカリキュラムにおいて十分に実現可能です。

- 言語の選択: Pythonはプロトタイピングや概念実証に優れており、最初のFSMやGOAPの実装に適しています（GOAPyやPymunkなどの既存ライブラリを参考にできるため）。しかし、パフォーマンスが要求される物理エンジンや高度なPCG（WFC等）においては、C++とメモリ管理の知識が不可欠となります。本カリキュラムでは、1年次にPythonでアルゴリズムの論理を理解し、2-3年次にC++で高速化・最適化を行う「二段階アプローチ」を推奨します。
    

### 5.2 教育的意義：なぜ「車輪の再発明」が必要なのか

1. ブラックボックスの解体: 商用エンジンのAPI（例：NavMeshAgent.SetDestination()）を叩くだけでは、その裏でどのような計算が行われているか（A*、パススムージング、ステアリング挙動）を理解できません。自作することで、エンジンの挙動に対する深い洞察が得られ、トラブルシューティング能力が飛躍的に向上します。
    
2. 応用力と転移性: HTNやGOAPのロジックは、ゲームAIに限らず、ロボット工学や業務プロセスの自動化にも応用可能です。ECSによるデータ指向設計の知識は、大規模なデータ処理を伴うあらゆるソフトウェア開発において有用です。
    
3. システムエンジニアリング能力: 複数のコンポーネント（レンダリング、物理、AI、入力）を統合し、一つの整合性のあるシステムとして動作させる経験は、大規模なソフトウェアアーキテクチャを設計する能力（システムズエンジニアリング）を養います。
    

## 第6部：最新技術トレンドへの接続（GDC 2025/2026）

カリキュラムの最終段階では、これまでに学んだ「古典的」な技術と、現在進行形のAI革命を融合させます。

### 6.1 ニューロシンボリックAI

ニューロシンボリックAIは、ニューラルネットワーク（深層学習）の学習能力・汎化能力と、シンボリックAI（論理・ルールベース）の推論能力・説明可能性を組み合わせるアプローチです。

- 教育的アプローチ: 学生は、自作したビヘイビアツリー（シンボリックAI）のノード選択ロジックの一部に、強化学習（RL）やLLM（ニューラルAI）を組み込む実験を行います。
    
- LLMをプランナーとして利用: LLMに自然言語で「状況」と「利用可能なアクション」を入力し、ゴール達成のためのプラン（アクションの順序）を出力させ、それを従来のGOAP/HTNシステムで検証・実行するハイブリッドシステムの研究が進んでいます。
    

### 6.2 生成AIとゲーム開発

NetEaseやTencentなどの巨大テック企業は、強化学習を用いたゲームバランス調整や、生成AIによる3Dアセット制作パイプラインの構築に多大な投資を行っています。本カリキュラムで学ぶ「PCG（WFC等）」の知識は、生成AIが出力した結果をゲーム内で利用可能な形式に変換・修正するための「制約」として機能させる際に重要となります。

## 結論

本報告書で提案したカリキュラムは、単に「ゲームが作れる」人材ではなく、「ゲーム技術を作れる」エンジニアの育成を目的としています。物理法則の数値化、意思決定の論理構造化、そしてプロシージャルな創造性のアルゴリズム化——これら数学的・工学的アプローチの習得は、ツールがどれほど進化しようとも陳腐化することのない、普遍的なエンジニアリング能力の土台となります。学生たちは、先人たちが築き上げたアルゴリズムの歴史（FSMからHTN、そしてニューロシンボリックへ）を自らの手で再構築（Reinvent）することで、次世代のゲーム産業を牽引するイノベーターとしての資質を獲得するでしょう。

### 表1：主要なAI意思決定アルゴリズムの比較と特性

|アルゴリズム|基本メカニズム|長所（Pros）|短所（Cons）|代表的な採用タイトル|適した用途|
|---|---|---|---|---|---|
|FSM (有限ステートマシン)|状態遷移図に基づく決定論的遷移|実装が容易、デバッグしやすい、挙動が予測可能|状態数が増えると複雑化し管理不能になる（スパゲッティコード）|『パックマン』、『スーパーマリオ』|シンプルな敵、UIフロー、ドア等のオブジェクト制御|
|HFSM (階層型FSM)|状態のネスト（親状態・子状態）化|FSMの再利用性が向上、構造化が可能|本質的な「遷移の複雑さ」は解決しきれない|『アサシン クリード』初期作|アクションゲームのコンボシステム、中規模なAI|
|Behavior Trees (BT)|ツリー構造の走査（Task Execution）|モジュール性が高い、デザイナーが調整しやすい、拡張性が高い|ツリーが深くなりすぎると毎フレームの評価コストが増大する|『Halo 2』、『Project Zomboid』、『Unreal Engine』標準|FPSの敵、複雑な判断を要するNPC、現在の業界標準|
|GOAP (ゴール指向アクションプランニング)|逆方向A*探索によるプラン生成|状況に応じた創発的な行動、事前の遷移定義が不要|計算コストが高い、デバッグが難しい（なぜそのプランを選んだか直感的に分かりにくい）|『F.E.A.R.』、『Deus Ex』|ステルスゲーム、予測不能な環境での自律エージェント|
|HTN (階層型タスクネットワーク)|タスクの分解によるプラン生成|ドクトリン（戦術）を反映しやすい、長期的・複雑な計画が可能|ドメイン知識（タスク分解ルール）の記述コストが高い|『Horizon Zero Dawn』、『Killzone 2』|軍事シミュレーション、戦術的な分隊行動、RTS|
|Utility AI (効用ベースAI)|数値スコアリングによる確率的選択|非常に有機的で「人間らしい」曖昧な選択が可能、設計が柔軟|調整（カーブの設定）が難しく、意図した挙動に収束させるのが困難|『The Sims』、『Civilization』|シミュレーションゲーム、RPGのNPC、群衆シミュレーション|

### 表2：物理エンジン開発ロードマップ（1-2年次）

|コンポーネント|必要な数学・物理概念|実装の詳細ポイント|学習リソース/参照|
|---|---|---|---|
|ベクトル・行列演算|線形代数、内積・外積|ベクトルクラス、行列クラス（3x3, 4x4）、クォータニオンの実装|3Dグラフィックス基礎|
|積分（Integration）|微積分、数値解析|オイラー法（不安定性の確認）→ ベレ法またはRK4の実装||
|ブロードフェーズ|空間分割アルゴリズム|総当り（O(N^2)）からの脱却。四分木（Quadtree）または動的AABBツリーの実装||
|ナローフェーズ|凸解析、幾何学|GJKアルゴリズム（ミンコフスキー差）とEPA（貫通深度計算）の実装||
|制約ソルバー|連立一次方程式、ヤコビ行列|逐次インパルス法（Sequential Impulse）。摩擦、反発係数、ジョイントの解決||

### 表3：プロシージャルコンテンツ生成（PCG）技術体系

| 技術カテゴリ | アルゴリズム例 | 数学的背景 | 応用例 | 代表的タイトル | | :--- | :--- | :--- | :--- | :--- | | ノイズ生成 | Perlin Noise, Simplex Noise | 勾配ベクトル、補間、擬似乱数 | 地形生成、雲のテクスチャ、揺らぎ | 『Minecraft』 | | セルオートマトン | Game of Life, Cellular Automata | 離散数学、グリッド近傍計算 | 洞窟生成、流体シミュレーション（簡易）、生態系 | 各種ローグライクゲーム | | 文法ベース生成 | L-System | 形式言語理論、書き換え規則、再帰 | 樹木、植物、道路網の生成 | プロシージャル植物生成ツール | | 制約充足 | Wave Function Collapse (WFC) | 量子力学（重ね合わせ）、エントロピー、グラフ理論 | 建物、ダンジョン、島の生成、テクスチャ合成 | 『Townscaper』、『Bad North』 |

#### 引用文献

1. (PDF) Building a Scalable Game Engine to Teach Computer Science Languages, https://www.researchgate.net/publication/282904188_Building_a_Scalable_Game_Engine_to_Teach_Computer_Science_Languages 2. Mind Games: Game Engines as an Architecture for Intuitive Physics - Harvard University, https://klab.tch.harvard.edu/academia/classes/BAI/pdfs/UllmanEtAl_TICS2017.pdf 3. Reinvent The Wheel! - ircmaxell's Blog, https://blog.ircmaxell.com/2012/08/reinvent-wheel.html 4. System Thinking in Game Design - Proceedings, https://proceedings.systemdynamics.org/2024/papers/P1159.pdf 5. Master Thesis Computer Science Thesis no: MCS-2013-06 June 2013 Using Multicore Programming on the GPU to Improve Creation of Po - DiVA portal, https://www.diva-portal.org/smash/get/diva2:833037/FULLTEXT01.pdf 6. Procedural Content Generation for video games, a friendly approach, https://www.levelup-gamedevhub.com/en/news/procedural-content-generation-for-video-games-a-friendly-approach/ 7. The Evolution of Game Physics Engines: From Basic Collision to Realistic Simulations |, https://happywheelsmore.org/the-evolution-of-game-physics-engines-from-basic-collision-to-realistic-simulations/ 8. Pymunk — Pymunk documentation, http://www.pymunk.org/ 9. Build a simple 2D physics engine for JavaScript games - IBM Developer, https://developer.ibm.com/tutorials/wa-build2dphysicsengine/ 10. Collision detection - Wikipedia, https://en.wikipedia.org/wiki/Collision_detection 11. Game Physics - CNRS, https://perso.liris.cnrs.fr/npronost/UUCourses/GamePhysics/lectures/lecture%207%20Collision%20Resolution.pdf 12. Decision-making AI in digital games - Diva-portal.org, https://www.diva-portal.org/smash/get/diva2:1673140/FULLTEXT01.pdf 13. An intelligent agent of finite state machine in educational game “Flora the Explorer”, https://www.researchgate.net/publication/337078490_An_intelligent_agent_of_finite_state_machine_in_educational_game_Flora_the_Explorer 14. Finite State Machines - Game Manual 0, https://gm0.org/en/latest/docs/software/concepts/finite-state-machines.html 15. LLM-A*: Large Language Model Enhanced Incremental Heuristic Search on Path Planning - ACL Anthology, https://aclanthology.org/2024.findings-emnlp.60.pdf 16. Game AI Pro - Behavior Selection Algorithms, http://www.gameaipro.com/GameAIPro/GameAIPro_Chapter04_Behavior_Selection_Algorithms.pdf 17. Behavior trees for AI: How they work - Game Developer, https://www.gamedeveloper.com/programming/behavior-trees-for-ai-how-they-work 18. Tech Breakdown: AI with Finite State Machines - Little Polygon Game Dev Blog, https://blog.littlepolygon.com/posts/fsm/ 19. flags/GOAPy: Pure-Python implementation of Goal-Oriented Action Planning. - GitHub, https://github.com/flags/GOAPy 20. stolk/GPGOAP: General Purpose Goal Oriented Action Planning - GitHub, https://github.com/stolk/GPGOAP 21. DEVELOPING AN HTN PLANNER FOR VIRTUAL ECOSYSTEMS - UPCommons, https://upcommons.upc.edu/bitstreams/b49b2cc6-45b8-483b-9561-378272467fad/download 22. Behind The AI of Horizon Zero Dawn (Part 1) - Game Developer, https://www.gamedeveloper.com/design/behind-the-ai-of-horizon-zero-dawn-part-1- 23. HTN Planning in Transformers: Fall of Cybertron | AI and Games #14 - YouTube, https://www.youtube.com/watch?v=kXm467TFTcY 24. An Introduction to Utility Theory - Game AI Pro, http://www.gameaipro.com/GameAIPro/GameAIPro_Chapter09_An_Introduction_to_Utility_Theory.pdf 25. Onchain Utility AI: A Litepaper - Ather Labs Atlas, https://atlas.atherlabs.com/atherxperiment/onchain-utility-ai 26. The Genius AI Behind The Sims - YouTube, https://www.youtube.com/watch?v=9gf2MT-IOsg 27. Understanding Perlin Noise - an in-depth look at the algorithm itself as well as implementation details. Also contains fully commented and deobfuscated code. : r/gamedev - Reddit, https://www.reddit.com/r/gamedev/comments/2d284n/understanding_perlin_noise_an_indepth_look_at_the/ 28. Exploring Procedural Content Generation for a 2D Space Exploration Game - Chalmers ODR, https://odr.chalmers.se/bitstreams/0af53ed4-c966-4620-a947-867f1b5c9d96/download 29. Procedural generation - Wikipedia, https://en.wikipedia.org/wiki/Procedural_generation 30. mxgmn/WaveFunctionCollapse: Bitmap & tilemap generation from a single example with the help of ideas from quantum mechanics - GitHub, https://github.com/mxgmn/WaveFunctionCollapse 31. How was Oskar Stalberg's Bad North and Townscaper grid systems implemented with all the unique pieces? : r/howdidtheycodeit - Reddit, https://www.reddit.com/r/howdidtheycodeit/comments/jpzhc6/how_was_oskar_stalbergs_bad_north_and_townscaper/ 32. Entity component system - Wikipedia, https://en.wikipedia.org/wiki/Entity_component_system 33. SanderMertens/ecs-faq: Frequently asked questions about Entity Component Systems, https://github.com/SanderMertens/ecs-faq 34. Entity-Component-Systems and Data-oriented design : r/gamedev - Reddit, https://www.reddit.com/r/gamedev/comments/1qtvug/entitycomponentsystems_and_dataoriented_design/ 35. LLM-A*: Large Language Model Enhanced Incremental Heuristic Search on Path Planning, https://liner.com/review/llma-large-language-model-enhanced-incremental-heuristic-search-on-path 36. Leveraging LLMs and Behavior Trees for Understanding User Instructions - kth .diva, https://kth.diva-portal.org/smash/get/diva2:1948875/FULLTEXT02.pdf 37. A Code-Driven Approach to Behavior Tree Generation for Robot Tasks Planning with Large Language Models - IJCAI, https://www.ijcai.org/proceedings/2025/0980.pdf 38. Digital Player: Evaluating Large Language Models based Human-like Agent in Games, https://arxiv.org/html/2502.20807v1 39. Generating Behavior-Diverse Game AIs with Evolutionary Multi-Objective Deep Reinforcement Learning - IJCAI, https://www.ijcai.org/proceedings/2020/0466.pdf 40. What Are the Essential Skills for Systems Engineer? A Comprehensive Overview, https://www.techneeds.com/2025/03/31/what-are-the-essential-skills-for-systems-engineer-a-comprehensive-overview/ 41. Systems Engineer - Grove Street Games, https://grovestreetgames.com/systems-engineer/ 42. Cutting-Edge AI for Gaming and the Future Beyond (Presented by Tencent AI Lab) - GDC Vault, https://www.gdcvault.com/play/1027502/Tencent-Game-AI-Cutting-Edge

**

**

# ゲーム開発を通じた計算論的思考の強化：AI・システム思考・課題解決のためのカリキュラム設計と世界的動向の調査報告書

日付: 2026年1月8日 対象: 大学・大学院における計算機科学およびシステム工学教育関係者 主題: ゲームAI開発を題材とした「思考の筋力トレーニング」としての体験型学習カリキュラムの提案、および米国・欧州・中国における最新Gaming AIトレンドの包括的調査

## 1. 序論：なぜ今、ゲームAIが「思考の筋トレ」なのか

### 1.1 背景：ブラックボックス化する技術と「思考」の空洞化

現代のコンピュータサイエンス教育、特にAIやIT開発の現場において、一つのパラドックスが生じています。ChatGPTやCopilotといった強力な生成AIツールの普及により、学生はかつてない速度でコードを生成し、動くアプリケーションを作ることができるようになりました。しかし、その裏側で、論理の「足腰」とも言うべき基礎的なシステム思考力、デバッグ能力、そして複雑な因果関係を解きほぐす力が空洞化するリスクが指摘されています。

学生たちは、ライブラリのAPIを叩くことには長けていても、そのライブラリが内部でどのような状態遷移を行っているのか、なぜそのアルゴリズムが選択されたのかという「根本原理」への理解がおろそかになりがちです。最新のLLM（大規模言語モデル）のトレンドを追うことは重要ですが、それらは数ヶ月単位で陳腐化します。教育機関として提供すべきは、技術の流行り廃りに左右されない、普遍的かつ堅牢な「論理的思考（Computational Thinking）」の型です。

### 1.2 ゲーム開発という「思考の実験室」

本報告書では、この課題に対する解決策として、「ゲームAI開発」を題材とした演習カリキュラムを提案します。ゲーム開発、特にゲーム内の自律エージェント（AI）やシステムを構築する作業は、極めて厳密な論理構築を要求される「思考の実験室」です。

Web開発やデータ分析と異なり、ゲームAIにおけるバグは「視覚的な振る舞い」として即座に現れます。経路探索のロジックが誤っていれば、キャラクターは壁に激突し続けます。状態遷移の設計が甘ければ、敵は棒立ちになります。この「即時フィードバック（Immediate Feedback）」こそが、学生の論理的思考を鍛えるための最強のツールとなります。ここでの「ゲーム開発」は、エンターテインメント作品を作ること自体を目的とせず、あくまで論理構造、状態管理、制約充足といったシステム工学の概念を体得するための「筋力トレーニング（筋トレ）」としての手段と位置づけます。

### 1.3 本報告書の構成

本報告書は大きく二つのパートで構成されます。前半では、教育カリキュラムの現実的な文脈を提供するために、2024年から2025年にかけての米国、欧州、中国におけるゲームAIの最新トレンドを網羅的に調査・分析します。後半では、それらのトレンドを踏まえつつ、Pythonを習得済みの学生が「インタプリタ作成」「レベルデザイン」「自律エージェント構築」を通じてシステム思考を鍛えるための具体的な授業設計を提案します。

## 2. 世界のGaming AI最新トレンド分析（2024-2025）

授業を行うにあたり、学生に対して「なぜこれを学ぶのか」という動機付けを行うためには、現在の産業界で実際にどのような技術が使われているかを示すことが不可欠です。2025年現在、ゲームAIは単なる「対戦相手」を超え、開発プロセスの自動化、デジタル社会のシミュレーション、そして人間の認知を拡張するパートナーへと進化しています。

以下の分析は、GDC (Game Developers Conference)、CEDEC、および主要な研究機関・企業の発表資料に基づいています。

### 2.1 中国：大規模シミュレーションと「デジタルライフ」の追求

中国のゲームAIトレンドは、Tencent（騰訊）やNetEase（網易）、miHoYoといった巨大テック企業が主導しており、その特徴は「規模」と「自律性」にあります。彼らは単なるNPCではなく、人間のように思考し、社会を形成する「デジタルプレイヤー」の構築を目指しています。

#### 2.1.1 NetEase Fuxi AI Lab：推論する「デジタルプレイヤー」

NetEase（網易）のFuxi AI Labは、従来の強化学習に加え、LLMをゲームプレイの「頭脳」として統合する研究で世界をリードしています。特に注目すべきは、オープンソースの戦略ゲーム『Unciv』（Civilizationのクローン）を用いたCivAgentの研究です。

- ニューロ・シンボリック・アーキテクチャの社会実装 NetEaseの研究チームは、LLMが単にテキストを生成するだけでなく、ゲームの勝利条件に向けて長期的な計画（Planning）を立てる能力を実証しました。CivAgentのアーキテクチャは、LLMを「推論器」として使用し、実際のゲーム操作（ユニットの移動、技術開発）は決定論的なコード（API）を通じて実行させます。 これは、LLMの「幻覚（Hallucination）」を抑制しつつ、高度な戦略立案を可能にするアプローチであり、学生が学ぶべき「システム設計」の好例です。エージェントはRAG（検索拡張生成）を用いてルールブックや過去のプレイデータを参照し、「現在は軍事力が不足しているため、火薬技術を優先すべきだ」といった推論を行います 。
    
- エンゲージメント指向のマッチメイキング (EnMatch) また、対戦ゲームにおけるマッチメイキングにおいても、単に勝率を均衡させる（ELOレーティング）のではなく、「プレイヤーのエンゲージメント（没頭度）」を最大化するためのAI活用が進んでいます。NetEaseのEnMatchフレームワークは、プレイヤーの離脱率や満足度を予測し、あえて実力差のあるマッチングを組むことで「劇的な勝利体験」を演出するなど、心理的な側面を数値化して制御するシステム工学的なアプローチをとっています 。
    

#### 2.1.2 Tencent AI Lab：生成と制御の融合

Tencentは、その圧倒的なユーザー数を背景に、コンテンツ生成の自動化と大規模エージェントの制御に注力しています。

- Hunyuan-GameCraftと空間知能 2025年に発表されたHunyuan-GameCraftは、1600時間以上のAAAタイトルゲームプレイ映像を学習したモデルであり、テキストプロンプトから一貫性のある3Dシーンやキャラクターの挙動を生成します。HKUST（香港科技大学）との共同研究では、2Dの映像から3Dの空間構造を理解する「空間知能（Spatial Intelligence）」の実装が進んでおり、これによりレベルデザインの大部分が自動化されつつあります 。
    
- 異種エージェントの協調 多数の異なる役割（タンク、ヒーラー、アタッカー）を持つAIエージェントが、共通の目標に向かって自律的に協調する強化学習モデルの研究も進んでいます。これは「チームワーク」をアルゴリズムで記述する試みであり、複雑系システムの学習に適した題材です 。
    

#### 2.1.3 miHoYo：美的追求と物理シミュレーション

『原神』や『崩壊：スターレイル』で知られるmiHoYoは、AIを「効率化」よりも「美的品質の向上」に活用する傾向があります。

- アニメーションの強化学習 キャラクターのスカートや髪の毛の揺れなど、複雑な物理挙動をアーティストの手付けアニメーションのような品質で再現するために、強化学習（RL）が用いられています。物理シミュレーションのパラメータをAIに調整させることで、破綻のない美しい映像をリアルタイムで生成しています。これは「美学」を数学的な「報酬関数」として定義する試みと言えます 。
    

### 2.2 欧米：創発的ストーリーテリングと汎用エージェント

米国および欧州のトレンドは、Google DeepMindやEA、Ubisoftなどが主導する「汎用的なゲームプレイ能力」と「人間と共創するNPC」に焦点が当てられています。

#### 2.2.1 Google DeepMind：ゲームを「夢見る」AI

DeepMindは、AIにゲームを「プレイさせる」段階から、AIにゲームそのものを「生成させる」段階へと移行しています。

- Genie 2とSIMA Genie 2は、ユーザーの入力に応じてリアルタイムでゲームの映像とロジックを生成する「世界モデル（World Model）」です。これはコードによって記述されたゲームエンジンを持たず、ニューラルネットワークが過去の学習データに基づいて「次はこうなるはずだ」という予測を映像として出力します。これは究極のブラックボックスですが、その背後にある「物理法則の学習」という概念は、学生にとって非常に刺激的なトピックです 。 また、SIMA (Scalable Instructable Multiworld Agent) は、自然言語の指示（「木を切れ」「城を見つけろ」）に従って、未知の3Dゲーム環境で行動できる汎用エージェントです。特定のゲーム専用のAPIを持たず、人間と同じように画面を見てキーボード操作を行うこのAIは、汎用人工知能（AGI）への重要なステップと位置づけられています。
    

#### 2.2.2 Ubisoft La Forge：身体性を持つ対話AI

Ubisoftの研究部門La Forgeは、LLMをゲームプレイに統合する「Neo NPC」プロジェクトを推進しています。

- Project Teammates (Jaspar) GDC 2024以降に公開されたデモでは、AIチームメイト「Jaspar」が登場します。従来のチャットボットと決定的に異なるのは、Jasparが「ゲームの状態」を理解している点です。プレイヤーが「右から回り込め！」と叫ぶと、JasparはLLMで意図を解釈し、ゲームエンジンの経路探索アルゴリズムを呼び出して実際に右翼へ展開します。ここでは**NLP（自然言語処理）とビヘイビアツリー（行動決定木）**の高度な統合が行われており、まさに本カリキュラムで目指す「システム結合」の実例です 。
    

#### 2.2.3 Electronic Arts (EA) & Xbox：開発者支援とテスト自動化

- SEED部門と模倣学習 EAのSEED部門は、人間のプレイヤーの操作ログから行動を学ぶ「模倣学習（Imitation Learning）」を用いて、人間らしい振る舞いをするBotを大量に生成しています。これらは主にQA（品質保証）工程で使用され、人間では不可能な回数のテストプレイを高速に行い、バグやバランスの不備を検出します。これは「課題解決」としてのAI活用の最も実用的な例です 。
    

### 2.3 インディー・研究界隈：アルゴリズムによる「構造」の美学

大手企業がブラックボックス的なDeep Learningに向かう一方で、インディーゲーム界隈や学術研究（7DRLなど）では、人間が理解可能なアルゴリズムを用いた**手続き型生成（Procedural Content Generation: PCG）**が再評価されています。

- Wave Function Collapse (WFC) 『Townscaper』や『Bad North』、『Caves of Qud』で使用されている**波動関数崩壊アルゴリズム（WFC）**は、制約充足問題（Constraint Satisfaction Problem）を応用したマップ生成技術です。「隣り合うタイルが矛盾しないように配置する」という単純なルールから、極めて複雑で美しい構造物が生成されます。このアルゴリズムは、決定論的でありながら創発的であるため、論理的思考のトレーニングに最適です 。
    

#### 表1: グローバルGaming AIトレンド・事例一覧（2024-2025）

|地域|カテゴリ|組織/プロジェクト|主要技術・キーワード|概要とURL/出典|教育的示唆・関連性|
|---|---|---|---|---|---|
|中国|大手R&D|NetEase Fuxi (CivAgent)|LLM, RAG, Neuro-Symbolic, Strategy|Civilization系ゲーム『Unciv』における、推論と実行を分離した自律エージェント。|推論と実行の分離: LLMを脳、APIを身体として設計するシステム思考。|
|中国|大手R&D|NetEase (EnMatch)|Engagement Optimization, Prediction|プレイヤーの離脱率や心理状態を予測し、勝率以外の指標でマッチングを最適化。|目的関数の設計: 「公平さ」とは何か、「面白さ」とは何かを数値化する課題解決。|
|中国|大手R&D|Tencent (GameCraft)|Generative AI, Spatial Intelligence|ビデオ入力からの3Dシーン再構築、プロンプトによるゲームロジック生成。|データ駆動開発: 大量データからルールを導き出す帰納的アプローチ。|
|米国|AI研究|Google DeepMind (Genie 2)|World Model, Video Generation|ゲームエンジンを持たず、ビデオ生成としてゲームプレイをシミュレートする基盤モデル。|モデル化: 世界の物理法則をニューラルネットで近似する概念。|
|欧州|大手R&D|Ubisoft La Forge (Project Teammates)|NLP, Behavior Trees, Embodied AI|自然言語による指示をゲーム内の戦術行動に変換するAIチームメイト。|インターフェース設計: 自然言語（曖昧）をコード（厳密）に変換する難しさ。|
|米国|大手R&D|EA SEED|Imitation Learning, Automated QA|人間のプレイデータを模倣し、テストプレイを自動化するボット群。|品質保証: バグ発見やバランス調整という実務的な課題解決。|
|世界|インディー|Townscaper / Bad North|Wave Function Collapse (WFC)|制約充足問題を用いた、矛盾のないマップ・構造物の自動生成。|制約プログラミング: 「何をしてはいけないか」を定義することで全体像を作る思考。|
|世界|コミュニティ|7DRL Challenge|Systemic Design, Roguelike|複雑な相互作用（火が草を燃やす、蒸気が視界を遮るなど）を持つシステムの短期開発。|創発性: 単純なルールの組み合わせから複雑な挙動を生むシステム思考。|

## 3. カリキュラム設計：「論理の筋トレ」としてのゲームAI開発

### 3.1 設計思想：なぜ「インタプリタ」や「レベルデザイン」なのか

本カリキュラムの目的は、ゲームを作ることそのものではなく、ゲーム開発のプロセスに内在する**「抽象化」「制約管理」「状態遷移」「メタ認知」**といったエンジニアリングの本質的なスキルを鍛えることにあります。

1. インタプリタを作る（抽象化・メタ認知） ゲーム内のスクリプト言語やカードゲームのルール処理系を作ることは、プログラミング言語そのものの仕組み（パース、実行、スタック）を理解することと同義です。これは、LLMが出力する曖昧なテキストを、厳密なシステム動作に変換する際の基礎体力となります。
    
2. レベルデザインをAIで行う（制約管理・最適化） 「プレイヤーがクリア可能なマップ」を自動生成するには、「スタートからゴールへの経路が存在する」という制約を数理的に保証する必要があります。これはシステム設計における要件定義とバリデーションの訓練になります。
    
3. キャラを設定する（状態遷移・因果関係） 「空腹なら食事をする」「敵が来たら逃げる」という行動をコードに落とし込む作業は、有限オートマトン（FSM）やビヘイビアツリー（BT）といった状態管理の訓練であり、複雑なシステムのバグを防ぐ思考法を養います。
    

### 3.2 授業構成案（全15回 / 1セメスター）

前提: Pythonの基本文法は習得済み。PC環境（Windows/Mac/Linux）あり。 使用ツール: Python 3.12+, Pygame または TCOD (Roguelike用ライブラリ), Visual Studio Code。 ※あえてUnityやUnreal Engineを使わず、Pythonコードベースで行うことで、ブラックボックスを排し「ロジックそのもの」に向き合わせます。

#### フェーズ1：世界の創造主（手続き型生成と制約）

テーマ: カオスからの秩序形成。制約条件の管理。

- 第1回：ランダムとノイズの違い
    

- 講義：完全なランダム（White Noise）はゲームとして面白くない。Perlin Noiseや平滑化の概念。
    
- 演習：Pythonで2次元配列を作り、ランダムに壁を配置した後、セル・オートマトン（Cellular Automata）のルール（「周囲に壁が多ければ壁になる」）を適用して、洞窟のような有機的な形状を生成する。
    
- 思考の筋トレ: 単純なルールの反復適用が、全体として意味のある構造（洞窟）を生み出す「創発（Emergence）」を体験する。
    

- 第2回：制約充足問題とWave Function Collapse (WFC)
    

- 講義：『Townscaper』や『Caves of Qud』で使われるWFCアルゴリズムの解説。エントロピー最小化の原理。
    
- 演習：簡易版WFCの実装。3x3のグリッドに対し、「道」「草」「海」のタイルを配置する。ただし「海と道は隣接できない」等のルールを設定し、矛盾なく埋めるプログラムを書く。
    
- 思考の筋トレ: 「何ができるか」ではなく「何をしてはいけないか（制約）」を定義することで解を導く、逆転の発想と論理的厳密さ。
    

- 第3回：経路探索と保証
    

- 講義：ダイクストラ法とA*（A-Star）アルゴリズム。グラフ理論の基礎。
    
- 演習：生成したダンジョンに対し、スタートからゴールまで到達可能かを検証（Flood Fill）し、最短経路を可視化する。到達不能なら再生成するループを作る。
    
- 思考の筋トレ: システムの「正当性（Valid state）」を自動テストする思考。
    

#### フェーズ2：ルールの執行者（インタプリタとDSL）

テーマ: 言語の構造化。メタプログラミング。

- 第4回：データとロジックの分離
    

- 講義：なぜ if card == "Fireball": damage(10) とハードコードしてはいけないのか。データ駆動設計（Data-Driven Design）の重要性。
    
- 演習：魔法やカードの効果をJSONやテキストファイル（例: NAME:Fireball, COST:5, EFFECT:DAMAGE(10)）で定義し、それを読み込んで実行するクラスを設計する。
    

- 第5回：インタプリタの構築（構文解析入門）
    

- 講義：Peter Norvigの『Lispy』（Pythonで作るLispインタプリタ）を参考にした、再帰的評価の仕組み 。
    
- 演習：簡単なスクリプト言語（DSL）のパーサを作る。文字列 (SEQ (MOVE_TO 10 10) (ATTACK_NEAREST)) をトークン化し、Pythonの関数呼び出しに変換する「実行エンジン」を実装する。
    
- 思考の筋トレ: コンピュータが「言葉」を「動作」に変えるプロセスの脱魔術化。再帰構造の理解。
    

- 第6回：イベント駆動アーキテクチャ
    

- 講義：オブザーバーパターンとメッセージパッシング。
    
- 演習：「ダメージを受けた時（OnDamage）」に発動するスキルを実装する。イベントキューを自作し、処理順序（スタック）を管理する。
    
- 思考の筋トレ: 非同期的な事象の因果関係を整理する力。
    

#### フェーズ3：知性の設計者（意思決定アルゴリズム）

テーマ: 状態管理と自律性。

- 第7回：ステートマシンの限界と可能性
    

- 講義：有限オートマトン（FSM）の基礎。状態爆発問題（スパゲッティコード化）の体験。
    
- 演習：FSMで敵AIを作る。「パトロール」「追跡」「攻撃」の状態遷移図を描き、実装する。
    

- 第8回：ビヘイビアツリー（Behavior Trees）
    

- 講義：HaloやUncharted等のAAAタイトルで標準的に使われるBTの構造。「Sequence（順次実行）」「Selector（優先選択）」ノード。
    
- 演習：FSMで作ったAIをBTで書き直す。モジュール化（「パトロール」ノードの再利用）の恩恵を体感する。
    
- 思考の筋トレ: 複雑な振る舞いを、再利用可能な小さな論理ブロックに分解する「構造化能力」 。
    

- 第9回：GOAP（Goal-Oriented Action Planning）
    

- 講義：F.E.A.R.やS.T.A.L.K.E.R.で使われるプランニングAI。
    
- 演習：AIに「空腹を満たす」というゴールだけ与える。AIは「食料を探す」「料理する」「食べる」というアクションの前提条件（Preconditions）と効果（Effects）を逆算し、自律的に行動計画を立てるシステムを作る。
    
- 思考の筋トレ: 目的から手段を逆算するバックキャスティング思考。
    

#### フェーズ4：AIとの共創者（LLMとシステムの統合）

テーマ: 確率的AIを決定論的システムに組み込む。 注意: ここではLLMを魔法の杖としてではなく、フェーズ2で作った「インタプリタ」への入力装置として扱います。

- 第10回：幻覚（Hallucination）の制御
    

- 講義：LLMは確率的に嘘をつく。JSONモードとスキーマエンジニアリング。
    
- 演習：OpenAI API（またはローカルのLlama 3等）を使い、自然言語の指示（「弱っている敵に火の玉を！」）を、フェーズ2で作ったDSL（CAST(TARGET=WEAKEST, SPELL=FIREBALL)）に変換させる。
    
- 思考の筋トレ: 曖昧な入力を厳密なシステム命令に変換する「サニタイズ」と「バリデーション」の設計。
    

- 第11回：RAGと世界観の維持
    

- 講義：コンテキストウィンドウの限界と検索拡張生成。
    
- 演習：ゲーム内の膨大な設定資料（Lore）をVector DBに入れ、NPCとの会話時に適切な知識を検索して回答させる「Lorekeeper」を作る。
    

- 第12回：デジタルダンジョンマスター（総合演習）
    

- 演習：プレイヤーの自由な行動（テキスト入力）に対し、LLMが状況を描写し、裏側でPythonのゲームエンジン（HP管理、アイテムドロップ）をAPI経由で操作するTRPGシステムを構築する。
    
- 思考の筋トレ: 「文系的な創造性（ナラティブ）」と「理系的な論理（システム）」の境界線を設計するエンジニアリング能力。
    

#### フェーズ5：最終課題（The Systemic Ecosystem）

- 第13-15回：最終プロジェクト
    

- 課題：「捕食者と被食者」「天候と植生」など、複数のAIエージェントと環境が相互作用する「閉じた生態系」シミュレーションを作成する。
    
- 要件：
    

1. マップはWFC等で自動生成されていること。
    
2. エージェントはBTまたはGOAPで自律行動すること。
    
3. ログまたは会話生成にLLMを利用し、状況をドラマチックに報告すること。
    

## 4. 課題解決とシステム思考への波及効果

このカリキュラムを通じて学生が得られるスキルは、ゲーム開発に留まらず、汎用的なITエンジニアリングや研究能力に直結します。

### 4.1 論理的整合性の検証能力

ゲームAI開発では、矛盾したロジック（例：HPが0なのに攻撃してくる）は許されません。この「動かない」「おかしい」という強烈な体験を通じて、学生はエッジケース（境界値）を想定する癖がつきます。これは金融システムやセキュリティ設計における**堅牢性（Robustness）**の確保と同じ思考回路です。

### 4.2 複雑系の理解とデバッグ

複数の自律エージェントが動く環境でのバグは、再現性が低く、原因特定が困難です。「なぜこのAIはここで立ち止まったのか？」をログや可視化ツールを使って追跡する作業は、分散システムやマイクロサービスの**可観測性（Observability）**とトラブルシューティング能力を養います。

### 4.3 人間とAIの協調設計

フェーズ4で学ぶ「LLMの出力をコードで制限・修正する」というアーキテクチャ（ニューロ・シンボリックAI）は、今後あらゆる産業用AIアプリケーション（医療、法務、金融）で必須となる設計思想です。AIを盲信するのではなく、信頼できるシステムの一部としてモジュール化する視点は、将来のAIエンジニアにとって最も重要なリテラシーとなります。

## 5. 推奨リソース・参考文献

学生に配布すべき、あるいは講師が参照すべき主要なリソースです。

### 5.1 書籍・テキスト

- "Programming Game AI by Example" (Mat Buckland) : 古典ですが、ステートマシンや自律エージェントの実装においてこれ以上の教科書はありません。Pythonでの再実装は非常に良い練習になります。
    
- "Artificial Intelligence: A Modern Approach" (Russell & Norvig) : AIの基礎理論。特に探索アルゴリズムや論理推論の章。
    

### 5.2 オンラインリソース・論文

- Stanford CS221 / Generative Agents: スタンフォード大学のAIコースおよび、LLMを用いた人間行動シミュレーション（Generative Agents）の論文。社会シミュレーションの最先端を知るために必須 。
    
- NetEase CivAgent Paper: "Digital Player: Evaluating Large Language Models based Human-like Agent in Games". 実践的なシステム構成図が掲載されており、システム設計の参考になります。
    
- WaveFunctionCollapse (GitHub - mxgmn): アルゴリズムの原典。多くの言語へのポートがあり、視覚的にも理解しやすい 。
    
- RoguelikeDev Resources (Reddit/GitHub): Pythonとtcodを用いたローグライク開発のチュートリアルが充実しており、授業のベースコードとして最適です 。
    

### 5.3 ツール

- Godot Engine: PythonライクなGDScriptを採用しており、視覚的なデバッグが容易。LLM統合プラグインも存在 。
    
- Ollama: ローカル環境でLlama 3等を動作させるツール。APIキーや通信コストを気にせず、学生が自身のPCでLLM統合を試すために最適。
    

## 6. 結論

本報告書で提案したカリキュラムは、ゲームという「楽しさ」を入り口にしつつ、その実体は極めてハードコアなコンピュータサイエンスの演習です。NetEaseやDeepMindといった世界のトップランナーたちも、結局のところ「いかにして複雑な現実（またはゲーム）をモデル化し、計算可能な形に落とし込むか」という課題に取り組んでいます。

インタプリタを書き、制約ソルバを実装し、エージェントの意思決定を設計するというプロセスは、流行のライブラリを使うだけでは得られない「エンジニアとしての基礎体力」を劇的に向上させます。この「思考の筋トレ」こそが、AI時代においても陳腐化しない、学生たちへの最高の贈り物となるはずです。

#### 引用文献

1. Bihan Xu's research works | University of Science and Technology of China and other places - ResearchGate, https://www.researchgate.net/scientific-contributions/Bihan-Xu-2248428686 2. Digital Player: Evaluating Large Language Models based Human-like Agent in Games, https://www.researchgate.net/publication/389510075_Digital_Player_Evaluating_Large_Language_Models_based_Human-like_Agent_in_Games 3. EnMatch: Matchmaking for Better Player Engagement via Neural Combinatorial Optimization | Proceedings of the AAAI Conference on Artificial Intelligence, https://ojs.aaai.org/index.php/aaai/article/view/28760 4. Research Project selected for 2025 Tencent AI Lab Rhino-Bird Focused Research Program, https://amc.hkust.edu.hk/news/research-project-selected-2025-tencent-ai-lab-rhino-bird 5. The State of AI Game Development in 2025: Progress and Barriers | by The Research Lab, https://medium.com/@theresearchlab/the-state-of-ai-game-development-in-2025-progress-and-barriers-42dc95aafc58 6. Tencent Games to Showcase Latest Tech at the GDC 2024, https://www.tencent.com/en-us/articles/2201793.html 7. miHoYo - TECH OTAKUS SAVE THE WORLD | PDF | Video Game Industry - Scribd, https://www.scribd.com/document/917366853/miHoYo-TECH-OTAKUS-SAVE-THE-WORLD 8. The Evaluation of miHoYo Technology Based on PEST, SWOT and POCD Analysis, https://bcpublication.org/index.php/BM/article/download/3002/2959/2931 9. Google DeepMind | From Prompt to Simulation Why Genie 3 is the missing piece for Extended Reality ️ and intelligent robots - Xpert.Digital, https://xpert.digital/en/google-genie-3/ 10. Ubisoft Reveals Teammates – An AI Experiment to Change the Game, https://www.ubisoft.com/en-us/studio/halifax/news/3mWlITIuWuu0MoVuR6o8ps/ubisoft-reveals-teammates-an-ai-experiment-to-change-the-game 11. Ubisoft La Forge – Pushing State-Of-The-Art AI In Games To Create The Next Generation Of NPCs, https://news.ubisoft.com/en-us/article/6Mv4hZqUMJoY1xpf1yiQPi/ubisoft-la-forge-pushing-stateoftheart-ai-in-games-to-create-the-next-generation-of-npcs 12. Report: EA's internal AI is causing issues with games development - Reddit, https://www.reddit.com/r/GamingLeaksAndRumours/comments/1oe0ucj/report_eas_internal_ai_is_causing_issues_with/ 13. EA execs say generative AI is "not merely a buzzword for us, it's the very core of our business," then pretend to tell a computer to generate buildings live on stage - GamesRadar, https://www.gamesradar.com/games/ea-execs-say-generative-ai-is-not-merely-a-buzzword-for-us-its-the-very-core-of-our-business-then-pretend-to-tell-a-computer-to-generate-buildings-live-on-stage/ 14. Wave Function Collapse Explained - BorisTheBrave.Com, https://www.boristhebrave.com/2020/04/13/wave-function-collapse-explained/ 15. How Townscaper Works: A Story Four Games in the Making | AI and Games #65 - YouTube, https://www.youtube.com/watch?v=_1fvJ5sHh6A 16. How Townscaper Works: A Story Four Games in the Making, https://www.gamedeveloper.com/game-platforms/how-townscaper-works-a-story-four-games-in-the-making 17. Risp (in (Rust) (Lisp)) - Stepan Parunashvili - Medium, https://medium.com/stepan/risp-lisp-in-rust-90a0dad5b116 18. Behavior Trees and how to implement them in Godot | This is Vini!, https://thisisvini.com/behavior-trees 19. Behavior Trees Enable Structured Programming of Language Model Agents - arXiv, https://arxiv.org/html/2404.07439v1 20. CISC 489: Artificial Intelligence in Games, https://www.eecis.udel.edu/~chester/courses/489.html 21. AIML402 Advanced Artificial Intelligence Semester 2 - University of Otago, https://www.otago.ac.nz/_media/papers/AIML402-Course-Outline.pdf 22. Computational Agents Exhibit Believable Humanlike Behavior | Stanford HAI, https://hai.stanford.edu/news/computational-agents-exhibit-believable-humanlike-behavior 23. kushagra06/CS221_AI: Stanford CS221: Artificial Intelligence: Principles and Techniques - GitHub, https://github.com/kushagra06/CS221_AI 24. mxgmn/WaveFunctionCollapse: Bitmap & tilemap generation from a single example with the help of ideas from quantum mechanics - GitHub, https://github.com/mxgmn/WaveFunctionCollapse 25. marukrap/RoguelikeDevResources: A curated list of roguelike development resources - GitHub, https://github.com/marukrap/RoguelikeDevResources 26. RoguelikeDev Does The Complete Roguelike Tutorial - Week 1 - Reddit, https://www.reddit.com/r/roguelikedev/comments/1m09vsn/roguelikedev_does_the_complete_roguelike_tutorial/ 27. Asset Library - Godot LLM - Godot Engine, https://godotengine.org/asset-library/asset/2913

**





**

# 生成AI主導型開発（バイブコーディング）時代におけるコンピュータサイエンス基礎教育の不可欠性とゲーム開発への応用に関する包括的調査報告書

## 要旨

本報告書は、生成AI（Generative AI）および大規模言語モデル（LLM）の急速な普及に伴い提唱された新たな開発パラダイム「バイブコーディング（Vibe Coding）」の有効性と限界を、特にゲーム開発という複雑なドメインに焦点を当てて検証するものである。Andrej Karpathy氏らによって提唱されたこの概念は、自然言語による直感的な指示のみでソフトウェア構築を行う未来を示唆するが、Andrew Ng氏やDave Farley氏を含む多数の専門家および最新の学術研究（Arxiv等）は、むしろ伝統的なIT基礎知識（アルゴリズム、データ構造、アーキテクチャ、デバッグ能力）の重要性が増していることを示唆している。

本調査では、認知科学的アプローチによる初学者の学習プロセス分析、ゲーム開発における状態管理と論理的整合性の課題、そして「プロンプトエンジニアリング」の本質的な計算論的思考要件を多角的に分析した。その結果、AIは熟練者にとっては強力な増幅器となる一方で、基礎を持たない初学者に対しては「能力の錯覚（Illusion of Competence）」を引き起こし、長期的には技術的負債と学習の停滞を招くリスクが高いことが明らかになった。本報告書は、これらの知見に基づき、AI時代における大学生および初学者が採るべき学習戦略と、技術的基礎がいかにしてAIツールのポテンシャルを最大化するかについて詳述する。

## 1. 序論：バイブコーディングの台頭と「基礎不要論」の検証

### 1.1 生成AIによるパラダイムシフトと「バイブコーディング」の定義

ソフトウェアエンジニアリングの世界は、GitHub CopilotやChatGPT、ClaudeといったAI支援ツールの登場により、かつてない変革期を迎えている。この中で生まれた「バイブコーディング（Vibe Coding）」という用語は、Andrej Karpathy氏らによって広められた概念であり、人間がコードの細部（構文やメモリ管理）を記述するのではなく、自然言語を用いてAIに「雰囲気（Vibe）」や意図を伝え、生成された出力を監督・修正しながら開発を進めるスタイルを指す 。

このアプローチは、プログラミングの敷居を劇的に下げ、非エンジニアでもアプリケーションを構築できる可能性を提示した。一部の楽観的な観測では、自然言語が新しいプログラミング言語となり、従来のコーディングスキルやコンピュータサイエンス（CS）の基礎知識は陳腐化するとさえ言われている。しかし、この「基礎不要論」に対しては、現場のエンジニアや教育研究者から強い懸念が示されている。バイブコーディングは、一見すると魔法のように機能するが、その背後には確率的なトークン予測というメカニズムが存在しており、これがソフトウェア工学における決定論的な要求と衝突する場面が多々あるからである 。

### 1.2 ゲーム開発：AI能力の極限試験場として

本報告書では、特に「ゲーム開発」を事例の中心に据える。Webアプリケーションの多くがステートレス（状態を持たない）なリクエスト処理を主とするのに対し、ゲーム開発は「状態（State）」の連続的な変化、リアルタイム処理、物理法則のシミュレーション、そして複雑なユーザーインタラクションを扱う高度なシステム工学である 。

Arxiv上の研究によれば、ゲーム開発はLLMにとって最も困難なタスクの一つであり、単なるテキスト生成能力だけでは解決できない「論理的整合性」や「空間的推論」が求められる 。したがって、ゲーム開発におけるAIの挙動を分析することは、AIの限界点と、それを補完するために必要な人間の「基礎力」を浮き彫りにする最適なケーススタディとなる。

### 1.3 本調査の構成と目的

本調査は、以下の多面的な問いに答えることを目的として構成されている。

1. 認知科学的側面：AI利用は初学者の学習プロセスやメタ認知にどのような影響を与えるのか？「能力の錯覚」とは何か？
    
2. 技術的側面（ゲーム開発）：状態管理、レベルデザイン、デバッグにおいて、なぜ基礎知識が不可欠なのか？
    
3. 品質管理と持続可能性：AIが生成するコードの「技術的負債」とは何か？
    
4. 教育的提言：これからの学生はどのようにAIと付き合い、何を学ぶべきか？
    

各セクションでは、Arxiv等の最新論文（プレプリント含む）から得られた実証データと、業界の専門家の意見を統合し、論拠を提示する。

## 2. 認知科学的分析：AI利用と学習者のメンタルモデル

AIツールが普及した現代において、プログラミング教育の現場では「AIを使えば初心者でも熟練者のように振る舞える」という現象が観察されている。しかし、深層的な理解を伴わないパフォーマンスの向上は、学習者の認知プロセスに深刻な副作用をもたらすことが研究によって明らかになりつつある。

### 2.1 「能力の錯覚（Illusion of Competence）」のメカニズム

最も警戒すべき現象の一つが「能力の錯覚」である。これは、学習者がAIの助けを借りて課題を達成できたにもかかわらず、それを自身の能力によるものだと誤認し、実際の理解度と自己評価の間に大きな乖離が生じる状態を指す。

Prather et al. (2024) による研究 "The Widening Gap: The Benefits and Harms of Generative AI for Novice Programmers" は、この問題を定量的に分析している。視線追跡（Eye Tracking）を用いた実験では、以下の傾向が確認された。

- メタ認知の欠如：成績下位の学生ほど、AIが生成したコードを無批判に受け入れる傾向があった。彼らはコードのロジックを追跡（トレース）する視線の動きが少なく、AIの出力を「正解」として即座に実装に移していた。
    
- 認知的不協和の解消：AIの助けを借りて課題を完了した学生は、インタビューにおいて「自分は理解している」と主張したが、実際にはコードの動作原理を説明できないケースが多発した。これは、AIの流暢な応答が学習者の自信を不当に高め、自らの無知を隠蔽してしまうことを示唆している。
    

さらに、Loksa et al. (2016) が提唱した問題解決の6段階モデル（再解釈、類似検索、解決策探索、評価、実装、実装評価）において、AI依存の初学者は「評価（Evaluate）」のプロセスをバイパスしがちであることが指摘されている 。正常に動作しているように見えるコードであっても、それがなぜ動くのか、どのようなエッジケースで動かなくなるのかを評価する能力が育たないまま、「完了」とみなしてしまうのである。

### 2.2 メンタルモデルの形成不全と過信

初学者がプログラミングを学ぶ過程で最も重要なのは、コンピュータがどのようにデータを処理し、メモリを管理するかという「メンタルモデル（心的な模型）」を構築することである。しかし、AIはこの構築プロセスを阻害する可能性がある。

Microsoft Researchの2025年のレポート や関連するArxiv論文 によれば、初心者はLLMに対して誤ったメンタルモデル（例：「AIは検索エンジンのように正確な知識を検索してくる」「AIは人間のように論理的に思考している」）を持ちやすい。

|誤ったメンタルモデル|正しい理解（IT基礎知識）|結果として生じる問題|
|---|---|---|
|AIは論理を理解している|AIは確率的にトークンを繋げているだけである|論理的に矛盾したコードでも「AIが書いたから正しい」と思い込み、デバッグが泥沼化する。|
|エラーが出たらAIに聞けば直る|エラーメッセージはコンパイラからの論理的な指摘である|エラーの原因を考えず、AIに同じ質問を繰り返して無限ループに陥る。|
|コードは動けばそれでよい|コードはメモリ効率や計算量、保守性が重要|動作はするがリソースを浪費する非効率な実装（O(n^2)など）を見過ごす。|

### 2.3 熟練者と初学者の認知的負荷の逆転現象

興味深いことに、AIツールの導入は必ずしもすべての開発者の負担を減らすわけではない。の研究 は、熟練者と初学者の間でAI利用時の「認知的負荷（Cognitive Load）」の質が異なることを示唆している。

- 熟練者（Expert）：自身の確固たる知識基盤（スキーマ）とAIの提案を照合する「検証モード」でAIを使用する。AIが単純作業を代行することで、より高次のアーキテクチャ設計に脳のリソースを割くことができる。
    
- 初学者（Novice）：知識基盤がないため、AIの提案が正しいかどうかを判断する基準を持たない。そのため、AIの出力を解読しようとする負荷や、誤ったコードが動かない時の混乱により、かえって認知的な混乱（Cognitive Overload）に陥るか、あるいは思考を放棄してAIに全依存するかの二極化が進む 。
    

この「理解とパフォーマンスのギャップ（Comprehension-Performance Gap）」は、特に既存のコードベースを修正するタスク（Brownfield Programming）において顕著となる。Qiao et al. (2025) の研究 では、AIを使用した学生グループはタスク完了速度こそ向上したが、コードベース全体の理解度は向上しなかった。これは、将来的にそのコードをメンテナンスしたり拡張したりする能力が欠如したエンジニアが量産されるリスクを示唆している。

## 3. ゲーム開発における特異点：AIが超えられない「論理の壁」

ゲーム開発は、Webサイト制作やデータ分析スクリプトの作成とは異なり、AIにとって極めて難易度の高い領域である。ここでは、具体的な事例を通じて、なぜITの基礎知識がなければAIを用いたゲーム開発が破綻するのかを詳述する。

### 3.1 状態管理（State Management）の崩壊と整合性

ゲームプログラミングにおいて最も重要な概念の一つが「状態（State）」である。プレイヤーのHP、所持アイテム、クエストの進行状況、敵の位置など、変数の集合体としての「世界」を一貫性を持って維持し続ける必要がある。

しかし、LLMは本質的にステートレスであり、長期的な一貫性を保つことが苦手である。

- テキストアドベンチャーの事例： や の事例では、LLMにゲームマスター役を任せた際、数ターン前には「鍵を持っていない」と言っていたのに、次のターンで突然ドアを開けてしまったり、死んだはずのNPCが会話に参加してきたりといった「幻覚（Hallucination）」が頻発した。 これを防ぐためには、PythonやC#などのプログラミング言語を用いて確実な「状態管理システム（Game State Machine）」を構築し、LLMにはその状態を参照させるだけの役割に制限する必要がある。つまり、「変数のスコープ」「データ構造（DictionaryやList）」「オブジェクト指向設計」といった基礎知識がなければ、まともに遊べるゲームは作れないのである 。
    
- DeepSeek/o1によるコード生成の限界： の報告によれば、優秀とされる推論モデル（OpenAI o1やDeepSeek R1）であっても、ゲーム開発においては「表示ロジック」と「データ管理ロジック」を分離（Separation of Concerns）できず、密結合なスパゲッティコードを生成してしまう傾向がある。これは、MVC（Model-View-Controller）やMVVMといったアーキテクチャパターンの知識を持つ人間が、コードの構造を修正・指導しなければ、拡張不可能なプロジェクトになってしまうことを意味する。
    

### 3.2 空間論理とレベルデザインの幻覚

ゲームのレベル（マップ）生成においても、AIの限界は顕著である。

- 倉庫番（Sokoban）の事例： や の研究では、AIにパズルゲームのレベルを生成させたところ、「クリア不可能な配置」や「物理的に到達できないエリア」を含むマップが生成されるケースが確認された。AIは「マップっぽいテキスト」を出力することはできるが、そのマップのトポロジー（位相幾何学的な接続関係）や、ゲームルール上の可解性を論理的に検証しているわけではない。 ここでも、A*アルゴリズムやダイクストラ法といった「グラフ探索アルゴリズム」の基礎知識を持つ人間が、生成されたマップがクリア可能かどうかを自動検証するスクリプトを書く必要がある。
    
- 物理エンジンの無視： UnityやUnreal Engineの開発において、AIはしばしばエンジンの物理法則を無視したコードを生成する。例えば、Rigidbodyを使用しているオブジェクトに対して、物理演算フレーム（FixedUpdate）ではなく描画フレーム（Update）で直接座標を書き換えるコードを提案することがある 。これは「一見動く」が、オブジェクトが壁をすり抜けたり、挙動が不安定になったりする原因となる。エンジンのライフサイクルや物理演算の基礎を知らない初学者は、このバグの原因を特定できず、途方に暮れることになる。
    

### 3.3 既存エンジン（Unity/Unreal）との統合難易度

Arxiv上の研究 は、UnityやUnreal Engine 5 (UE5) といった高度なゲームエンジンと生成AIの統合における課題を指摘している。

- APIの幻覚とバージョン不整合： ゲームエンジンは頻繁にアップデートされ、APIが変更される。LLMの学習データは過去のものであるため、廃止された関数や、存在しない架空のメソッド（例：Unityのtransform.Move()のような、ありそうで存在しない関数）を自信満々に提案することがある。公式ドキュメントを読み解き、コンパイラのエラーメッセージを理解する基礎力がなければ、AIの提案を修正して動かすことはできない。
    
- ブループリントとC++の乖離： Unreal Engineではビジュアルスクリプト（Blueprints）とC++が併用されるが、AIはこれらを混同したり、C++のメモリ管理（ポインタ、参照、ガベージコレクション）を誤ったりすることがある。特にC++のメモリリークや不正アクセスはゲームをクラッシュさせるため、ポインタやメモリ管理の概念理解は必須である 。
    

## 4. 隠れたコスト：技術的負債と品質保証

「バイブコーディング」で素早く動くプロトタイプを作ることは可能だが、それを製品レベル（Production Ready）に引き上げる段階で、基礎知識の欠如が致命的なコストとなって跳ね返ってくる。これを研究者たちは「生成的負債（Generative Debt）」と呼んでいる。

### 4.1 生成的負債（Generative Debt）の正体

の研究では、AI生成コード特有の技術的負債を以下の3つに分類している。

1. 構造的負債 (Structural Debt)：コードは動作するが、モジュール性が低く、一つのファイルに全てのロジックが詰め込まれている状態。可読性が低く、チーム開発や将来の拡張が困難になる。
    
2. 幻覚的複雑性 (Hallucinated Complexity)：標準ライブラリを使えば1行で済む処理を、AIがわざわざ独自の複雑な関数として実装してしまう現象。車輪の再発明により、バグの温床が増える。
    
3. 省略の負債 (Omission Debt)：エラーハンドリングやエッジケース（境界値）の処理が省かれている状態。AIは「ハッピーパス（正常系）」のコードを書くのは得意だが、ネットワーク切断や不正な入力といった「異常系」を無視する傾向がある。
    

これらの負債は、静的解析ツールやコードレビューによって発見・修正される必要があるが、そのためには「何が良いコード（Clean Code）か」という審美眼、すなわちソフトウェア工学の基礎知識が必要となる。

### 4.2 セキュリティリスク

Arxivのセキュリティ関連の研究 によれば、LLMが生成したコードの約40%に、SQLインジェクション、クロスサイトスクリプティング（XSS）、ハードコードされたクレデンシャル（パスワード等）などの脆弱性が含まれていたという報告がある。 特にゲーム開発において、サーバーサイドのロジック（課金処理、プレイヤーデータ保存）に脆弱性があれば、チートやデータ改ざんの被害に直結する。AIにセキュリティ意識を期待することは現状難しく、開発者自身がセキュリティの基礎（OWASP Top 10など）を理解し、AIの出力を監査しなければならない。

### 4.3 バイブコーディングの限界：プロトタイプから製品へ

や の記事は、バイブコーディングが「MVP（実用最小限の製品）」を作るには最適だが、「スケーラブルな製品」を作るには不向きであることを指摘している。 「動くこと」と「正しく作られていること」は別である。バイブコーディングで作られたゲームは、プレイヤーが10人のうちは動くかもしれないが、1000人になった瞬間にサーバーがダウンしたり、データベースが整合性を失ったりするリスクがある。スケーラビリティ、パフォーマンスチューニング（計算量オーダーの理解）、並行処理（スレッドセーフ）といったCSの基礎概念は、大規模なシステムを支えるために依然として不可欠である。

## 5. 逆説的真実：「プロンプトエンジニアリング」の本質はプログラミングである

「自然言語で指示すればよいから、プログラミング言語は不要」という考えは、プロンプトエンジニアリングの本質を誤解している。最新の研究は、効果的なプロンプトを作成する行為そのものが、高度なプログラミング的思考を要求することを示している。

### 5.1 "Prompts Are Programs Too"（プロンプトもプログラムである）

2025年の重要論文 "Prompts Are Programs Too: Understanding How Developers Build Software Containing Prompts" は、プロンプト開発が従来のソフトウェア開発と驚くほど類似していることを指摘している。 プロンプトエンジニアリングにおいて求められるのは、単なる文章力ではなく、以下の「計算論的思考（Computational Thinking）」である 。

- 分解 (Decomposition)： 複雑なタスク（例：「RPGを作って」）を、AIが処理可能な小さなサブタスク（例：「インベントリクラスの定義」「ダメージ計算式の実装」「UIイベントのハンドリング」）に分割する能力。これは関数の設計やクラス設計そのものである。
    
- 抽象化 (Abstraction)： 具体的な指示だけでなく、汎用的なルールや制約（例：「SOLID原則に従ってコードを生成せよ」）を言語化する能力。デザインパターンやアーキテクチャの知識がなければ、適切な抽象度の指示が出せない。
    
- デバッグと反復 (Debugging & Iteration)： AIが意図しない出力をした際、プロンプトのどの部分が曖昧だったのかを特定し、条件を追加・修正するプロセスは、プログラムのデバッグと同じ論理的推論を必要とする。
    

### 5.2 基礎知識がプロンプトの質を決める

AIに対する指示の質（Input Quality）は、出力の質（Output Quality）に直結する。ITの基礎知識を持つ者と持たない者では、同じAIを使っても得られる結果に天と地ほどの差が生まれる。

|初心者のプロンプト（Vibe重視）|基礎知識を持つ者のプロンプト（Engineering重視）|結果の違い|
|---|---|---|
|「インベントリシステムを作って。アイテムを持てるようにして。」|「UnityのScriptableObjectを使用してアイテムデータベースを構築し、インベントリはDictionary<ItemID, Quantity>で管理して検索をO(1)に最適化せよ。UIとは疎結合にするため、C#のActionデリゲートでイベント通知を行うこと。」|前者は拡張性がなく、アイテムが増えると処理落ちするコードになる。後者はプロ仕様の保守性が高く高速なコードになる。|
|「バグってるから直して。」|「NullReferenceExceptionが発生している。非同期ロード中にオブジェクトが参照されている可能性があるため、UniTaskを使用してawait処理を適切に実装するか、Nullチェックを追加して。」|前者はAIが当てずっぽうな修正を繰り返し、コードが汚くなる。後者は一発で根本原因が修正される。|

このように、「何が正解か（ベストプラクティス）」を知っていることこそが、最強のプロンプトエンジニアリングスキルなのである。

## 6. 専門家の見解とケーススタディ

業界の権威や著名なエンジニアたちも、AI時代における基礎学習の重要性を強調している。

### 6.1 Andrew Ng氏とAndrej Karpathy氏の視点

- Andrew Ng氏（AI研究の世界的権威）： 彼は、AIによるコーディングが進む現在であっても、ディープラーニングやアルゴリズムの仕組みを「ゼロから実装してみる」ことの重要性を説いている。「コードを一行読んだら、リファレンスを見ずに自分でタイプしてみる」といった意図的な練習（Deliberate Practice）が、深い理解（Deep Learning in Human Brain）に繋がると述べている 。
    
- Andrej Karpathy氏（元Tesla AIディレクター）： バイブコーディングの提唱者である彼でさえ、それが「伝統的なソフトウェアエンジニアリング」を完全に置換するものではなく、ツールベルトの一つであると認めている。彼は、AIが生成したコードの検証可能性（Verifiability）が重要であり、そのためには人間がコードを理解している必要があると示唆している 。
    

### 6.2 失敗事例からの教訓

- Redditや技術ブログでの報告 ： あるゲーム開発者は、全てのコードをLLMに書かせた結果、プロジェクトの後半でバグ修正が不可能になり、プロジェクトが破綻したと告白している。「自分が理解していないコードが1万行ある」という恐怖は、開発のモチベーションを破壊する。彼が得た教訓は、「AIはアシスタントであり、司令官（自分）が技術を理解していなければならない」という点であった。
    

## 7. 大学生への提言：AI時代を生き抜くための学習戦略

以上の調査に基づき、これからITやゲーム開発を学ぶ大学生に対して、以下の具体的な学習戦略を提案する。

### 7.1 「サンドイッチ方式」の実践

AIを排除するのではなく、人間の工程でAIを挟み込むワークフローを確立せよ。

1. Human (Architect & Plan)：
    

- 何を作るか、どういう構造（アーキテクチャ）にするかは人間が決める。これにはデザインパターンやシステム設計の基礎知識が必要。
    

2. AI (Draft & Generate)：
    

- ボイラープレート（定型文）の生成、基本的な関数の実装、APIの使い方の検索はAIに任せる。ここで生産性を爆発的に高める。
    

3. Human (Review & Refine)：
    

- AIが書いたコードを一行ずつ読み、セキュリティ、パフォーマンス、整合性をチェックする。バグがあれば修正し、プロジェクト全体に統合する。これにはデバッグ能力とコード読解力が必要。
    

### 7.2 重点的に学ぶべき「基礎」の再定義

単に文法を暗記する（Syntax）のではなく、AIが苦手とする「概念（Semantics & Context）」を重点的に学ぶべきである。

- アルゴリズムとデータ構造： AIが出したコードが効率的か（計算量オーダー）、適切なデータ構造を使っているか（List vs Dictionary vs HashSet）を判断するため。
    
- メモリとハードウェアの理解： なぜゲームが重いのか、なぜクラッシュするのかを理解するため（スタックとヒープ、ガベージコレクション、GPUのパイプライン）。
    
- デバッグとトラブルシューティング： エラーログを読む力、仮説検証のサイクルを回す力。これはAIには代替できない「探偵」のようなスキルである。
    
- 英語（English）： 最新のAIモデルやドキュメントは英語が主流であり、英語でのプロンプトの方が精度が高い場合が多いため、英語力も立派な「IT基礎」の一つと言える。
    

### 7.3 「苦闘（Productive Struggle）」を避けない

最も重要なのは、学習の過程で「わからない」「動かない」という壁にぶつかった時、すぐにAIに答えを求めず、まずは自分で考える時間を確保することである。 Pratherらの研究が示したように、この「苦闘」のプロセスこそが、脳内に強固な神経回路（スキーマ）を形成し、真の応用力を育む。AIは、その苦闘の末に答え合わせをするための「家庭教師」として使うべきであり、宿題を代行させる「代行業者」として使ってはならない。

## 8. 結論

バイブコーディングの時代において、ITの基礎知識は「不要」になるどころか、**「プレミアムな価値」**を持つようになった。 誰もがAIを使って「それっぽいもの」を作れるようになったからこそ、その裏側にあるロジックを理解し、トラブルを解決し、品質を保証できるエンジニアの希少性は高まっている。 ゲーム開発という、論理と創造性が交差する最も複雑なフィールドにおいて、AIは強力な武器となる。しかし、その武器を使いこなすためには、使い手である人間に確固たる「基礎」という土台がなければならない。

学生諸君には、表面的な「Vibe（雰囲気）」に流されることなく、技術の深淵にある原理原則を学び、AIを真の意味で支配できるエンジニアを目指してほしい。

### 付録：データと統計

#### 表1: 熟練者と初学者のAI利用における行動比較

|行動指標|熟練者 (Expert)|初学者 (Novice)|
|---|---|---|
|視線動向|生成コードの論理構造（ループ条件、分岐）を重点的に注視|全体を漠然と見るか、コピーボタンを即座に探す|
|デバッグ戦略|エラーメッセージに基づき、コードの特定箇所を修正|全文を再生成させたり、AIに「動かない」と曖昧に訴える|
|認知的負荷|減少（単純作業からの解放）|増大（検証不能なコードへの不安）または著しく低下（思考停止）|
|成果物の品質|高い（保守性・効率性が考慮されている）|表面上は動くが、脆弱性や技術的負債を含む|

#### 表2: LLMが生成したコードに含まれる主な脆弱性とその割合

|脆弱性の種類|概要|発生頻度（概算）|
|---|---|---|
|セキュリティ|SQLインジェクション、XSS、APIキーの露出|~40%|
|信頼性 (Reliability)|例外処理の欠如、Nullチェック漏れ|~50%|
|保守性 (Maintainability)|冗長なコード、ハードコードされた定数、不適切な命名|~80%（初期生成時）|
|※ 静的解析ツールによるフィードバックを与えながら反復修正させることで、これらは改善可能だが、その「フィードバック」を与える知識が人間に必要である。|||

#### 引用文献

1. What is Vibe Coding? The Pros, Cons, and Controversies | Tanium, https://www.tanium.com/blog/what-is-vibe-coding/ 2. Andrej Karpathy: Software Is Changing (Again) - The Singju Post, https://singjupost.com/andrej-karpathy-software-is-changing-again/ 3. Simon Willison on andrej-karpathy, https://simonwillison.net/tags/andrej-karpathy/ 4. The Dark Side of Vibe-Coding: Debugging, Technical Debt & Security Risks, https://dev.to/arbisoftcompany/the-dark-side-of-vibe-coding-debugging-technical-debt-security-risks-9ef 5. Andrej Karpathy: Software in the era of AI [video] - Hacker News, https://news.ycombinator.com/item?id=44314423 6. Beyond Synthetic Benchmarks: Evaluating LLM Performance on Real-World Class-Level Code Generation - arXiv, https://arxiv.org/html/2510.26130v2 7. V-GameGym: Visual Game Generation for Code Large Language Models - arXiv, https://arxiv.org/html/2509.20136v1 8. Generating Games via LLMs: An Investigation with Video Game Description Language, https://arxiv.org/html/2404.08706v1 9. A Survey on Large Language Model-Based Game Agents - arXiv, https://arxiv.org/html/2404.02039v3 10. The Widening Gap: The Benefits and Harms of Generative AI for Novice Programmers - Juho Leinonen, https://juholeinonen.com/assets/pdf/prather2024widening.pdf 11. The Widening Gap: The Benefits and Harms of Generative AI for Novice Programmers | Request PDF - ResearchGate, https://www.researchgate.net/publication/383080888_The_Widening_Gap_The_Benefits_and_Harms_of_Generative_AI_for_Novice_Programmers 12. Protecting The Young, and Defending Independent Thought, in the Age of GenAI, https://thequantumrecord.com/philosophy-of-technology/defending-independent-thought-in-age-of-genai/ 13. The Widening Gap: The Benefits and Harms of Generative AI for Novice Programmers, https://arxiv.org/html/2405.17739v1 14. Fostering appropriate reliance on GenAI Lessons learned from early research - Microsoft, https://www.microsoft.com/en-us/research/wp-content/uploads/2025/03/Appropriate-Reliance-Lessons-Learned-Published-2025-3-3.pdf 15. User Misconceptions of LLM-Based Conversational Programming Assistants - arXiv, https://arxiv.org/html/2510.25662v1 16. Mental model shifts in human-LLM interactions - ResearchGate, https://www.researchgate.net/publication/393055408_Mental_model_shifts_in_human-LLM_interactions 17. Towards Decoding Developer Cognition in the Age of AI Assistants - arXiv, https://arxiv.org/html/2501.02684v1 18. Who's the Leader? Analyzing Novice Workflows in LLM-Assisted Debugging of Machine Learning Code - arXiv, https://arxiv.org/html/2505.08063v1 19. Comprehension-Performance Gap in GenAI-Assisted Brownfield Programming: A Replication and Extension - arXiv, https://arxiv.org/html/2511.02922v1 20. Comprehension-Performance Gap in GenAI-Assisted Brownfield Programming: A Replication and Extension - ResearchGate, https://www.researchgate.net/publication/397321474_Comprehension-Performance_Gap_in_GenAI-Assisted_Brownfield_Programming_A_Replication_and_Extension 21. [Part 1] Crafting a Text Adventure Game with LLMs in Just 6 Hours! | by Dain Kim - Medium, https://medium.com/@ddanakim0304/part-1-crafting-a-text-adventure-game-with-llms-in-just-6-hours-bb415ebbb67a 22. Intra: design notes on an LLM-driven text adventure - Ian Bicking, https://ianbicking.org/blog/2025/07/intra-llm-text-adventure 23. I Vibe Coded a Game That Attracted 10k+ Players In a Single Weekend - Generative AI, https://generativeai.pub/i-vibe-coded-a-game-that-attracted-10k-players-in-a-single-weekend-6cff508bad58 24. Testing LLM Creativity Through The Power of Constraints: The Commodore 64 Challenge, https://medium.com/@gianlucabailo/testing-llm-creativity-through-the-power-of-constraints-the-commodore-64-challenge-0b147d6e02c7 25. 90% Faster, 100% Code-Free: MLLM-Driven Zero-Code 3D Game Development - arXiv, https://arxiv.org/html/2509.26161v1 26. Unreal-Engine-Based General Platform for Multi-Agent Reinforcement Learning - arXiv, https://arxiv.org/html/2503.15947v1 27. DreamGarden: A Designer Assistant for Growing Games from a Single Prompt - arXiv, https://arxiv.org/html/2410.01791v1 28. Quantitative Analysis of Technical Debt and Pattern Violation in Large Language Model Architectures - arXiv, https://arxiv.org/html/2512.04273v1 29. Static Analysis as a Feedback Loop: Enhancing LLM-Generated Code Beyond Correctness, https://arxiv.org/html/2508.14419v1 30. Security and Quality in LLM-Generated Code: A Multi-Language, Multi-Model Analysis, https://arxiv.org/html/2502.01853v1 31. Unveiling Inefficiencies in LLM-Generated Code: Toward a Comprehensive Taxonomy, https://arxiv.org/html/2503.06327v2 32. What vibe coding can (and can't) do for software engineering | We Love Open Source, https://allthingsopen.org/articles/what-is-vibe-coding-developers 33. Why Your Vibe Coding Is Ruining Your Business - Ulam Labs, https://www.ulam.io/blog/why-your-vibe-coding-is-ruining-your-business 34. (PDF) Prompts Are Programs Too! Understanding How Developers Build Software Containing Prompts - ResearchGate, https://www.researchgate.net/publication/384154805_Prompts_Are_Programs_Too_Understanding_How_Developers_Build_Software_Containing_Prompts 35. Prompts Are Programs Too! Understanding How Developers Build Software Containing Prompts (FSE 2025 - Research Papers) - conf.researchr.org, https://conf.researchr.org/details/fse-2025/fse-2025-research-papers/2/Prompts-Are-Programs-Too-Understanding-How-Developers-Build-Software-Containing-Prom 36. Leveraging Computational Thinking in the Era of Generative AI - Communications of the ACM, https://cacm.acm.org/blogcacm/leveraging-computational-thinking-in-the-era-of-generative-ai/ 37. What Should We Engineer in Prompts? Training Humans in Requirement-Driven LLM Use, https://arxiv.org/html/2409.08775v2 38. Improving Student-AI Interaction Through Pedagogical Prompting: An Example in Computer Science Education - arXiv, https://arxiv.org/html/2506.19107v1 39. Five Important AI Programming Languages - DeepLearning.AI, https://www.deeplearning.ai/blog/five-important-ai-programming-languages/ 40. A quote from Andrew Ng - Simon Willison's Weblog, https://simonwillison.net/2025/Mar/15/andrew-ng/ 41. Andrew Ng calls "vibe coding" an unfortunate term for deep intellectual exercise - Perplexity, https://www.perplexity.ai/page/andrew-ng-calls-vibe-coding-an-Sg_5eUFKSASP5kPByGD8tg 42. How vibe coding lead to my project's downfall. : r/gamedev - Reddit, https://www.reddit.com/r/gamedev/comments/1q043ym/how_vibe_coding_lead_to_my_projects_downfall/

**











