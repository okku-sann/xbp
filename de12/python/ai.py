# de12/python/ai.py
import openai

def ask_openai(prompt):
    # APIキーは環境変数から取得する（安全）
    import os
    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
