# 第3回 演習・宿題：学習支援エージェントを作る

## この回のゴール

- エージェントが「モデル＋ループ＋ツール」でできていることを、自分のコードで確かめる
- どのツールが、どの引数で呼ばれたかを読める
- ツールを1つ追加できる

## 準備

前の回までの作業が終わっている場合は、`main` から `lec03` ブランチを作ります。

```bash
git switch main && git switch -c lec03
```

終わっていない場合は、講座 repo の開始時点のコード（`lec03-start` タグ）からブランチを作れます。

```bash
git remote -v                     # upstream がなければ次の行で登録する
git remote add upstream https://github.com/matsuolab/lecture-ai-engineering-2026.git
git fetch upstream --tags
git switch -c lec03 lec03-start
```

## 演習（30分）

### 1. 第1回と同じ質問をエージェントに投げる

```bash
uv run python -m app.agent "AIE2026の講座で使う「lecNN-start タグ」とは何ですか？"
```

第1回の `app.ask` の回答と比べてみましょう。

### 2. ツール呼び出しを読む

```bash
uv run python -m app.agent --trace "LoRAとQLoRAの違いは？"
```
＿＿＿＿＿＿＿
`[tool call]` の行で、モデルがどのツールをどんな引数で呼んだかを確認します。`[usage]` の `requests` は、1つの質問で LLM を何回呼んだかを表します。
uv run：このプロジェクトの環境でプログラムを実行する
python -m app.agent：app/agent.pyを実行する
--trace：回答だけでなく、エージェントが使ったツールも表示する
"LoRAとQLoRAの違いは？"：エージェントに渡す質問
[tool call]：モデルが「このツールをこの引数で使う」と決めた記録
[tool return]：ツールが調べて返した結果
[usage] requests：モデルに問い合わせた回数。たとえば、ツールを使う指示を出すために1回、ツールの結果を受けて回答するためにもう1回、合計2回になることがあります
tool_calls：ツールを呼んだ回数。requestsとは別の数です
＿＿＿＿
AIE2026の講座における「3レベル」とは、宿題の構成を段階的に分けた以下の3つのレベルのことを指します。

1. **基礎**：講義内容の確認を行うレベル
2. **実装**：自分で実際にコードを書くレベル
3. **発展**：調査や新たな試みを行うレベル

この3つのレベルのうち、**どれか1つ**に取り組めばその回の宿題は完了となります。なお、原則として宿題の採点はありませんので、ご自身の理解度や目的に合わせて選んで取り組んでみてください。

関連する回：第1回
(aie2026-exercises) @o ➜ /workspaces/lecture-ai-engineering-2026 (lec03) $ uv run python -m app.agent --trace "LoRAとQLoRAの違いは？"
[model] gemini-3.5-flash-lite
講座の用語集によると、LoRAとQLoRAの違いは以下のとおりです。

* **LoRA**
  事前学習済みの重みを固定したまま、重みの更新分を2つの小さな行列（低ランク行列）の積で表し、その小さな行列だけを学習するPEFT（Parameter-Efficient Fine-Tuning）手法です。学習するパラメータを大幅に削減できます。

* **QLoRA**
  ベースモデルの重みを4ビットなどに**量子化**してメモリを大幅に節約したうえで、LoRAを適用して学習する手法です。これにより、さらに大きなモデルを小さなGPU環境でも扱えるようになります。

（関係する回：第2回）

