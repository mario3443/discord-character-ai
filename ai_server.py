from flask import Flask, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv

# 讀取 .env 裡的 OPENAI_API_KEY
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "").strip()
    print(f" 收到訊息：{user_message}")

    try:
        # 設定系統提示詞
        # 之後可以修改成自己的想法
        system_prompt = (
        "用繁體中文回答"
        "你是一位帶有知性個性的小杰，"
        "你喜歡閱讀和學習新知識，"
        "你會用溫和的語氣回答問題，"
        "並且喜歡分享有趣的事物。"
        "請用簡潔明瞭的方式回答問題，"
        )

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )

        ai_reply = completion.choices[0].message.content.strip()
        print(f"小杰回應：{ai_reply}")
        return jsonify({"reply": ai_reply})

    except Exception as e:
        print(f"❌ GPT 生成失敗：{e}")
        return jsonify({"reply": "GPT 生成失敗，請稍後再試"}), 500

if __name__ == "__main__":
    app.run(port=5005, debug=True)
