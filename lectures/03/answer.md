# 第3回 解答

## 演習

- 第1回（素のLLM）とエージェントの回答の違い：
- `--trace` で見えたツール呼び出し（ツール名と引数）：
- 1つの質問での LLM 呼び出し回数（`requests`）：
- 追加したツールと、docstring に書いた説明：

## 宿題

- 取り組んだレベル：基礎 
- やったこと：
`agent.py` の `INSTRUCTIONS` や `tools.py` の `docstring` を書き換えた際に、ツールの呼ばれ方（`--trace`）や回答内容、トークン消費量がどう変化するかを比較・記録する。
**実行コマンド:**
```bash
uv run python -m app.agent --trace "LoRAとQLoRAの違いは？"
```
**使用モデル:** `gemini-3.5-flash-lite`

- 結果：
| 比較項目 | ① 変更なし（基準） | ② `agent.py` に追加 | ③ `tools.py` に追加 |
| :--- | :--- | :--- | :--- |
| **入力トークン数 (`input_tokens`)** | 1,310 | 1,354 (+44) | 1,424 (+114) |
| **出力トークン数 (`output_tokens`)** | 184 | 155 (-29) | 177 (-7) |
| **APIコスト (`cost`)** | $0.0008530 | $0.0007937 | $0.0008697 |
| **リクエスト回数 (`requests`)** | 2回 | 2回 | 2回 |
| **ツール呼び出し回数 (`tool_calls`)** | 2回 | 2回 | 2回 |
| **呼ばれたツール (`trace`)** | `search_glossary('LoRA')`<br>`search_glossary('QLoRA')` | `search_glossary('LoRA')`<br>`search_glossary('QLoRA')` | `search_glossary('LoRA')`<br>`search_glossary('QLoRA')` |



- 気づき・疑問：
1. **違いはトークン**
   `INSTRUCTIONS`（システムプロンプト）や `docstring`（関数の説明文）は、どちらも裏側でLLMへの入力プロンプトとして送信される。そのため、記述を増やした分だけ `input_tokens` が確実に増加することが数値（1310 → 1354 → 1424）から確認できる。

2. **`trace`が変わらなかった**
   「LoRAとQLoRAの違いは？」という質問に答えるには、どちらの用語も `search_glossary` で調べている。説明文やルールを補足しても「2つの用語を検索する」という指示ではなかったため、ツール呼び出しのログ自体は同じ結果である。

3. **影響**
   同じ情報を受け取っていても、`INSTRUCTIONS` や `docstring` の書き方が変わることで、モデルが出力の長さが微妙に変化することが分かる。