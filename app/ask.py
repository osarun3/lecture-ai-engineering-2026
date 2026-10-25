"""第1回: 素のLLMに1回だけ質問するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask            # 質問を省略すると、講座に固有の質問をする

ツールも会話履歴も持たない「素の」呼び出し。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse
#追加
import time
from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def ask(question: str) -> str:
    client = genai.Client(api_key=get_api_key())
    response = client.models.generate_content(model=MODEL, contents=question)

    # TODO(第1回 演習): response.usage_metadata から
    #   入力トークン数と出力トークン数を表示してみよう（Copilotに頼んでよい）

    # 会話履歴を自動で記憶してくれるチャットセッションを作成する
    chat = client.chats.create(model=MODEL)

    # 最初の質問をセットする
    current_question = question
    turn = 1


    print(f"[質問] {current_question}\n")

        # ストップウォッチ開始（応答時間の計測スタート）
    start_time = time.perf_counter()

        # チャットセッションにメッセージを送る（過去の会話履歴も自動で一緒に送られる）
    response = chat.send_message(current_question)

        # ストップウォッチ停止（かかった秒数を計算）
    elapsed_time = time.perf_counter() - start_time

        # AIの返答を表示
    print(f"[回答]\n{response.text}\n")

        # response.usage_metadata からトークン数を取得して表示
    usage = response.usage_metadata
    if usage:
            prompt_tokens = usage.prompt_token_count        # 入力トークン数（履歴＋今回の質問）
            output_tokens = usage.candidates_token_count    # 出力トークン数（今回のAIの返答）
            total_tokens = usage.total_token_count          # 合計トークン数
            print(
                f"[計測] 応答時間: {elapsed_time:.2f}秒 | "
                f"トークン数 -> 入力: {prompt_tokens}, 出力: {output_tokens}, 合計: {total_tokens}"
            )
    else:
            print(f"[計測] 応答時間: {elapsed_time:.2f}秒 | トークン情報なし")
    #return response.text


def main() -> None:
    parser = argparse.ArgumentParser(description="素のLLMに質問する")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    args = parser.parse_args()

    print(f"[model] {MODEL}")
    print(f"[質問] {args.question}\n")
    try:
        print(ask(args.question))
    except errors.APIError as e:
        print(api_error_message(e.code, e.message or ""))
        #print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()