--- trace ---
[tool call]   search_glossary({'query': 'LoRA'})
[tool call]   search_glossary({'query': 'QLoRA'})
[tool return] search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…
[tool return] search_glossary -> [{"term": "QLoRA", "lecture": 2, "definition": "ベースモデルの重みを4ビットなどに量子化してメモリを節約したうえで、LoRAで学習する手法。より大きなモデルを小さなGPUで扱える。本講座の第2…
[usage] RunUsage(cost=Decimal('0.0008338'), details={'text_prompt_tokens': 1196}, input_text_tokens=1196, input_tokens=1196, output_tokens=190, requests=2, tool_calls=2)
＿＿＿＿
uv run python -m app.agent --trace "LoRAとQLoRAの違いは？"

[model] gemini-3.5-flash-lite
LoRAとQLoRAの主な違いは、**ベースモデルの重みの保持方法（量子化の有無）**にあります。

* **LoRA**: 
  事前学習済みの重みをそのまま固定し、追加の小さな低ランク行列（アダプタ）のみを学習してパラメータ数やメモリを削減するPEFT手法です。
* **QLoRA**: 
  LoRAの手法をベースにしつつ、ベースモデルの重みを4ビットなどに**量子化**してさらにメモリを大幅に節約した上で学習を行います。これにより、より大きなモデルを比較的小さなGPUメモリでも扱えるようになります。

（関連する回：第2回）

--- trace ---
[tool call]   search_glossary({'query': 'LoRA'})
[tool call]   search_glossary({'query': 'QLoRA'})
[tool return] search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…
[tool return] search_glossary -> [{"term": "QLoRA", "lecture": 2, "definition": "ベースモデルの重みを4ビットなどに量子化してメモリを節約したうえで、LoRAで学習する手法。より大きなモデルを小さなGPUで扱える。本講座の第2…
[usage] RunUsage(cost=Decimal('0.0008530'), details={'text_prompt_tokens': 1310}, input_text_tokens=1310, input_tokens=1310, output_tokens=184, requests=2, tool_calls=2)
＿＿＿＿
agentに追加
[model] gemini-3.5-flash-lite
LoRAとQLoRAの違いは以下のとおりです。

* **LoRA**: 事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列（低ランク行列）で表し、その小さな行列だけを効率的に学習するPEFT手法です。
* **QLoRA**: ベースモデルの重みを4ビットなどに量子化してメモリを大きく節約したうえで、LoRAによる学習を行う手法です。これにより、より大きなモデルを小さなGPU環境でも扱えるようになります。

（第2回）

--- trace ---
[tool call]   search_glossary({'query': 'LoRA'})
[tool call]   search_glossary({'query': 'QLoRA'})
[tool return] search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…
[tool return] search_glossary -> [{"term": "QLoRA", "lecture": 2, "definition": "ベースモデルの重みを4ビットなどに量子化してメモリを節約したうえで、LoRAで学習する手法。より大きなモデルを小さなGPUで扱える。本講座の第2…
[usage] RunUsage(cost=Decimal('0.0007937'), details={'text_prompt_tokens': 1354}, input_text_tokens=1354, input_tokens=1354, output_tokens=155, requests=2, tool_calls=2)
＿＿＿
toolに追加

[model] gemini-3.5-flash-lite
LoRAとQLoRAの違いは以下の通りです。

- **LoRA**
  - 事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法です。学習するパラメータが少なく、学習結果（アダプタ）も小さいファイルで保存できます。
- **QLoRA**
  - ベースモデルの重みを4ビットなどに量子化してメモリを節約したうえで、LoRAで学習する手法です。これにより、より大きなモデルを小さなGPUで扱うことができます。

（第2回）

--- trace ---
[tool call]   search_glossary({'query': 'LoRA'})
[tool call]   search_glossary({'query': 'QLoRA'})
[tool return] search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…
[tool return] search_glossary -> [{"term": "QLoRA", "lecture": 2, "definition": "ベースモデルの重みを4ビットなどに量子化してメモリを節約したうえで、LoRAで学習する手法。より大きなモデルを小さなGPUで扱える。本講座の第2…
[usage] RunUsage(cost=Decimal('0.0008697'), details={'text_prompt_tokens': 1424}, input_text_tokens=1424, input_tokens=1424, output_tokens=177, requests=2, tool_calls=2)
＿＿＿＿


### 3. ツールを1つ追加する

`app/tools.py` に `make_quiz` を追加し、`app/agent.py` の `TODO(第3回 演習)` の場所で登録します。

- 例：指定した回（`lecture: int`）の用語から1つを選び、「この用語の意味は？」という問題と答えを返す
- docstring には「いつ、何のために使うツールか」を書く（モデルはこれを読んで使うかどうかを決める）

```bash
uv run python -m app.agent --trace "第2回の内容から確認問題を1問出して"
uv run pytest -q
```

### 4. 提出

`lectures/03/answer.md` を書き、`lec03` → 自分の fork の `main` へ PR を出します。

## 宿題（どれか1つで完了）

| レベル | 内容 |
|---|---|
| 基礎 | `INSTRUCTIONS` やツールの docstring を書き換え、ツールの呼ばれ方や回答がどう変わるかを `--trace` で比べて記録する |
| 実装 | 学習の記録を `learning_log/` に保存する `save_learning_log` ツールを作る。保存の前に利用者の確認を挟む（Pydantic AI の `requires_approval=True`）。TestModel を使ったテストも書く |
| 発展 | 次のどちらか。(a) 同じエージェントを Google の ADK で作り直し、書き方や `adk web` での見え方を比較する。(b) 講義で紹介した Pi を Codespaces 上で動かし、公開されている Pi のシステムプロンプトと自分のエージェントの `INSTRUCTIONS` を比較する |

### 発展（b）の進め方

Pi はファイルの読み書きやコマンドの実行ができるコーディングエージェントで、ツールを実行するたびに確認は求めません。自分のPCではなく、Codespaces の中で試してください。

```bash
npm install -g --ignore-scripts @earendil-works/pi-coding-agent
pi
```

- Gemini は環境変数 `GEMINI_API_KEY` を読むので、Codespaces secret があればそのまま使えます。Pi の中で `/model` と入力し、Gemini のモデルを選びます
- npm のパッケージ名は `@earendil-works/pi-coding-agent` です（古い記事にある `@mariozechner/...` は旧名です）
- Pi のシステムプロンプトは、公開リポジトリ https://github.com/earendil-works/pi の `packages/coding-agent/src/core/system-prompt.ts` にあります。自分の `INSTRUCTIONS` と比べ、何が書かれていて何が書かれていないかを見てみましょう
- 公式ドキュメント：https://github.com/earendil-works/pi/tree/main/packages/coding-agent/docs

## 参考

- Pydantic AI: https://ai.pydantic.dev/
- ADK: https://google.github.io/adk-docs/
