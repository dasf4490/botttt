import openai
import os

# OpenAI APIキーの設定
openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_message(message: str) -> bool:
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"以下のメッセージが不適切かどうか判定してください:\n\n\"{message}\"",
            max_tokens=50
        )
        result = response['choices'][0]['text'].strip().lower()
        return "不適切" in result
    except Exception as e:
        print(f"Error during analysis: {e}")
        return False
